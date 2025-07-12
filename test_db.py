from app.database import engine
from sqlalchemy import text
import json

def test_database():
    try:
        with engine.connect() as connection:
            # Test if employees table exists
            result = connection.execute(text("SELECT * FROM employees LIMIT 3"))
            data = [dict(row._mapping) for row in result]
            print("✅ Employees table exists and has data:")
            print(json.dumps(data, indent=2, default=str))
            
            # Check table count
            result = connection.execute(text("SELECT COUNT(*) as count FROM employees"))
            count = result.fetchone()[0]
            print(f"\n📊 Total employees: {count}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_database() 