from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
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

class SimpleSQLAgent:
    def __init__(self):
        self.engine = db_engine
        self.llm = llm

    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute a SQL query and return results."""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                if result.returns_rows:
                    rows = [dict(row._mapping) for row in result]
                    return {
                        "success": True,
                        "data": rows,
                        "message": f"Query executed successfully. Retrieved {len(rows)} rows."
                    }
                else:
                    return {
                        "success": True,
                        "data": [],
                        "message": f"Query executed successfully. {result.rowcount} rows affected."
                    }
        except SQLAlchemyError as e:
            return {
                "success": False,
                "data": [],
                "message": f"Database error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "data": [],
                "message": f"Error: {str(e)}"
            }

    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Get the schema of a specific table."""
        try:
            with self.engine.connect() as connection:
                query = f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = '{table_name}' AND table_schema = 'public'
                ORDER BY ordinal_position;
                """
                result = connection.execute(text(query))
                schema = [dict(row._mapping) for row in result]
                return {
                    "success": True,
                    "data": schema,
                    "message": f"Schema retrieved for table '{table_name}'"
                }
        except Exception as e:
            return {
                "success": False,
                "data": [],
                "message": f"Error getting schema: {str(e)}"
            }

    def list_tables(self) -> Dict[str, Any]:
        """List all tables in the database."""
        try:
            with self.engine.connect() as connection:
                query = """
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
                result = connection.execute(text(query))
                tables = [row[0] for row in result]
                return {
                    "success": True,
                    "data": tables,
                    "message": f"Found {len(tables)} tables"
                }
        except Exception as e:
            return {
                "success": False,
                "data": [],
                "message": f"Error listing tables: {str(e)}"
            }

    def analyze_query(self, query: str) -> str:
        """Use LLM to analyze and explain the query result."""
        try:
            # First execute the query
            result = self.execute_query(query)
            
            if not result["success"]:
                return f"Query failed: {result['message']}"
            
            # Create a prompt for the LLM to analyze the results
            prompt = f"""
            Analyze this SQL query and its results:
            
            Query: {query}
            Results: {json.dumps(result['data'], indent=2)}
            
            Provide a clear explanation of what this query does and what the results mean.
            """
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            return f"Error analyzing query: {str(e)}"

# Create agent instance
sql_agent = SimpleSQLAgent()

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