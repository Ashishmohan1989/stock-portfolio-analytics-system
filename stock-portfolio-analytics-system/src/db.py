from sqlalchemy import create_engine
from sqlalchemy.engine import URL

DB_USER = "root"
DB_PASSWORD = "Ashishmohan@1234"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "mca_project"

connection_url = URL.create(
    drivername="mysql+mysqlconnector",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(connection_url)

def get_engine():
    return engine

if __name__ == "__main__":
    conn = engine.connect()
    print("Database connection successful")
    conn.close()
