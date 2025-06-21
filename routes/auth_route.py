
# # from flask import Blueprint, request, jsonify, current_app
# # from models.user_model import User
# # import jwt
# # from functools import wraps
# # import traceback
# # import logging

# # auth_bp = Blueprint("auth", __name__)

# # def token_required(f):
# #     @wraps(f)
# #     def decorated(*args, **kwargs):
# #         token = None
        
# #         if 'Authorization' in request.headers:
# #             auth_header = request.headers['Authorization']
# #             if auth_header.startswith('Bearer '):
# #                 token = auth_header.split(' ')[1]
        
# #         if not token:
# #             return jsonify({'message': 'Token is missing!'}), 401
        
# #         try:
# #             data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
# #             current_user = User.get_user_by_id(data['sub'])
# #             if not current_user:
# #                 return jsonify({'message': 'Invalid token!'}), 401
# #         except Exception as e:
# #             logging.error(f"Token validation error: {str(e)}")
# #             return jsonify({'message': 'Invalid token!'}), 401
        
# #         return f(current_user, *args, **kwargs)
    
# #     return decorated

# # @auth_bp.route("/register", methods=["POST"])
# # def register():
# #     try:
# #         # Get JSON data from request
# #         data = request.get_json()
        
# #         # Debug: Print received data
# #         print("Received registration data:", data)
# #         logging.info(f"Registration attempt for data: {data}")
        
# #         # Validate input
# #         if not data:
# #             return jsonify({"error": "No data provided"}), 400
            
# #         # Check required fields
# #         required_fields = ['username', 'email', 'password']
# #         for field in required_fields:
# #             if not data.get(field):
# #                 return jsonify({"error": f"{field.capitalize()} is required"}), 400
        
# #         username = data.get('username').strip()
# #         email = data.get('email').strip().lower()
# #         password = data.get('password')
        
# #         # Basic validation
# #         if len(username) < 3:
# #             return jsonify({"error": "Username must be at least 3 characters long"}), 400
            
# #         if len(password) < 6:
# #             return jsonify({"error": "Password must be at least 6 characters long"}), 400
            
# #         if '@' not in email or '.' not in email:
# #             return jsonify({"error": "Please provide a valid email address"}), 400
        
# #         # Create user
# #         success, result = User.create_user(username, email, password)
        
# #         if success:
# #             # Generate token
# #             token = User.generate_token(result)
            
# #             # Get user data
# #             user = User.get_user_by_id(result)
            
# #             # Remove password from user data if present
# #             if user and 'password' in user:
# #                 del user['password']
            
# #             response_data = {
# #                 "message": "User registered successfully",
# #                 "token": token,
# #                 "user": user,
# #                 "success": True
# #             }
            
# #             print(f"Registration successful for user: {username}")
# #             logging.info(f"User registered successfully: {username}")
            
# #             return jsonify(response_data), 201
# #         else:
# #             print(f"Registration failed: {result}")
# #             logging.error(f"Registration failed: {result}")
# #             return jsonify({"error": result, "success": False}), 400
            
# #     except Exception as e:
# #         # Log the full stack trace
# #         error_traceback = traceback.format_exc()
# #         logging.error(f"Registration error: {str(e)}\n{error_traceback}")
# #         print(f"Registration error: {str(e)}\n{error_traceback}")
# #         return jsonify({
# #             "error": f"Server error: {str(e)}", 
# #             "success": False
# #         }), 500

# # @auth_bp.route("/login", methods=["POST"])
# # def login():
# #     try:
# #         data = request.get_json()
        
# #         print("Received login data:", data)
# #         logging.info(f"Login attempt for: {data.get('email') if data else 'No data'}")
        
# #         # Validate input
# #         if not data or not data.get('email') or not data.get('password'):
# #             return jsonify({"error": "Missing email or password", "success": False}), 400
        
# #         email = data.get('email').strip().lower()
# #         password = data.get('password')
        
# #         # Authenticate user
# #         success, result = User.authenticate(email, password)
        
# #         if success:
# #             # Generate token
# #             token = User.generate_token(result['id'])
            
# #             # Return user data without password
# #             user_data = {
# #                 'id': result['id'],
# #                 'username': result['username'],
# #                 'email': result['email']
# #             }
            
# #             response_data = {
# #                 "message": "Login successful",
# #                 "token": token,
# #                 "user": user_data,
# #                 "success": True
# #             }
            
# #             print(f"Login successful for user: {email}")
# #             logging.info(f"Login successful for user: {email}")
            
# #             return jsonify(response_data), 200
# #         else:
# #             print(f"Login failed for {email}: {result}")
# #             logging.warning(f"Login failed for {email}: {result}")
# #             return jsonify({"error": result, "success": False}), 401
            
