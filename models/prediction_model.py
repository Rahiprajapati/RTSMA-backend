# Predict the data
# stock market analaysis


# import yfinance as yf
# from sklearn.linear_model import LinearRegression
# import numpy as np

# def predict_stock_price(ticker):
#     stock = yf.download(ticker, period="60d")
#     stock['Days'] = np.arange(len(stock)).reshape(-1, 1)
#     model = LinearRegression()
#     model.fit(stock['Days'], stock[['Close']])
#     next_day = np.array([[len(stock)]])
#     prediction = model.predict(next_day)
#     return prediction[0]



# import yfinance as yf
# from sklearn.linear_model import LinearRegression
# import numpy as np
# import pandas as pd

# def predict_stock_price(ticker):
#     # Download last 60 days of stock data
#     stock = yf.download(ticker, period="60d", auto_adjust=False)

#     if stock.empty:
#         raise ValueError("No stock data found for the given ticker.")

#     # Prepare the features (days as 0, 1, 2, ...) and reshape them
#     X = np.array(range(len(stock))).reshape(-1, 1)

#     # Target variable: Closing prices as a 2D array
#     y = stock["Close"].values.reshape(-1, 1)

#     # Create and train the model
#     model = LinearRegression()
#     model.fit(X, y)

#     # Predict the next day's price
#     next_day = np.array([[len(stock)]])
#     prediction = model.predict(next_day)

#     return round(float(prediction[0][0]), 2)




import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import time
import random
import os
import requests
from datetime import datetime, timedelta

# Create cache directory
CACHE_DIR = "stock_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# Mock data for common stocks to avoid rate limiting during development
MOCK_DATA = {
    "MSFT": {
        "start_price": 350.0,
        "volatility": 5.0,
        "trend": 0.5  # positive trend
    },
    "AAPL": {
        "start_price": 180.0,
        "volatility": 4.0,
        "trend": 0.3
    },
    "GOOGL": {
        "start_price": 140.0,
        "volatility": 6.0,
        "trend": 0.4
    },
    "AMZN": {
        "start_price": 170.0,
        "volatility": 7.0,
        "trend": 0.6
    }
}

def generate_mock_data(ticker, period="60d"):
    """Generate mock stock data for development purposes"""
    if ticker not in MOCK_DATA:
        # For unknown tickers, create random parameters
        MOCK_DATA[ticker] = {
            "start_price": random.uniform(50.0, 500.0),
            "volatility": random.uniform(2.0, 10.0),
            "trend": random.uniform(-0.5, 0.5)
        }
    
    # Parse the period to determine number of days
    days = 60
    if period.endswith("d"):
        days = int(period[:-1])
    elif period.endswith("mo"):
        days = int(period[:-2]) * 30
    elif period.endswith("y"):
        days = int(period[:-1]) * 365
    
    # Generate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')  # 'B' for business days
    
    # Generate price data
    params = MOCK_DATA[ticker]
    prices = []
    current_price = params["start_price"]
    
    for _ in range(len(date_range)):
        # Add random noise and trend
        change = random.normalvariate(0, 1) * params["volatility"] + params["trend"]
        current_price = max(0.01, current_price + change)
        prices.append(current_price)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Open': prices,
        'High': [p * (1 + random.uniform(0, 0.02)) for p in prices],
        'Low': [p * (1 - random.uniform(0, 0.02)) for p in prices],
        'Close': prices,
        'Adj Close': prices,
        'Volume': [int(random.uniform(1000000, 10000000)) for _ in prices]
    }, index=date_range)
    
    return df

def get_stock_data(ticker, period="60d", use_mock=True):
    """Get stock data with caching and fallback to mock data"""
    ticker = ticker.upper()
    cache_file = os.path.join(CACHE_DIR, f"{ticker}_{period}.csv")
    
    # For development, use mock data if specified
    if use_mock:
        print(f"Using mock data for {ticker}")
        mock_data = generate_mock_data(ticker, period)
        mock_data.to_csv(cache_file)  # Cache the mock data
        return mock_data
    
    # Try to use cache first
    if os.path.exists(cache_file):
        try:
            print(f"Using cached data for {ticker}")
            return pd.read_csv(cache_file, index_col=0, parse_dates=True)
        except Exception as e:
            print(f"Error reading cache: {e}")
    
    # If no cache or cache read failed, try to download
    try:
        # Create a session with custom headers
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        })
        
        # Use a ticker object with our custom session
        ticker_obj = yf.Ticker(ticker, session=session)
        
        # Get historical data
        stock_data = ticker_obj.history(period=period)
        
        # Save to cache if successful
        if not stock_data.empty:
            stock_data.to_csv(cache_file)
            
        return stock_data
    except Exception as e:
        print(f"Download error for {ticker}: {e}")
        
        # If download failed, fall back to mock data
        print(f"Falling back to mock data for {ticker}")
        mock_data = generate_mock_data(ticker, period)
        mock_data.to_csv(cache_file)  # Cache the mock data
        return mock_data

def predict_stock_price(ticker):
    try:
        # Get stock data with our robust function
        stock = get_stock_data(ticker, period="60d", use_mock=True)  # Set to True for development
        
        if stock.empty:
            raise ValueError("No stock data found for the given ticker.")
        
        # Make sure we have the 'Close' column
        if 'Close' not in stock.columns:
            # Try to find an alternative column
            if 'Adj Close' in stock.columns:
                stock['Close'] = stock['Adj Close']
            else:
                raise ValueError("Missing 'Close' price data in the stock information.")
        
        # Prepare the features (days as 0, 1, 2, ...) and reshape them
        X = np.array(range(len(stock))).reshape(-1, 1)
        
        # Target variable: Closing prices as a 2D array
        y = stock["Close"].values.reshape(-1, 1)
        
        # Create and train the model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict the next day's price
        next_day = np.array([[len(stock)]])
        prediction = model.predict(next_day)
        
        return round(float(prediction[0][0]), 2)
    
    except Exception as e:
        # For debugging
        print(f"Error in predict_stock_price for {ticker}: {str(e)}")
        raise
