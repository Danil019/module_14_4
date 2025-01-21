import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    Id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    connection.commit()

def add_products():
    for i in range(4):
        products_names = ['Яблоко', 'Авокадо', 'Яйцо', 'Апельсин']
        cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (f"{products_names[i]}", f"{products_names[i]}", (i + 1) * 100))
    connection.commit()

def get_all_products():
    cursor.execute(f"SELECT title, description, price FROM Products")
    return cursor.fetchall()

print(get_all_products())