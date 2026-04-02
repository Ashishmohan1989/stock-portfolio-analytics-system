import pandas as pd
from datetime import date
from db import get_engine

# get database connection
engine = get_engine()

# -----------------------------
# USERS DATA (Python generated)
# -----------------------------
users_df = pd.DataFrame({
    "full_name": [
        "Ashish Mohan",
        "Rahul Sharma",
        "Neha Verma",
        "Amit Patel",
        "Sneha Iyer",
        "Rohit Mehta",
        "Pooja Nair",
        "Kunal Singh",
        "Ananya Gupta",
        "Vikram Rao"
    ],
    "email": [
        "ashish@rediff.com",
        "rahul@gmail.com",
        "neha@gmail.com",
        "amit@yahoo.com",
        "sneha@gmail.com",
        "rohit@hotmail.com",
        "pooja@outlook.com",
        "kunal@gmail.com",
        "ananya@gmail.com",
        "vikram@yahoo.com"
    ],
    "mobile": [
        "9876543210",
        "9123456789",
        "9988776655",
        "9090909090",
        "9898989898",
        "9000011111",
        "9000022222",
        "9000033333",
        "9000044444",
        "9000055555"
    ],
    "pan_no": [
        "ABCDE1234F",
        "PQRSX5678Y",
        "LMNOP4321Q",
        "ZXCVB6789K",
        "QWERT9876P",
        "ASDFG3456L",
        "HJKLO9988M",
        "BNMQW1122R",
        "PLMKO5566T",
        "UIOPL7788S"
    ],
    "kyc_status": [
        "Verified",
        "Verified",
        "Pending",
        "Verified",
        "Pending",
        "Verified",
        "Pending",
        "Verified",
        "Verified",
        "Pending"
    ],
    "registration_date": [date.today()] * 10
})

# insert into MySQL
users_df.to_sql(
    name="users",
    con=engine,
    if_exists="append",
    index=False
)

print("Users data inserted successfully")


import pandas as pd
from db import get_engine

# Create database connection
engine = get_engine()


# STOCKS DATA --from Screener and Groww


# Read Excel file
stocks_df = pd.read_excel("data/stocks.xlsx")

# Print original column names (for verification)
print("Original Columns:", stocks_df.columns)

# Rename Excel columns to match MySQL table schema
stocks_df = stocks_df.rename(columns={
    "Symbol": "symbol",
    "Company Name": "company_name",
    "Sector": "sector",
    "Exchange": "exchange",
    "Market Cap in Cr.": "mkt_cap"
})

# Keep only required columns
stocks_df = stocks_df[
    ["symbol", "company_name", "sector", "exchange", "mkt_cap"]
]

# Remove rows with missing stock symbols
stocks_df = stocks_df.dropna(subset=["symbol"])

# Remove duplicate stocks (based on symbol)
stocks_df = stocks_df.drop_duplicates(subset=["symbol"])

# Insert data into MySQL stocks table
stocks_df.to_sql(
    name="stocks",
    con=engine,
    if_exists="append",
    index=False
)

print("Stocks data inserted successfully")




import pandas as pd
import random
from db import get_engine

# Create database connection

engine = get_engine()

# FETCH STOCK IDS FROM DATABASE

stocks_df = pd.read_sql("SELECT stock_id FROM stocks", engine)

# GENERATE PERFORMANCE DATA

performance_data = []

for _, row in stocks_df.iterrows():
    base_price = random.uniform(500, 3000)

    todays_low = round(base_price * random.uniform(0.95, 0.98), 2)
    todays_high = round(base_price * random.uniform(1.02, 1.05), 2)

    week_52_low = round(base_price * random.uniform(0.70, 0.85), 2)
    week_52_high = round(base_price * random.uniform(1.20, 1.50), 2)

    volume = random.randint(100000, 5000000)

    performance_data.append([
        row["stock_id"],
        todays_high,
        todays_low,
        week_52_high,
        week_52_low,
        volume
    ])

# CREATE DATAFRAME

performance_df = pd.DataFrame(
    performance_data,
    columns=[
        "stock_id",
        "Todays_High",
        "Todays_Low",
        "Week_High_52",
        "Week_Low_52",
        "volume"
    ]
)


# INSERT INTO MYSQL

performance_df.to_sql(
    name="performance",
    con=engine,
    if_exists="append",
    index=False
)

print("Performance data inserted successfully")




