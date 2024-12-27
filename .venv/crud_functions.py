import sqlite3

connection = sqlite3.connect("database_health.db", timeout=10)
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
    )
    ''')
    connection.commit()

def filling_data():
    for i in range(1, 5):
        cursor.execute('INSERT INTO Products (id, title, description, price) VALUES(?, ?, ?, ?)',
                       (i, f'Продукт{i}', f'описание {i}', i * 100))
    connection.commit()

def killing_data():
    cursor.execute('DROP TABLE Products')
    connection.commit()


def get_all_products():
    cursor.execute("SELECT * FROM Products")
    get_prod = cursor.fetchall()
    return get_prod

def add_user(username, email, age):
    cursor.execute("INSERT INTO Users (username, email, age, balance ) VALUES (?, ?, ?, ?)", (username, email, age, 1000))
    connection.commit()

def is_included(username):
    check_user = cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    if check_user.fetchone() is not None:
        return True
    connection.commit()
    return False

if __name__ == '__main__':
    initiate_db()
    filling_data()
#    killing_data()
    print(get_all_products())
    connection.close()

