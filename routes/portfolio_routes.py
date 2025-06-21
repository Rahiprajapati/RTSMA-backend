from flask import Blueprint, jsonify, request
from database.db import get_db

portfolio_bp = Blueprint("portfolio", __name__)

def get_user_id():
    return "demo_user"

@portfolio_bp.route("/", methods=["GET"])
def get_portfolio():
    try:
        db = get_db()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = db.cursor(dictionary=True)
        user_id = get_user_id()
        
        cursor.execute(
            "SELECT ticker, price, change_percent as `change`, sentiment FROM portfolio WHERE user_id = %s",
            (user_id,)
        )
        portfolio = cursor.fetchall()
        cursor.close()
        
        return jsonify(portfolio)
    except Exception as e:
        print(f"Error fetching portfolio: {e}")
        return jsonify({"error": "Failed to fetch portfolio"}), 500

@portfolio_bp.route("/", methods=["POST"])
def add_to_portfolio():
    try:
        db = get_db()
        if not db:
            return jsonify({"error": "Database connection failed"}), 500
            
        data = request.get_json()
        if not data or not data.get("ticker"):
            return jsonify({"error": "Ticker required"}), 400
            
        cursor = db.cursor()
        user_id = get_user_id()
        
        # Insert or update
        cursor.execute("""
            INSERT INTO portfolio (user_id, ticker, price, change_percent, sentiment)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            price = VALUES(price),
            change_percent = VALUES(change_percent),
            sentiment = VALUES(sentiment)
        """, (user_id, data["ticker"], data.get("price"), data.get("change"), data.get("sentiment")))
        
        db.commit()
        cursor.close()
        
        return jsonify({"message": "Stock added to portfolio successfully"}), 201
        
    except Exception as e:
        print(f"Error adding to portfolio: {e}")
        return jsonify({"error": "Failed to add stock to portfolio"}), 500
