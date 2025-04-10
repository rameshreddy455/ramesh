import requests
import sqlite3
import os

# Alpha Vantage API key (replace with your own API key)
API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

# SQLite database to store user portfolio
DB_FILE = "portfolio.db"

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect(DB_FILE)
    return conn

# Function to create the database if it doesn't exist
def create_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        quantity INTEGER,
        purchase_price REAL
    )
    """)
    conn.commit()
    conn.close()

# Function to add stock to the portfolio
def add_stock(symbol, quantity, purchase_price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO portfolio (symbol, quantity, purchase_price)
    VALUES (?, ?, ?)
    """, (symbol, quantity, purchase_price))
    conn.commit()
    conn.close()
    print(f"Added {quantity} shares of {symbol} at ${purchase_price} per share.")

# Function to remove stock from the portfolio
def remove_stock(symbol):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM portfolio WHERE symbol = ?
    """, (symbol,))
    conn.commit()
    conn.close()1
    print(f"Removed {symbol} from portfolio.")

# Function to fetch the real-time stock price
def get_stock_price(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        # Fetch the latest price from the Time Series data
        time_series = data["Time Series (5min)"]
        latest_timestamp = list(time_series.keys())[0]
        latest_data = time_series[latest_timestamp]
        current_price = float(latest_data["4. close"])
        return current_price
    except KeyError:
        print(f"Error fetching data for {symbol}. It may be an invalid symbol or API limit reached.")
        return None

# Function to calculate and display portfolio performance
def get_portfolio_performance():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, quantity, purchase_price FROM portfolio")
    stocks = cursor.fetchall()

    total_investment = 0
    total_current_value = 0
    profit_loss = 0

    print("\nPortfolio Performance:")
    for stock in stocks:
        symbol, quantity, purchase_price = stock
        current_price = get_stock_price(symbol)
        if current_price:
            current_value = current_price * quantity
            total_investment += purchase_price * quantity
            total_current_value += current_value
            profit_loss += (current_value - purchase_price * quantity)
            print(f"{symbol} - {quantity} shares - Current Price: ${current_price} - Total Value: ${current_value}")

    print(f"\nTotal Investment: ${total_investment}")
    print(f"Total Current Value: ${total_current_value}")
    print(f"Profit/Loss: ${profit_loss}")

# Main function to interact with the user
def main():
    create_db()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add stock")
        print("2. Remove stock")
        print("3. View portfolio performance")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            symbol = input("Enter the stock symbol (e.g., AAPL, TSLA): ").upper()
            quantity = int(input("Enter the number of shares: "))
            purchase_price = float(input("Enter the purchase price per share: "))
            add_stock(symbol, quantity, purchase_price)
        elif choice == "2":
            symbol = input("Enter the stock symbol to remove: ").upper()
            remove_stock(symbol)
        elif choice == "3":
            get_portfolio_performance()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
