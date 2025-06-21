# # fetch the history of a stock

# from flask import Blueprint, request, jsonify
# from models.prediction_model import predict_stock_price
# from models.sentiment_analysis import analyze_sentiment

# stock_bp = Blueprint("stock", __name__)

# @stock_bp.route("/predict/<ticker>", methods=["GET"])
# def predict(ticker):
#     try:
#         price = predict_stock_price(ticker)
#         return jsonify({"ticker": ticker, "predicted_price": price})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @stock_bp.route("/sentiment", methods=["POST"])
# def sentiment():
#     data = request.get_json()
#     text = data.get("text", "")
#     result = analyze_sentiment(text)
#     return jsonify({"sentiment": result})


# # GOOGL: Alphabet Inc. (Google)

# # AMZN: Amazon

# # MSFT: Microsoft



# fetch the history of a stock

from flask import Blueprint, request, jsonify
from models.prediction_model import predict_stock_price
from models.sentiment_analysis import analyze_sentiment
import time

stock_bp = Blueprint("stock", __name__)

# Keep track of recent requests to implement our own rate limiting
recent_requests = {}

@stock_bp.route("/predict/<ticker>", methods=["GET"])
def predict(ticker):
    # Convert ticker to uppercase
    ticker = ticker.upper()
    
    # Simple rate limiting to avoid hitting Yahoo's limits
    current_time = time.time()
    if ticker in recent_requests:
        time_since_last_request = current_time - recent_requests[ticker]
        if time_since_last_request < 5:  # 5 seconds between requests for the same ticker
            return jsonify({
                "error": "Too many requests for this ticker",
                "message": f"Please wait {5 - time_since_last_request:.1f} seconds before trying again"
            }), 429
    
    # Update the last request time
    recent_requests[ticker] = current_time
    
    try:
        price = predict_stock_price(ticker)
        return jsonify({"ticker": ticker, "predicted_price": price})
    except Exception as e:
        error_message = str(e)
        if "Rate limited" in error_message:
            return jsonify({
                "error": "Yahoo Finance rate limit reached",
                "message": "The service is temporarily unavailable due to rate limiting. Please try again later."
            }), 503
        else:
            return jsonify({"error": error_message}), 500

@stock_bp.route("/sentiment", methods=["POST"])
def sentiment():
    data = request.get_json()
    text = data.get("text", "")
    result = analyze_sentiment(text)
    return jsonify({"sentiment": result})


