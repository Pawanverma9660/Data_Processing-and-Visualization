import sqlite3
import os

# Database setup
DB_NAME = 'example.db'

def setup_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)  # Remove existing database

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            join_date DATE NOT NULL
        )
    ''')

    # Create transactions table
    cursor.execute('''
        CREATE TABLE transactions (
            transaction_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            transaction_date DATE,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    # Seed users table
    users = [
        (1, 'Happy', 'happy@example.com', '2024-01-15'),
        (2, 'Ram', 'ram@example.com', '2024-02-20'),
        (3, 'Shyam', 'shyam@example.com', '2024-03-10'),
        (4, 'David', 'david@example.com', '2024-04-25'),
        (5, 'Pawan', 'pawan@example.com', '2024-05-05')
    ]
    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users)

    # Seed transactions table
    transactions = [
        (1, 1, 200.00, '2024-07-01'),
        (2, 2, 150.00, '2024-07-02'),
        (3, 1, 50.00, '2024-07-03'),
        (4, 3, 300.00, '2024-07-04'),
        (5, 4, 20.00, '2024-07-05'),
        (6, 4, 80.00, '2024-07-05'),
        (7, 3, 20.00, '2024-07-05'),
    ]
    cursor.executemany('INSERT INTO transactions VALUES (?, ?, ?, ?)', transactions)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()
    print(f'Database {DB_NAME} created and seeded successfully.')