# #     except Exception as e:
# #         # Log the full stack trace
# #         error_traceback = traceback.format_exc()
# #         logging.error(f"Login error: {str(e)}\n{error_traceback}")
# #         print(f"Login error: {str(e)}\n{error_traceback}")
# #         return jsonify({
# #             "error": f"Server error: {str(e)}", 
# #             "success": False
# #         }), 500

# # @auth_bp.route("/profile", methods=["GET"])
# # @token_required
# # def profile(current_user):
# #     try:
# #         # Remove password from user data if present
# #         if current_user and 'password' in current_user:
# #             del current_user['password']
            
# #         return jsonify({
# #             "user": current_user,
# #             "success": True
# #         }), 200
# #     except Exception as e:
# #         logging.error(f"Profile error: {str(e)}")
# #         return jsonify({
# #             "error": "Failed to fetch profile",
# #             "success": False
# #         }), 500

# # # Health check endpoint
# # @auth_bp.route("/health", methods=["GET"])
# # def health_check():
# #     return jsonify({
# #         "status": "healthy",
# #         "service": "auth",
# #         "success": True
# #     }), 200




# # @auth_bp.route('/profile/<username>', methods=['GET'])
# # def get_user_profile(username):
# #     try:
# #         conn = get_db_connection()
# #         cursor = conn.cursor(dictionary=True)

# #         cursor.execute("SELECT id, username, email, created_at FROM stoker WHERE username = %s", (username,))
# #         user = cursor.fetchone()

# #         if user:
# #             return jsonify({"success": True, "user": user}), 200
# #         else:
# #             return jsonify({"success": False, "error": "User not found"}), 404
# #     except Exception as e:
# #         logging.error(f"Get user profile error: {str(e)}")
# #         return jsonify({"success": False, "error": "Server error"}), 500
# #     finally:
# #         if 'cursor' in locals():
# #             cursor.close()
# #         if 'conn' in locals():
# #             conn.close()






# # /////////////////////////////


# from flask import Blueprint, request, jsonify, current_app
# from models.user_model import User
# import jwt
# from functools import wraps
# import traceback
# import logging

# auth_bp = Blueprint("auth", __name__)

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
        
#         if 'Authorization' in request.headers:
#             auth_header = request.headers['Authorization']
#             if auth_header.startswith('Bearer '):
#                 token = auth_header.split(' ')[1]
        
#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401
        
#         try:
#             data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
#             current_user = User.get_user_by_id(data['sub'])
#             if not current_user:
#                 return jsonify({'message': 'Invalid token!'}), 401
#         except Exception as e:
#             logging.error(f"Token validation error: {str(e)}")
#             return jsonify({'message': 'Invalid token!'}), 401
        
#         return f(current_user, *args, **kwargs)
    
#     return decorated

# @auth_bp.route("/register", methods=["POST"])
# def register():
#     try:
#         # Get JSON data from request
#         data = request.get_json()
        
#         # Debug: Print received data
#         print("Received registration data:", data)
#         logging.info(f"Registration attempt for data: {data}")
        
#         # Validate input
#         if not data:
#             return jsonify({"error": "No data provided"}), 400
            
#         # Check required fields
#         required_fields = ['username', 'email', 'password']
#         for field in required_fields:
#             if not data.get(field):
#                 return jsonify({"error": f"{field.capitalize()} is required"}), 400
        
#         username = data.get('username').strip()
#         email = data.get('email').strip().lower()
#         password = data.get('password')
        
#         # Basic validation
#         if len(username) < 3:
#             return jsonify({"error": "Username must be at least 3 characters long"}), 400
            
#         if len(password) < 6:
#             return jsonify({"error": "Password must be at least 6 characters long"}), 400
            
#         if '@' not in email or '.' not in email:
#             return jsonify({"error": "Please provide a valid email address"}), 400
        
#         # Create user
#         success, result = User.create_user(username, email, password)
        
#         if success:
#             # Generate token
#             token = User.generate_token(result)
            
#             # Get user data
#             user = User.get_user_by_id(result)
            
#             # Remove password from user data if present
#             if user and 'password' in user:
#                 del user['password']
            
#             response_data = {
#                 "message": "User registered successfully",
#                 "token": token,
#                 "user": user,
#                 "success": True
#             }
            
#             print(f"Registration successful for user: {username}")
#             logging.info(f"User registered successfully: {username}")
            
#             return jsonify(response_data), 201
#         else:
#             print(f"Registration failed: {result}")
#             logging.error(f"Registration failed: {result}")
#             return jsonify({"error": result, "success": False}), 400
            
#     except Exception as e:
#         # Log the full stack trace
#         error_traceback = traceback.format_exc()
#         logging.error(f"Registration error: {str(e)}\n{error_traceback}")
#         print(f"Registration error: {str(e)}\n{error_traceback}")
#         return jsonify({
#             "error": f"Server error: {str(e)}", 
#             "success": False
#         }), 500

