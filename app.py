from flask import Flask, jsonify
from flask_cors import CORS
from routes.stock_routes import stock_bp
from routes.portfolio_routes import portfolio_bp
from routes.auth_route import auth_bp
from routes.prediction import prediction_bp
from database.db import init_app
import logging
import os

def create_app():
    # Set up logging
    logging_dir = 'logs'
    os.makedirs(logging_dir, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(logging_dir, 'app.log')),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    # Enable CORS with specific configuration
    # CORS(app, 
    #      origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    #      allow_headers=["Content-Type", "Authorization"],
    #      methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    CORS(app, 
     origins=[
         "http://localhost:3000", 
         "http://127.0.0.1:3000",
         "https://rtsma-frontend.onrender.com"  # <-- Add this
     ],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True  # <-- Include this if you're using cookies or auth
)
    
    # Initialize database
    try:
        init_app(app)
        app.logger.info("Database initialized successfully")
    except Exception as e:
        app.logger.error(f"Database initialization failed: {str(e)}")
    
    # Global error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "success": False
        }), 500

    # Handle 404 errors
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "error": "Endpoint not found",
            "success": False
        }), 404

    # Handle 405 errors (Method Not Allowed)
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "error": "Method not allowed",
            "success": False
        }), 405

    # Register Blueprints
    app.register_blueprint(stock_bp, url_prefix="/api/stocks")
    app.register_blueprint(portfolio_bp, url_prefix="/api/portfolio")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(prediction_bp, url_prefix="/api/predict")

    # Root endpoint
    @app.route("/")
    def home():
        return jsonify({
            "message": "Stock Analysis API",
            "status": "running",
            "endpoints": {
                "auth": "/api/auth",
                "stocks": "/api/stocks", 
                "portfolio": "/api/portfolio"
            }
        })

    # Health check endpoint
    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "service": "stock-analysis-api"
        })

    app.logger.info("Flask application created successfully")
    return app

# if __name__ == "__main__":
    
app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
