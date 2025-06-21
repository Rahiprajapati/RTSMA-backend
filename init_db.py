import mysql.connector
from mysql.connector import Error
import os
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Rahi1807@',
    'database': 'pythonlogin'
}

def init_database():
    """Initialize the database and tables"""
    connection = None
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            print(f"Database '{DB_CONFIG['database']}' checked/created successfully")
            
            # Switch to the database
            cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # Create accounts table if it doesn't exist
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            print("Table 'accounts' checked/created successfully")
            
            # Check if the table has the correct structure
            cursor.execute("DESCRIBE accounts")
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns]
            
            expected_columns = ['id', 'username', 'email', 'password', 'created_at']
            for col in expected_columns:
                if col not in column_names:
                    print(f"WARNING: Column '{col}' is missing from the accounts table")
            
            print("Database initialization completed successfully")
            
    except Error as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)
    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    init_database()
