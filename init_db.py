from sqlalchemy import create_engine, text
from app.config import settings
from app.database import engine
from app.models import Base

def init_database():
    """Initialize the database with sample tables and data."""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create sample tables and data
    with engine.connect() as connection:
        # Create sample tables
        sample_tables = [
            """
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                department VARCHAR(50),
                salary DECIMAL(10,2),
                hire_date DATE DEFAULT CURRENT_DATE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                price DECIMAL(10,2) NOT NULL,
                stock_quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                product_id INTEGER REFERENCES products(id),
                quantity INTEGER NOT NULL,
                total_amount DECIMAL(10,2) NOT NULL,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        ]
        
        for table_sql in sample_tables:
            connection.execute(text(table_sql))
        
        # Insert sample data
        sample_data = [
            # Employees
            "INSERT INTO employees (name, email, department, salary) VALUES ('John Doe', 'john@example.com', 'Engineering', 75000.00)",
            "INSERT INTO employees (name, email, department, salary) VALUES ('Jane Smith', 'jane@example.com', 'Marketing', 65000.00)",
            "INSERT INTO employees (name, email, department, salary) VALUES ('Bob Johnson', 'bob@example.com', 'Sales', 70000.00)",
            
            # Products
            "INSERT INTO products (name, category, price, stock_quantity) VALUES ('Laptop', 'Electronics', 999.99, 50)",
            "INSERT INTO products (name, category, price, stock_quantity) VALUES ('Mouse', 'Electronics', 29.99, 100)",
            "INSERT INTO products (name, category, price, stock_quantity) VALUES ('Desk Chair', 'Furniture', 199.99, 25)",
            
            # Orders
            "INSERT INTO orders (customer_name, product_id, quantity, total_amount) VALUES ('Alice Brown', 1, 1, 999.99)",
            "INSERT INTO orders (customer_name, product_id, quantity, total_amount) VALUES ('Charlie Wilson', 2, 2, 59.98)",
            "INSERT INTO orders (customer_name, product_id, quantity, total_amount) VALUES ('Diana Davis', 3, 1, 199.99)"
        ]
        
        for data_sql in sample_data:
            try:
                connection.execute(text(data_sql))
            except Exception as e:
                print(f"Warning: Could not insert sample data: {e}")
        
        connection.commit()
        print("Database initialized successfully with sample tables and data!")

if __name__ == "__main__":
    init_database() 