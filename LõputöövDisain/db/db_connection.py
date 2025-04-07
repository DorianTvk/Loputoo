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

def insert_test_result(test_name, url, status, error_message, execution_time):
    """Insert a test result into the database."""
    print(f"🔵 Inserting test result for: {test_name}, {url}")
    db = connect_to_db()
    if db is None:
        print("❌ Database connection failed!")
        return

    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO test_results (test_name, url, status, error_message, execution_time) VALUES (%s, %s, %s, %s, %s)",
            (test_name, url, status, error_message, execution_time)
        )
        db.commit()
        print("✅ Test result stored successfully!")
    except mysql.connector.Error as err:
        print(f"❌ Error inserting test result: {err}")
    finally:
        cursor.close()
        db.close()

