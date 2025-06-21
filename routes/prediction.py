from flask import Blueprint, jsonify

prediction_bp = Blueprint("prediction", __name__)

@prediction_bp.route("/<ticker>", methods=["GET"])
def get_prediction(ticker):
    dummy_price = 250 + abs(hash(ticker)) % 50  # Use abs to ensure non-negative
    dummy_history = [
        {"date": "2025-06-10", "price": dummy_price - 10},
        {"date": "2025-06-11", "price": dummy_price - 5},
        {"date": "2025-06-12", "price": dummy_price - 2},
        {"date": "2025-06-13", "price": dummy_price - 1},
        {"date": "2025-06-14", "price": dummy_price},
        {"date": "2025-06-15", "price": dummy_price + 3},
        {"date": "2025-06-16", "price": dummy_price + 5}
    ]
    return jsonify({
        "ticker": ticker,
        "predicted_price": dummy_price + 5,
        "history": dummy_history
    })

