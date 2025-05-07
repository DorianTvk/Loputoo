import mysql.connector

def connect_to_db():
    """Connect to the MySQL database."""
    try:
        print("✅ Attempting to connect to the database...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",  
            database="test_automation"
        )
        print("✅ Database connection successful.")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None

def insert_test_result(db, test_name, url, status, error_message, execution_time, screenshot_path, baseline_path=None, new_path=None, diff_path=None, test_type="regular"):
    """Insert a test result into the database, including visual regression paths."""
    print(f"🔵 Inserting test result for: {test_name}, {url}")
    
    if db is None:
        print("❌ No database connection.")
        return
    
    try:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO test_results 
            (test_name, url, status, error_message, execution_time, screenshot_path, baseline_path, new_path, diff_path, test_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (test_name, url, status, error_message, execution_time, screenshot_path, baseline_path, new_path, diff_path, test_type)
        )
        print("✅ Test result inserted.")
    except mysql.connector.Error as err:
        print(f"❌ Error inserting test result: {err}")
    finally:
        cursor.close()