import pandas as pd
import random
from datetime import date, timedelta
from db import get_engine

# Create database connection
engine = get_engine()

# FETCH USER IDS AND STOCK IDS
users_df = pd.read_sql("SELECT user_id FROM users", engine)
stocks_df = pd.read_sql("SELECT stock_id FROM stocks", engine)


# GENERATE TRADES DATA

trades_data = []

for _ in range(50):  # generate 50 trades
    user_id = random.choice(users_df["user_id"].tolist())
    stock_id = random.choice(stocks_df["stock_id"].tolist())

    trade_type = random.choice(["BUY", "SELL"])
    quantity = random.randint(1, 100)

    trade_price = round(random.uniform(500, 3000), 2)
    trade_date = date.today() - timedelta(days=random.randint(0, 30))

    trades_data.append([
        user_id,
        stock_id,
        trade_type,
        quantity,
        trade_price,
        trade_date
    ])

# CREATE DATAFRAME

trades_df = pd.DataFrame(
    trades_data,
    columns=[
        "user_id",
        "stock_id",
        "trade_type",
        "quantity",
        "trade_price",
        "trade_date"
    ]
)


# INSERT INTO MYSQL

trades_df.to_sql(
    name="trades",
    con=engine,
    if_exists="append",
    index=False
)

print("Trades data inserted successfully")





import pandas as pd
from datetime import date
from db import get_engine

# Create database connection
engine = get_engine()

# FETCH TRADES DATA
trades_df = pd.read_sql(
    "SELECT user_id, stock_id, trade_type, quantity, trade_price FROM trades",
    engine
)


# PROCESS BUY TRADES
buy_trades = trades_df[trades_df["trade_type"] == "BUY"]

# Calculate total quantity bought
buy_summary = buy_trades.groupby(
    ["user_id", "stock_id"]
).agg(
    total_qty=("quantity", "sum"),
    total_value=("trade_price", lambda x: (x * buy_trades.loc[x.index, "quantity"]).sum())
).reset_index()

# Calculate average buy price
buy_summary["avg_buy_price"] = buy_summary["total_value"] / buy_summary["total_qty"]

# PROCESS SELL TRADES

sell_trades = trades_df[trades_df["trade_type"] == "SELL"]

sell_summary = sell_trades.groupby(
    ["user_id", "stock_id"]
).agg(
    sold_qty=("quantity", "sum")
).reset_index()


# MERGE BUY AND SELL DATA

holdings_df = pd.merge(
    buy_summary,
    sell_summary,
    on=["user_id", "stock_id"],
    how="left"
)

holdings_df["sold_qty"] = holdings_df["sold_qty"].fillna(0)

# Calculate quantity held
holdings_df["quantity_held"] = holdings_df["total_qty"] - holdings_df["sold_qty"]

# Remove zero or negative holdings
holdings_df = holdings_df[holdings_df["quantity_held"] > 0]

# FINAL HOLDINGS DATA

holdings_df["last_updated"] = date.today()

final_holdings = holdings_df[[
    "user_id",
    "stock_id",
    "quantity_held",
    "avg_buy_price",
    "last_updated"
]]


# INSERT INTO MYSQL
final_holdings.to_sql(
    name="holdings",
    con=engine,
    if_exists="append",
    index=False
)

print("Holdings data derived and inserted successfully")







import pandas as pd
import random
from datetime import date
from db import get_engine


# Database connection

engine = get_engine()


# Fetch users and stocks

users_df = pd.read_sql("SELECT user_id FROM users", engine)
stocks_df = pd.read_sql("SELECT stock_id, sector FROM stocks", engine)


# Generate watchlist data

watchlist_data = []

for _ in range(20):   # create 20 watchlist entries
    user_id = random.choice(users_df["user_id"].tolist())
    stock_row = stocks_df.sample(1).iloc[0]

    stock_id = stock_row["stock_id"]
    sector = stock_row["sector"]
    added_date = date.today()

    watchlist_data.append([
        user_id,
        stock_id,
        sector,
        added_date
    ])

# Create DataFrame

watchlist_df = pd.DataFrame(
    watchlist_data,
    columns=[
        "user_id",
        "stock_id",
        "sector",
        "added_date"
    ]
)

# -------------------------------------------------
# Insert into MySQL
# -------------------------------------------------
watchlist_df.to_sql(
    name="watchlist",
    con=engine,
    if_exists="append",
    index=False
)

print("Watchlist data inserted successfully")






