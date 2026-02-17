from database.products import init_db, get_product

if __name__ == "__main__":
    # init_db()
    try:
        product = get_product(100)
        print(f"Product fetched: {product}")
    except Exception as e:
        print(f"Error: {e}")
