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

def init_transactions():
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS transactions") 
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("Transactions table initialized successfully.")
    except Exception as e:
        print(f"An error occurred during transactions initialization: {e}")
    finally:
        conn.close()

def get_product_price(name: str):
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT price FROM products WHERE name = ?", (name,))
        result = cursor.fetchone()
        return result[0] if result else 0
    except Exception as e:
        print(f"Error fetching price for {name}: {e}")
        return 0
    finally:
        conn.close()

def insert_transaction(purchase_id: str, product_name: str, price: float, quantity: int):
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO transactions (purchase_id, product_name, price, quantity) VALUES (?, ?, ?, ?)",
            (purchase_id, product_name, price, quantity)
        )
        conn.commit()
    except Exception as e:
        print(f"Error inserting transaction: {e}")
    finally:
        conn.close()

def update_product_stock(name: str, quantity: int):
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE stocks SET stock_count = stock_count - ? WHERE name = ?", (quantity, name))
        conn.commit()
    except Exception as e:
        print(f"Error updating stock for {name}: {e}")
    finally:
        conn.close()


def get_all_stocks():
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT product_id, name, price, stock_count FROM stocks ORDER BY product_id")
        rows = cursor.fetchall()
        return [
            {
                "product_id": row[0],
                "name": row[1],
                "price": row[2],
                "stock_count": row[3],
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error fetching stocks: {e}")
        return []
    finally:
        conn.close()

def add_or_update_product_stock(product_id: int, name: str, price: float, number: int):
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    try:
        # Check by product_id
        cursor.execute("SELECT product_id, name, price, stock_count FROM stocks WHERE product_id = ?", (product_id,))
        prod_by_id = cursor.fetchone()
        
        # Check by name
        cursor.execute("SELECT product_id, name, price, stock_count FROM stocks WHERE name = ?", (name,))
        prod_by_name = cursor.fetchone()
        
        if prod_by_id:
            db_id, db_name, db_price, db_stock = prod_by_id
            
            if db_name.lower() != name.lower():
                return {"success": False, "error": f"Product ID {product_id} exists but with a different name ({db_name})"}
            
            new_count = db_stock + number
            if db_price != price:
                cursor.execute("UPDATE stocks SET stock_count = ?, price = ? WHERE product_id = ?", (new_count, price, product_id))
                cursor.execute("UPDATE products SET price = ? WHERE product_id = ?", (price, product_id))
            else:
                cursor.execute("UPDATE stocks SET stock_count = ? WHERE product_id = ?", (new_count, product_id))
            
            conn.commit()
            return {"success": True, "message": "Existing product stock updated successfully"}
            
        elif prod_by_name:
            db_id = prod_by_name[0]
            return {"success": False, "error": f"Product name '{name}' exists but with a different ID ({db_id})"}
            
        else:
            # Completely new product
            cursor.execute("INSERT INTO products (product_id, name, price) VALUES (?, ?, ?)", (product_id, name, price))
            cursor.execute("INSERT INTO stocks (product_id, name, price, stock_count) VALUES (?, ?, ?, ?)", (product_id, name, price, number))
            conn.commit()
            return {"success": True, "message": "New product added successfully"}
            
    except Exception as e:
        print(f"Error in add_or_update_product_stock: {e}")
        return {"success": False, "error": "Internal server error"}
    finally:
        conn.close()


def get_all_transactions():
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, purchase_id, product_name, price, quantity, created_at
            FROM transactions
            ORDER BY created_at DESC, id DESC
            """
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "purchase_id": row[1],
                "product_name": row[2],
                "price": row[3],
                "quantity": row[4],
                "created_at": row[5],
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return []
    finally:
        conn.close()


def get_recent_transactions(limit: int = 5):
    conn = sqlitecloud.connect(CONNECTION_STRING)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT id, purchase_id, product_name, price, quantity, created_at
            FROM transactions
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "purchase_id": row[1],
                "product_name": row[2],
                "price": row[3],
                "quantity": row[4],
                "created_at": row[5],
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error fetching recent transactions: {e}")
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    # init_db() # Run this once to initialize the database
    # init_stocks()
    # init_transactions()
    # Example usage:
    # print(get_product(100))
    pass