# @auth_bp.route("/login", methods=["POST"])
# def login():
#     try:
#         data = request.get_json()
        
#         print("Received login data:", data)
#         logging.info(f"Login attempt for: {data.get('email') if data else 'No data'}")
        
#         # Validate input
#         if not data or not data.get('email') or not data.get('password'):
#             return jsonify({"error": "Missing email or password", "success": False}), 400
        
#         email = data.get('email').strip().lower()
#         password = data.get('password')
        
#         # Authenticate user
#         success, result = User.authenticate(email, password)
        
#         if success:
#             # Generate token
#             token = User.generate_token(result['id'])
            
#             # Return user data without password
#             user_data = {
#                 'id': result['id'],
#                 'username': result['username'],
#                 'email': result['email']
#             }
            
#             response_data = {
#                 "message": "Login successful",
#                 "token": token,
#                 "user": user_data,
#                 "success": True
#             }
            
#             print(f"Login successful for user: {email}")
#             logging.info(f"Login successful for user: {email}")
            
#             return jsonify(response_data), 200
#         else:
#             print(f"Login failed for {email}: {result}")
#             logging.warning(f"Login failed for {email}: {result}")
#             return jsonify({"error": result, "success": False}), 401
            
#     except Exception as e:
#         # Log the full stack trace
#         error_traceback = traceback.format_exc()
#         logging.error(f"Login error: {str(e)}\n{error_traceback}")
#         print(f"Login error: {str(e)}\n{error_traceback}")
#         return jsonify({
#             "error": f"Server error: {str(e)}", 
#             "success": False
#         }), 500

# @auth_bp.route("/profile", methods=["GET"])
# @token_required
# def profile(current_user):
#     try:
#         # Remove password from user data if present
#         if current_user and 'password' in current_user:
#             del current_user['password']
            
#         return jsonify({
#             "user": current_user,
#             "success": True
#         }), 200
#     except Exception as e:
#         logging.error(f"Profile error: {str(e)}")
#         return jsonify({
#             "error": "Failed to fetch profile",
#             "success": False
#         }), 500

# # Health check endpoint
# @auth_bp.route("/health", methods=["GET"])
# def health_check():
#     return jsonify({
#         "status": "healthy",
#         "service": "auth",
#         "success": True
#     }), 200

# # Get user profile by username - Using existing User model
# @auth_bp.route('/profile/<username>', methods=['GET'])
# def get_user_profile(username):
#     try:
#         print(f"Fetching profile for username: {username}")
#         logging.info(f"Profile request for username: {username}")
        
#         # Use the existing User model method to get user by username
#         user = User.get_user_by_username(username)
        
#         if user:
#             print(f"User found: {user}")
            
#             # Remove password from user data if present
#             if isinstance(user, dict) and 'password' in user:
#                 del user['password']
            
#             return jsonify({
#                 "success": True, 
#                 "user": user
#             }), 200
#         else:
#             print(f"User not found in database: {username}")
#             return jsonify({
#                 "success": False, 
#                 "error": "User not found"
#             }), 404
            
#     except Exception as e:
#         error_msg = f"Get user profile error: {str(e)}"
#         print(error_msg)
#         logging.error(f"{error_msg}\n{traceback.format_exc()}")
#         return jsonify({
#             "success": False, 
#             "error": "Server error"
#         }), 500



# ///////////////////////////////////

from flask import Blueprint, request, jsonify, current_app
from models.user_model import User
import jwt
from functools import wraps
import traceback
import logging

