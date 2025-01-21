import sqlite3

DB_NAME = 'database.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def initiate_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products(
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                price INTEGER NOT NULL
            )
        ''')
        conn.commit()

def add_products():
    with get_connection() as conn:
        cursor = conn.cursor()
        for i in range(4):
            products_names = ['Яблоко', 'Авокадо', 'Яйцо', 'Апельсин']
            cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (f"{products_names[i]}", f"{products_names[i]}", (i + 1) * 100))
        conn.commit()

def get_all_products():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, description, price FROM Products")
        return cursor.fetchall()

print(get_all_products())