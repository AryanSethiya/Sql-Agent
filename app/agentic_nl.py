from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.auth import get_current_active_user
from app.models import User
from app.config import settings
from app.database import get_db
from langchain_openai import ChatOpenAI
from sqlalchemy.orm import Session
import json

router = APIRouter()

class NLQuery(BaseModel):
    instruction: str

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=settings.openai_api_key
)

@router.post("/agent/nl_query")
async def agent_nl_query(
    request: NLQuery,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Accepts a natural language instruction, uses LLM to generate SQL, executes it, and returns the result.
    """
    prompt = f"""
You are a highly reliable and safe AI SQL assistant for a PostgreSQL database.

Database schema:
- Table 'employees':
    - id (integer, primary key)
    - name (string)
    - email (string)
    - department (string)
    - salary (decimal)
    - hire_date (date)
- Table 'products':
    - id (integer, primary key)
    - name (string)
    - category (string)
    - price (decimal)
    - stock_quantity (integer)
    - created_at (timestamp)
- Table 'orders':
    - id (integer, primary key)
    - customer_name (string)
    - product_id (integer, foreign key to products.id)
    - quantity (integer)
    - total_amount (decimal)
    - order_date (timestamp)

Instructions:
- Convert the following natural language instruction into valid SQL query or queries using ONLY the tables and columns listed above.
- If the instruction contains multiple steps, output the SQL queries needed, separated by semicolons, in the correct order.
- Never generate queries that drop tables, alter schema, or delete all records (always require a WHERE clause for DELETE).
- Do not use columns or tables that are not listed in the schema.
- Only output the SQL query or queries, do not include explanations, comments, or any extra text.
- Use single quotes for string values.
- If the instruction is not possible with the schema, output a SELECT statement that returns no rows (e.g., SELECT * FROM employees WHERE 1=0;).

Examples:
Instruction: Add a new employee named Alice Smith with email alice@example.com, department HR, and salary 70000.
SQL: INSERT INTO employees (name, email, department, salary) VALUES ('Alice Smith', 'alice@example.com', 'HR', 70000);

Instruction: Show all employees in the IT department.
SQL: SELECT * FROM employees WHERE department = 'IT';

Instruction: Add a new product named "Monitor" in category "Electronics" with price 199.99 and stock 20.
SQL: INSERT INTO products (name, category, price, stock_quantity) VALUES ('Monitor', 'Electronics', 199.99, 20);

Instruction: Show all orders for customer Alice Brown.
SQL: SELECT * FROM orders WHERE customer_name = 'Alice Brown';

Instruction: Add a new employee named Bob Lee with email bob@example.com, department IT, and salary 80000, then show all employees.
SQL: INSERT INTO employees (name, email, department, salary) VALUES ('Bob Lee', 'bob@example.com', 'IT', 80000); SELECT * FROM employees;

Instruction: Remove all employees (should be prevented).
SQL: SELECT * FROM employees WHERE 1=0;

Instruction: Drop the employees table (should be prevented).
SQL: SELECT * FROM employees WHERE 1=0;

Instruction: {request.instruction}
SQL:
"""
    try:
        # Get SQL from LLM
        response = llm.invoke(prompt)
        sql_query = response.content.strip().split("\n")[0]
        # Execute SQL
        try:
            queries = [q.strip() for q in sql_query.split(';') if q.strip()]
            results = []
            for q in queries:
                try:
                    result = db.execute(text(q))
                    if q.lower().startswith(("insert", "update", "delete")):
                        db.commit()
                    if result.returns_rows:
                        rows = [dict(row._mapping) for row in result]
                        results.append({
                            "sql": q,
                            "data": rows,
                            "message": f"Query executed successfully. Retrieved {len(rows)} rows.",
                            "error": None
                        })
                    else:
                        results.append({
                            "sql": q,
                            "data": [],
                            "message": f"Query executed successfully. {result.rowcount} rows affected.",
                            "error": None
                        })
                except SQLAlchemyError as e:
                    results.append({
                        "sql": q,
                        "data": [],
                        "message": f"Database error: {str(e)}",
                        "error": str(e)
                    })
            return {
                "success": all(r["error"] is None for r in results),
                "sql": sql_query,
                "results": results,
                "message": "All queries executed. See results for details."
            }
        except Exception as e:
            return {
                "success": False,
                "sql": sql_query,
                "results": [],
                "message": f"Execution error: {str(e)}"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM or execution error: {str(e)}") 