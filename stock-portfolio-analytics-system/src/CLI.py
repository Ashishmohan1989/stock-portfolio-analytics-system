import pandas as pd
from db import get_engine

# Create database connection
engine = get_engine()


def show_users():
    df = pd.read_sql("SELECT * FROM users", engine)
    print("\n===== USERS TABLE =====\n")
    print(df)


def show_stocks():
    df = pd.read_sql("SELECT * FROM stocks", engine)
    print("\n===== STOCKS TABLE =====\n")
    print(df)


def show_trades():
    df = pd.read_sql("SELECT * FROM trades", engine)
    print("\n===== TRADES TABLE =====\n")
    print(df)


def show_holdings():
    df = pd.read_sql("SELECT * FROM holdings", engine)
    print("\n===== HOLDINGS TABLE =====\n")
    print(df)


def show_watchlist():
    df = pd.read_sql("SELECT * FROM watchlist", engine)
    print("\n===== WATCHLIST TABLE =====\n")
    print(df)


def show_performance():
    df = pd.read_sql("SELECT * FROM performance", engine)
    print("\n===== PERFORMANCE TABLE =====\n")
    print(df)


def main_menu():
    while True:
        print("\n===== EQUITY PORTFOLIO MANAGEMENT SYSTEM =====")
        print("1. View Users")
        print("2. View Stocks")
        print("3. View Trades")
        print("4. View Holdings")
        print("5. View Watchlist")
        print("6. View Performance")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_users()
        elif choice == "2":
            show_stocks()
        elif choice == "3":
            show_trades()
        elif choice == "4":
            show_holdings()
        elif choice == "5":
            show_watchlist()
        elif choice == "6":
            show_performance()
        elif choice == "0":
            print("Exiting system. Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()

