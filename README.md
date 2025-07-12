# SQL Agent with LangGraph

A powerful SQL agent built with LangGraph, FastAPI, PostgreSQL, and React that provides intelligent database operations with JWT authentication and a modern web interface.

## Features

- 🤖 **LangGraph-powered SQL Agent**: Intelligent SQL query execution and analysis
- 🔐 **JWT Authentication**: Secure user authentication and authorization
- 📊 **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- 🗄️ **PostgreSQL Integration**: Robust database connectivity
- 📚 **Schema Management**: Database schema inspection and management
- 🧪 **Postman Testing**: Complete test collection for all endpoints
- 🔄 **Real-time Processing**: Fast and efficient query execution
- 🎨 **React Frontend**: Modern web interface for database operations
- ⚡ **Quick Setup**: Automated environment configuration and setup
- 📖 **Configuration Guide**: Comprehensive setup and configuration documentation

## Tech Stack

- **Backend**: FastAPI, Python 3.8+
- **Frontend**: React, Vite, JavaScript/TypeScript
- **Database**: PostgreSQL
- **AI/ML**: LangChain, LangGraph, OpenAI
- **Authentication**: JWT (JSON Web Tokens)
- **Testing**: Postman Collection
- **ORM**: SQLAlchemy

## Prerequisites

- Python 3.8 or higher
- Node.js 16+ (for frontend)
- PostgreSQL database
- OpenAI API key

## Quick Setup

### Option 1: Automated Quick Setup
```bash
# Run the quick setup script
python quick_setup.py
```

### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd sql-agent
   ```

2. **Install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend/frontend
   npm install
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   # Database Configuration
   DATABASE_URL=postgresql://username:password@localhost:5432/sql_agent_db
   
   # JWT Configuration
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # OpenAI Configuration
   OPENAI_API_KEY=your-openai-api-key-here
   
   # Application Configuration
   DEBUG=True
   HOST=0.0.0.0
   PORT=8000
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```

6. **Run the backend**
   ```bash
   python run.py
   ```

7. **Run the frontend (in a new terminal)**
   ```bash
   cd frontend/frontend
   npm run dev
   ```

The API will be available at `http://localhost:8000` and the frontend at `http://localhost:5173`

## Frontend Features

The React frontend provides a modern web interface for:

- **SQL Query Editor**: Write and execute SQL queries with syntax highlighting
- **Database Browser**: Explore tables, schemas, and data
- **CRUD Operations**: Create, read, update, and delete records through a user-friendly interface
- **Authentication**: Login and registration forms
- **Real-time Results**: View query results in a formatted table
- **Error Handling**: Clear error messages and suggestions

## Configuration Guide

For detailed setup instructions and troubleshooting, see the [Configuration Guide](CONFIGURATION_GUIDE.md).

## API Documentation

### Authentication Endpoints

#### Register User
```http
POST /register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpassword123"
}
```

#### Login
```http
POST /token
Content-Type: application/x-www-form-urlencoded

username=testuser&password=testpassword123
```

#### Get Current User
```http
GET /users/me
Authorization: Bearer <access_token>
```

### SQL Agent Endpoints

#### Execute SQL Query
```http
POST /sql/query
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "query": "SELECT * FROM employees LIMIT 5",
  "description": "Get first 5 employees"
}
```

### CRUD Operations

#### Create Record
```http
POST /crud
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "operation": "CREATE",
  "table": "employees",
  "data": {
    "name": "New Employee",
    "email": "new@example.com",
    "department": "IT",
    "salary": 80000.00
  }
}
```

#### Read Records
```http
POST /crud
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "operation": "READ",
  "table": "employees",
  "data": {},
  "where_clause": {
    "department": "Engineering"
  }
}
```

#### Update Records
```http
POST /crud
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "operation": "UPDATE",
  "table": "employees",
  "data": {
    "salary": 85000.00
  },
  "where_clause": {
    "email": "john@example.com"
  }
}
```

#### Delete Records
```http
POST /crud
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "operation": "DELETE",
  "table": "employees",
  "data": {},
  "where_clause": {
    "email": "new@example.com"
  }
}
```

### Schema Management

#### List All Tables
```http
GET /schema/tables
Authorization: Bearer <access_token>
```

#### Get Table Schema
```http
GET /schema/{table_name}
Authorization: Bearer <access_token>
```

### Health Check
```http
GET /health
```

## Testing with Postman

1. **Import the Postman Collection**
   - Open Postman
   - Import the `SQL_Agent_API.postman_collection.json` file

2. **Set up Environment Variables**
   - Create a new environment in Postman
   - Add variables:
     - `base_url`: `http://localhost:8000`
     - `access_token`: (leave empty initially)

3. **Test Flow**
   1. Run "Register User" to create a test account
   2. Run "Login - Get Token" to authenticate
   3. Copy the `access_token` from the response
   4. Set the `access_token` variable in your Postman environment
   5. Test all other endpoints

## Sample Database Schema

The application comes with sample tables:

### Employees Table
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE DEFAULT CURRENT_DATE
);
```

### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## LangGraph Agent Features

The SQL agent uses LangGraph to provide intelligent database operations:

- **Natural Language Processing**: Understands and processes SQL queries
- **Schema Awareness**: Automatically inspects table structures
- **Error Handling**: Provides clear error messages and suggestions
- **Query Optimization**: Suggests improvements for complex queries
- **Security**: Validates queries to prevent SQL injection

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password encryption
- **SQL Injection Protection**: Parameterized queries
- **Input Validation**: Pydantic schema validation
- **Error Handling**: Secure error responses

## Development

### Project Structure
```
sql-agent/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration settings
│   ├── database.py      # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # Authentication logic
│   └── sql_agent.py     # LangGraph SQL agent
├── frontend/
│   └── frontend/        # React application
│       ├── src/         # React source code
│       ├── public/      # Static assets
│       ├── package.json # Frontend dependencies
│       └── vite.config.js # Vite configuration
├── requirements.txt      # Python dependencies
├── run.py               # Application runner
├── init_db.py           # Database initialization
├── quick_setup.py       # Automated setup script
├── setup.py             # Manual setup script
├── CONFIGURATION_GUIDE.md # Detailed setup guide
├── env_example.txt      # Environment variables template
├── SQL_Agent_API.postman_collection.json
└── README.md
```

### Running in Development Mode

#### Backend
```bash
python run.py
```

#### Frontend
```bash
cd frontend/frontend
npm run dev
```

### Database Migrations
```bash
# Initialize Alembic (if needed)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## API Response Examples

### Successful SQL Query
```json
{
  "result": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "department": "Engineering",
      "salary": "75000.00",
      "hire_date": "2024-01-15"
    }
  ],
  "query": "SELECT * FROM employees LIMIT 1",
  "message": "Successfully retrieved 1 employee record.",
  "success": true
}
```

### CRUD Operation Response
```json
{
  "success": true,
  "message": "Record created successfully",
  "affected_rows": 1,
  "data": [
    {
      "id": 4,
      "name": "New Employee",
      "email": "new@example.com",
      "department": "IT",
      "salary": "80000.00"
    }
  ]
}
```

## Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `http://localhost:8000/docs`
- Review the Postman collection for examples 