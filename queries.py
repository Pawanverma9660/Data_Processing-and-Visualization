import sqlite3
import pandas as pd

DB_NAME = 'example.db'

def query_users_by_date_range(start_date, end_date):
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT * FROM users WHERE join_date BETWEEN ? AND ?
    '''
    users = pd.read_sql(query, conn, params=(start_date, end_date))
    conn.close()
    return users

def calculate_total_spent_by_user():
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT u.name, u.email, SUM(t.amount) AS total_spent
        FROM users u
        JOIN transactions t ON u.user_id = t.user_id
        GROUP BY u.user_id
    '''
    total_spent = pd.read_sql(query, conn)
    conn.close()
    return total_spent

def top_3_users():
    total_spent = calculate_total_spent_by_user()
    return total_spent.nlargest(3, 'total_spent')

def average_transaction_amount():
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT AVG(amount) AS avg_transaction
        FROM transactions
    '''
    avg_transaction = pd.read_sql(query, conn).iloc[0]['avg_transaction']
    conn.close()
    return avg_transaction

def users_with_no_transactions():
    conn = sqlite3.connect(DB_NAME)
    query = '''
        SELECT u.user_id, u.name, u.email, u.join_date
        FROM users u
        LEFT JOIN transactions t ON u.user_id = t.user_id
        WHERE t.transaction_id IS NULL
    '''
    users_no_transactions = pd.read_sql(query, conn)
    conn.close()
    return users_no_transactions

if __name__ == '__main__':
    print("Users joined between 2024-01-01 and 2024-03-31:")
    print(query_users_by_date_range('2024-01-01', '2024-03-31'))
    print("\nTotal spent by each user:")
    print(calculate_total_spent_by_user())
    print("\nTop 3 users by total spent:")
    print(top_3_users())
    print("\nTotal Average transaction amount:")
    print(average_transaction_amount())
    print("\nUsers with no transactions:")
    print(users_with_no_transactions())
