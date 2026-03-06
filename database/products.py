import sqlitecloud
from dotenv import load_dotenv
import os
load_dotenv()

CONNECTION_STRING = os.getenv("SQLITECLOUD_CONNECTION_STRING")
def init_db():
    try:
        conn = sqlitecloud.connect(CONNECTION_STRING)
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return

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
    init_db() # Run this once to initialize the database
    # Example usage:
    # print(get_product(100))
    pass
