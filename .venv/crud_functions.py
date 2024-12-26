import sqlite3

connection = sqlite3.connect("database.db", timeout=10)
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

if __name__ == '__main__':
#    initiate_db()
#    filling_data()
#    killing_data()
#    print(get_all_products())
    connection.close()

