import sqlitecloud
from dotenv import load_dotenv
import os
import random

load_dotenv()

CONNECTION_STRING = os.getenv("SQLITECLOUD_CONNECTION_STRING")
def init_db():
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE products;
                   
    """)
    # Create table if not exists with correct column names
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    # Populate with household objects (IDs 100-109)
    products = [
        (100, "Marie Gold", 10,),
        (101, "Cinthol", 70),
        (102, "Gloves", 200),
        (103, "Coco Cola", 40),
        (104, "Elite Brownie",20 ),
        (105, "Coconut Oil", 30),
        (106, "Shampoo", 100),
        (107, "Pen", 5 ),
        (108, "Note Book", 50),
        (109, "Water Bottle", 20)
    ]

    try:
        cursor.executemany("INSERT OR REPLACE INTO products (product_id, name, price) VALUES (?, ?, ?)", products)
        conn.commit()
        print("Database initialized and products inserted successfully.")
    except Exception as e:
        print(f"An error occurred during initialization: {e}")
    finally:
        conn.close()

def init_stocks():
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    
    try:
        cursor.execute("DROP TABLE IF EXISTS stocks")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stocks (
                product_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock_count INTEGER NOT NULL
            )
        """)

        products = [
            (100, "Marie Gold", 10),
            (101, "Cinthol", 70),
            (102, "Gloves", 200),
            (103, "Coco Cola", 40),
            (104, "Elite Brownie", 20),
            (105, "Coconut Oil", 30),
            (106, "Shampoo", 100),
            (107, "Pen", 5),
            (108, "Note Book", 50),
            (109, "Water Bottle", 20)
        ]

        stock_data = []
        for product in products:
            p_id, name, price = product
            stock = random.randint(20, 40)
            stock_data.append((p_id, name, price, stock))

        cursor.executemany("INSERT OR REPLACE INTO stocks (product_id, name, price, stock_count) VALUES (?, ?, ?, ?)", stock_data)
        conn.commit()
        print("Stocks table initialized successfully.")
    except Exception as e:
        print(f"An error occurred during stocks initialization: {e}")
    finally:
        conn.close()

def get_product(product_id: int):
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name, price FROM products WHERE product_id = ?", (product_id,))
        result = cursor.fetchone()
        
        if result:
            return {"name": result[0], "price": result[1]}
        else:
            return None
    except Exception as e:
        print(f"Error fetching product: {e}")
        return None
    finally:
        conn.close()

if __name__ == "__main__":
    # init_db() # Run this once to initialize the database
    init_stocks()
    # Example usage:
    # print(get_product(100))
    pass
