# import mysql.connector
# from mysql.connector import Error
# from flask import current_app, g

# def get_db():
#     """Get database connection"""
#     if 'db' not in g:
#         try:
#             g.db = mysql.connector.connect(
#                 host=current_app.config['MYSQL_HOST'],
#                 port=current_app.config['MYSQL_PORT'],
#                 user=current_app.config['MYSQL_USER'],
#                 password=current_app.config['MYSQL_PASSWORD'],
#                 database=current_app.config['MYSQL_DB']
#             )
#             print("Database connection successful")
#         except Error as e:
#             print(f"Error connecting to MySQL: {e}")
#             return None
#     return g.db


# def close_db(e=None):
#     """Close database connection"""
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()

# def init_app(app):
#     """Initialize database with app"""
#     app.teardown_appcontext(close_db)



import mysql.connector
from mysql.connector import Error
from flask import current_app, g
import logging

def get_db():
    """Get database connection"""
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],
                port=current_app.config['MYSQL_PORT'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB']
            )
            print("Database connection successful")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            logging.error(f"Database connection error: {e}")
            return None
    return g.db

def close_db(e=None):
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Initialize database with app"""
    app.teardown_appcontext(close_db)
    
    # Test database connection on startup
    with app.app_context():
        db = get_db()
        if db is None:
            print("WARNING: Could not connect to database on startup!")
        else:
            print("Database connection test successful")