auth_bp = Blueprint("auth", __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.get_user_by_id(data['sub'])
            if not current_user:
                return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            logging.error(f"Token validation error: {str(e)}")
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        print("Received registration data:", data)
        logging.info(f"Registration attempt for data: {data}")
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"{field.capitalize()} is required"}), 400
        
        username = data.get('username').strip()
        email = data.get('email').strip().lower()
        password = data.get('password')
        
        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters long"}), 400
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long"}), 400
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Please provide a valid email address"}), 400
        
        success, result = User.create_user(username, email, password)
        
        if success:
            token = User.generate_token(result)
            user = User.get_user_by_id(result)
            
            if user and 'password' in user:
                del user['password']
            
            response_data = {
                "message": "User registered successfully",
                "token": token,
                "user": user,
                "success": True
            }
            
            print(f"Registration successful for user: {username}")
            logging.info(f"User registered successfully: {username}")
            
            return jsonify(response_data), 201
        else:
            print(f"Registration failed: {result}")
            logging.error(f"Registration failed: {result}")
            return jsonify({"error": result, "success": False}), 400
            
    except Exception as e:
        error_traceback = traceback.format_exc()
        logging.error(f"Registration error: {str(e)}\n{error_traceback}")
        print(f"Registration error: {str(e)}\n{error_traceback}")
        return jsonify({
            "error": f"Server error: {str(e)}", 
            "success": False
        }), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print("Received login data:", data)
        logging.info(f"Login attempt for: {data.get('email') if data else 'No data'}")
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing email or password", "success": False}), 400
        
        email = data.get('email').strip().lower()
        password = data.get('password')
        
        success, result = User.authenticate(email, password)
        
        if success:
            token = User.generate_token(result['id'])
            
            user_data = {
                'id': result['id'],
                'username': result['username'],
                'email': result['email']
            }
            
            response_data = {
                "message": "Login successful",
                "token": token,
                "user": user_data,
                "success": True
            }
            
            print(f"Login successful for user: {email}")
            logging.info(f"Login successful for user: {email}")
            
            return jsonify(response_data), 200
        else:
            print(f"Login failed for {email}: {result}")
            logging.warning(f"Login failed for {email}: {result}")
            return jsonify({"error": result, "success": False}), 401
            
    except Exception as e:
        error_traceback = traceback.format_exc()
        logging.error(f"Login error: {str(e)}\n{error_traceback}")
        print(f"Login error: {str(e)}\n{error_traceback}")
        return jsonify({
            "error": f"Server error: {str(e)}", 
            "success": False
        }), 500

@auth_bp.route("/profile", methods=["GET"])
@token_required
def profile(current_user):
    try:
        if current_user and 'password' in current_user:
            del current_user['password']
            
        return jsonify({
            "user": current_user,
            "success": True
        }), 200
    except Exception as e:
        logging.error(f"Profile error: {str(e)}")
        return jsonify({
            "error": "Failed to fetch profile",
            "success": False
        }), 500

@auth_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "auth",
        "success": True
    }), 200

# Debug endpoint to see all users
@auth_bp.route('/debug/users', methods=['GET'])
def debug_users():
    try:
        users = User.get_all_users()
        return jsonify({
            "success": True,
            "users": users,
            "count": len(users)
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# # Profile route by username
# @auth_bp.route('/profile/<username>', methods=['GET'])
# def get_user_profile(username):
#     try:
#         print(f"Fetching profile for username: {username}")
#         logging.info(f"Profile request for username: {username}")
        
#         # Use the User model method
#         user = User.get_user_by_username(username)
        
#         if user:
#             print(f"User found: {user}")
            
#             # Remove password if present
#             if isinstance(user, dict) and 'password' in user:
#                 del user['password']
            
#             return jsonify({
#                 "success": True, 
#                 "user": user
#             }), 200
#         else:
#             print(f"User not found in database: {username}")
            
#             # For debugging, let's also check what users exist
#             all_users = User.get_all_users()
#             usernames = [u['username'] for u in all_users] if all_users else []
            
#             return jsonify({
#                 "success": False, 
#                 "error": f"User '{username}' not found",
#                 "available_usernames": usernames
#             }), 404
            
#     except Exception as e:
#         error_msg = f"Get user profile error: {str(e)}"
#         print(error_msg)
#         logging.error(f"{error_msg}\n{traceback.format_exc()}")
#         return jsonify({
#             "success": False, 
#             "error": "Server error",
#             "details": str(e)
#         }), 500



@auth_bp.route('/profile/<username>', methods=['GET'])
def get_user_profile(username):
    try:
        print(f"=== PROFILE REQUEST DEBUG ===")
        print(f"Fetching profile for username: {username}")
        logging.info(f"Profile request for username: {username}")
        
        # Use the User model method
        user = User.get_user_by_username(username)
        
        print(f"User query result: {user}")
        print(f"User type: {type(user)}")
        
        if user:
            print(f"User found: {user}")
            
            # Remove password if present
            if isinstance(user, dict) and 'password' in user:
                del user['password']
            
            response_data = {
                "success": True, 
                "user": user
            }
            
            print(f"Sending response: {response_data}")
            
            return jsonify(response_data), 200
        else:
            print(f"User not found in database: {username}")
            
            # For debugging, let's also check what users exist
            all_users = User.get_all_users()
            usernames = [u['username'] for u in all_users] if all_users else []
            
            print(f"Available users: {usernames}")
            
            return jsonify({
                "success": False, 
                "error": f"User '{username}' not found",
                "available_usernames": usernames
            }), 404
            
    except Exception as e:
        error_msg = f"Get user profile error: {str(e)}"
        print(error_msg)
        print(f"Full traceback: {traceback.format_exc()}")
        logging.error(f"{error_msg}\n{traceback.format_exc()}")
        return jsonify({
            "success": False, 
            "error": "Server error",
            "details": str(e)
        }), 500
