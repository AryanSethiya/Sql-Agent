from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_core.tools import tool
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import json
from app.config import settings

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=settings.openai_api_key
)

# Database engine
db_engine = create_engine(settings.database_url)

# Define the state
class AgentState:
    def __init__(self, messages: List, query: str = "", result: Dict = None):
        self.messages = messages
        self.query = query
        self.result = result or {}

# Tools for database operations
@tool
def execute_sql_query(query: str) -> str:
    """Execute a SQL query and return the results as JSON."""
    try:
        with db_engine.connect() as connection:
            result = connection.execute(text(query))
            if result.returns_rows:
                rows = [dict(row._mapping) for row in result]
                return json.dumps(rows, default=str)
            else:
                return json.dumps({"affected_rows": result.rowcount})
    except SQLAlchemyError as e:
        return json.dumps({"error": str(e)})

@tool
def get_table_schema(table_name: str) -> str:
    """Get the schema of a specific table."""
    try:
        with db_engine.connect() as connection:
            query = f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
            """
            result = connection.execute(text(query))
            schema = [dict(row._mapping) for row in result]
            return json.dumps(schema, default=str)
    except SQLAlchemyError as e:
        return json.dumps({"error": str(e)})

@tool
def list_tables() -> str:
    """List all tables in the database."""
    try:
        with db_engine.connect() as connection:
            query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
            result = connection.execute(text(query))
            tables = [row[0] for row in result]
            return json.dumps(tables)
    except SQLAlchemyError as e:
        return json.dumps({"error": str(e)})

# Create tool executor
tools = [execute_sql_query, get_table_schema, list_tables]
tool_executor = ToolExecutor(tools)

# Define the agent workflow
def create_sql_agent():
    # Define the state
    class AgentState:
        def __init__(self, messages: List, query: str = "", result: Dict = None):
            self.messages = messages
            self.query = query
            self.result = result or {}

    # Define the nodes
    def should_use_tool(state: AgentState) -> str:
        """Decide whether to use a tool or respond directly."""
        last_message = state.messages[-1].content if state.messages else ""
        if any(keyword in last_message.lower() for keyword in ["select", "insert", "update", "delete", "create", "drop", "schema", "table"]):
            return "use_tool"
        return "respond"

    def use_tool(state: AgentState) -> AgentState:
        """Use the appropriate tool based on the query."""
        last_message = state.messages[-1].content if state.messages else ""
        
        # Determine which tool to use
        if "schema" in last_message.lower() or "structure" in last_message.lower():
            # Extract table name from message
            # This is a simplified extraction - in practice, you'd want more sophisticated parsing
            words = last_message.split()
            table_name = None
            for i, word in enumerate(words):
                if word.lower() in ["table", "schema", "structure"] and i + 1 < len(words):
                    table_name = words[i + 1]
                    break
            
            if table_name:
                result = tool_executor.invoke({"name": "get_table_schema", "arguments": {"table_name": table_name}})
            else:
                result = tool_executor.invoke({"name": "list_tables", "arguments": {}})
        else:
            # Execute SQL query
            result = tool_executor.invoke({"name": "execute_sql_query", "arguments": {"query": last_message}})
        
        state.result = {"tool_result": result}
        return state

    def respond(state: AgentState) -> AgentState:
        """Generate a response based on the tool result."""
        tool_result = state.result.get("tool_result", "")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful SQL assistant. Analyze the query result and provide a clear explanation."),
            ("human", "Query result: {result}\n\nProvide a clear explanation of this result.")
        ])
        
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({"result": tool_result})
        
        state.messages.append(AIMessage(content=response))
        return state

    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("should_use_tool", should_use_tool)
    workflow.add_node("use_tool", use_tool)
    workflow.add_node("respond", respond)
    
    # Add edges
    workflow.add_edge("should_use_tool", "use_tool")
    workflow.add_edge("should_use_tool", "respond")
    workflow.add_edge("use_tool", "respond")
    workflow.add_edge("respond", END)
    
    # Set entry point
    workflow.set_entry_point("should_use_tool")
    
    return workflow.compile()

# Create the agent instance
sql_agent = create_sql_agent()

# CRUD Operations
class CRUDOperations:
    def __init__(self):
        self.engine = db_engine

    def create_record(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record in the specified table."""
        try:
            columns = ", ".join(data.keys())
            values = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in data.values()])
            query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING *"
            
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                connection.commit()
                return {"success": True, "message": "Record created successfully", "data": [dict(result.fetchone()._mapping)]}
        except SQLAlchemyError as e:
            return {"success": False, "message": f"Error creating record: {str(e)}"}

    def read_records(self, table: str, where_clause: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Read records from the specified table."""
        try:
            query = f"SELECT * FROM {table}"
            if where_clause:
                conditions = " AND ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in where_clause.items()])
                query += f" WHERE {conditions}"
            
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                data = [dict(row._mapping) for row in result]
                return {"success": True, "message": f"Retrieved {len(data)} records", "data": data}
        except SQLAlchemyError as e:
            return {"success": False, "message": f"Error reading records: {str(e)}"}

    def update_records(self, table: str, data: Dict[str, Any], where_clause: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update records in the specified table."""
        try:
            set_clause = ", ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in data.items()])
            query = f"UPDATE {table} SET {set_clause}"
            
            if where_clause:
                conditions = " AND ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in where_clause.items()])
                query += f" WHERE {conditions}"
            
            query += " RETURNING *"
            
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                connection.commit()
                data = [dict(row._mapping) for row in result]
                return {"success": True, "message": f"Updated {len(data)} records", "data": data}
        except SQLAlchemyError as e:
            return {"success": False, "message": f"Error updating records: {str(e)}"}

    def delete_records(self, table: str, where_clause: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Delete records from the specified table."""
        try:
            query = f"DELETE FROM {table}"
            
            if where_clause:
                conditions = " AND ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in where_clause.items()])
                query += f" WHERE {conditions}"
            
            query += " RETURNING *"
            
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                connection.commit()
                data = [dict(row._mapping) for row in result]
                return {"success": True, "message": f"Deleted {len(data)} records", "data": data}
        except SQLAlchemyError as e:
            return {"success": False, "message": f"Error deleting records: {str(e)}"}

# Create CRUD operations instance
crud_ops = CRUDOperations() 