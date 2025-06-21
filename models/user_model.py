# import bcrypt
# from database.db import get_db
# import jwt
# import datetime
# from flask import current_app
# import traceback
# import logging

# class User:
#     @staticmethod
#     def create_user(username, email, password):
#         """Create a new user"""
#         db = get_db()
#         if not db:
#             error_msg = "Database connection failed"
#             logging.error(error_msg)
#             return False, error_msg
            
#         cursor = db.cursor(dictionary=True)
        
#         # Check if user already exists
#         try:
#             cursor.execute("SELECT * FROM accounts WHERE email = %s", (email,))
#             if cursor.fetchone():
#                 cursor.close()
#                 return False, "Email already registered"
#         except Exception as e:
#             error_msg = f"Error checking existing user: {str(e)}"
#             logging.error(f"{error_msg}\n{traceback.format_exc()}")
#             cursor.close()
#             return False, error_msg
        
#         # Hash the password
#         try:
#             hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#         except Exception as e:
#             error_msg = f"Error hashing password: {str(e)}"
#             logging.error(f"{error_msg}\n{traceback.format_exc()}")
#             cursor.close()
#             return False, error_msg
        
#         # Insert new user
#         try:
#             cursor.execute(
#                 "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)",
#                 (username, email, hashed_password)
#             )
#             db.commit()
#             user_id = cursor.lastrowid
#             cursor.close()
#             return True, user_id
#         except Exception as e:
#             error_msg = f"Error creating user: {str(e)}"
#             logging.error(f"{error_msg}\n{traceback.format_exc()}")
#             cursor.close()
#             return False, error_msg
    
#     @staticmethod
#     def authenticate(email, password):
#         """Authenticate a user"""
#         db = get_db()
#         if not db:
#             return False, "Database connection failed"
            
#         cursor = db.cursor(dictionary=True)
        
#         # Find user by email
#         try:
#             cursor.execute("SELECT * FROM accounts WHERE email = %s", (email,))
#             user = cursor.fetchone()
#             cursor.close()
            
#             if not user:
#                 return False, "Invalid email or password"
            
#             # Check password
#             if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
#                 return True, user
#             else:
#                 return False, "Invalid email or password"
#         except Exception as e:
#             error_msg = f"Authentication error: {str(e)}"
#             logging.error(f"{error_msg}\n{traceback.format_exc()}")
#             cursor.close()
#             return False, error_msg
    
#     @staticmethod
#     def generate_token(user_id):
#         """Generate JWT token"""
#         try:
#             payload = {
#                 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
#                 'iat': datetime.datetime.utcnow(),
#                 'sub': user_id
#             }
#             return jwt.encode(
#                 payload,
#                 current_app.config.get('SECRET_KEY'),
#                 algorithm='HS256'
#             )
#         except Exception as e:
#             error_msg = f"Token generation error: {str(e)}"
#             logging.error(f"{error_msg}\n{traceback.format_exc()}")
#             raise
    
#     @staticmethod
#     def get_user_by_id(user_id):
#         """Get user by ID"""
#         db = get_db()
#         if not db:
#             return None
            
#         cursor = db.cursor(dictionary=True)
        
#         try:
#             cursor.execute("SELECT id, username, email FROM accounts WHERE id = %s", (user_id,))
#             user = cursor.fetchone()
#             cursor.close()
#             return user
#         except Exception as e:
#             error_msg = f"Error fetching user: {str(e)}"
#             logging.error(f"{error_msg}\n{traceback.format_exc()}")
#             cursor.close()
#             return None





import bcrypt
from database.db import get_db
import jwt
import datetime
from flask import current_app
import traceback
import logging

class User:
    @staticmethod
    def create_user(username, email, password):
        """Create a new user"""
        db = get_db()
        if not db:
            error_msg = "Database connection failed"
            logging.error(error_msg)
            return False, error_msg
            
        cursor = db.cursor(dictionary=True)
        
        # Check if user already exists
        try:
            cursor.execute("SELECT * FROM accounts WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                return False, "Email already registered"
        except Exception as e:
            error_msg = f"Error checking existing user: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            cursor.close()
            return False, error_msg
        
        # Hash the password
        try:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        except Exception as e:
            error_msg = f"Error hashing password: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            cursor.close()
            return False, error_msg
        
        # Insert new user
        try:
            cursor.execute(
                "INSERT INTO accounts (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            db.commit()
            user_id = cursor.lastrowid
            cursor.close()
            return True, user_id
        except Exception as e:
            error_msg = f"Error creating user: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            cursor.close()
            return False, error_msg
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate a user"""
        db = get_db()
        if not db:
            return False, "Database connection failed"
            
        cursor = db.cursor(dictionary=True)
        
        # Find user by email
        try:
            cursor.execute("SELECT * FROM accounts WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            
            if not user:
                return False, "Invalid email or password"
            
            # Check password
            if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return True, user
            else:
                return False, "Invalid email or password"
        except Exception as e:
            error_msg = f"Authentication error: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            cursor.close()
            return False, error_msg
    
    @staticmethod
    def generate_token(user_id):
        """Generate JWT token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            error_msg = f"Token generation error: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            raise
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        db = get_db()
        if not db:
            return None
            
        cursor = db.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, username, email FROM accounts WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Exception as e:
            error_msg = f"Error fetching user: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            cursor.close()
            return None

    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        db = get_db()
        if not db:
            logging.error("Database connection failed in get_user_by_username")
            return None
            
        cursor = db.cursor(dictionary=True)
        
        try:
            # Query the accounts table (not stoker)
            cursor.execute("SELECT id, username, email, created_at FROM accounts WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if user:
                # Convert datetime to string if needed
                if 'created_at' in user and user['created_at']:
                    if hasattr(user['created_at'], 'isoformat'):
                        user['created_at'] = user['created_at'].isoformat()
                    else:
                        user['created_at'] = str(user['created_at'])
                        
                logging.info(f"User found by username {username}: {user}")
            else:
                logging.info(f"No user found with username: {username}")
            
            cursor.close()
            return user
            
        except Exception as e:
            error_msg = f"Error getting user by username: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            cursor.close()
            return None

    @staticmethod
    def get_all_users():
        """Get all users (for debugging)"""
        db = get_db()
        if not db:
            return []
            
        cursor = db.cursor(dictionary=True)
        
        try:
            cursor.execute("SELECT id, username, email, created_at FROM accounts")
            users = cursor.fetchall()
            cursor.close()
            return users
        except Exception as e:
            error_msg = f"Error fetching all users: {str(e)}"
            logging.error(f"{error_msg}\n{traceback.format_exc()}")
            cursor.close()
            return []
