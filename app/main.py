from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import json
from sqlalchemy import text

from app.database import get_db, engine
from app.models import Base, User
from app.schemas import UserCreate, User as UserSchema, Token, SQLQuery, SQLResponse, CRUDOperation, CRUDResponse
from app.auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash
from app.sql_agent_simple import sql_agent, crud_ops
from app.config import settings
from app.agentic_nl import router as agentic_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SQL Agent API",
    description="A LangChain-powered SQL agent with CRUD operations and JWT authentication",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agentic_router)

# Authentication endpoints
@app.post("/register", response_model=UserSchema)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login to get access token."""
    print("hello",form_data.username, form_data.password)
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

# SQL Agent endpoints
@app.post("/sql/query", response_model=SQLResponse)
async def execute_sql_query(
    query: SQLQuery,
    current_user: User = Depends(get_current_active_user)
):
    """Execute a SQL query using the LangChain agent."""
    try:
        # Execute the query
        result = sql_agent.execute_query(query.query)
        
        # Get LLM analysis if query was successful
        if result["success"]:
            analysis = sql_agent.analyze_query(query.query)
        else:
            analysis = result["message"]
        
        return SQLResponse(
            result=result["data"],
            query=query.query,
            message=analysis,
            success=result["success"]
        )
    except Exception as e:
        return SQLResponse(
            result=[],
            query=query.query,
            message=f"Error executing query: {str(e)}",
            success=False
        )

# CRUD Operations endpoints
@app.post("/crud", response_model=CRUDResponse)
async def perform_crud_operation(
    operation: CRUDOperation,
    current_user: User = Depends(get_current_active_user)
):
    """Perform CRUD operations on the database."""
    try:
        if operation.operation.upper() == "CREATE":
            result = crud_ops.create_record(operation.table, operation.data)
        elif operation.operation.upper() == "READ":
            result = crud_ops.read_records(operation.table, operation.where_clause)
        elif operation.operation.upper() == "UPDATE":
            result = crud_ops.update_records(operation.table, operation.data, operation.where_clause)
        elif operation.operation.upper() == "DELETE":
            result = crud_ops.delete_records(operation.table, operation.where_clause)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid operation. Must be CREATE, READ, UPDATE, or DELETE"
            )
        
        return CRUDResponse(
            success=result["success"],
            message=result["message"],
            affected_rows=len(result.get("data", [])) if result.get("data") else None,
            data=result.get("data")
        )
    except Exception as e:
        return CRUDResponse(
            success=False,
            message=f"Error performing {operation.operation} operation: {str(e)}"
        )

# Database schema endpoints
@app.get("/schema/tables")
async def list_database_tables(current_user: User = Depends(get_current_active_user)):
    """List all tables in the database."""
    try:
        result = sql_agent.list_tables()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing tables: {str(e)}"
        )

@app.get("/schema/{table_name}")
async def get_table_schema(
    table_name: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get the schema of a specific table."""
    try:
        result = sql_agent.get_table_schema(table_name)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting table schema: {str(e)}"
        )

# Simple health check for Railway
@app.get("/")
async def root():
    """Root endpoint for basic health check."""
    return {"status": "ok", "message": "SQL Agent API is running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "SQL Agent API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port) 