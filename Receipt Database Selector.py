import sqlite3
from datetime import datetime

# Function to create the database and tables
def create_database():
    conn = sqlite3.connect('ReceiptsDB.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Clients (
                    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_name TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS Receipts (
                    receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER,
                    receipt_date DATE,
                    FOREIGN KEY (client_id) REFERENCES Clients(client_id)
                )''')

    conn.commit()
    conn.close()

# Function to add a new client to the database
def add_client(client_name):
    conn = sqlite3.connect('ReceiptsDB.db')
    c = conn.cursor()

    c.execute("INSERT INTO Clients (client_name) VALUES (?)", (client_name,))
    conn.commit()
    conn.close()

# Function to add a new receipt to the database
def add_receipt(client_id, receipt_date):
    conn = sqlite3.connect('ReceiptsDB.db')
    c = conn.cursor()

    c.execute("INSERT INTO Receipts (client_id, receipt_date) VALUES (?, ?)", (client_id, receipt_date))
    conn.commit()
    conn.close()

# Function to get all receipts for a specific client
def get_receipts_by_client(client_id):
    conn = sqlite3.connect('ReceiptsDB.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Receipts WHERE client_id = ?", (client_id,))
    receipts = c.fetchall()
    conn.close()
    return receipts

# Function to get all receipts in a specific month and year
def get_receipts_by_month_year(month, year):
    conn = sqlite3.connect('ReceiptsDB.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Receipts WHERE strftime('%m', receipt_date) = ? AND strftime('%Y', receipt_date) = ?", (month, year))
    receipts = c.fetchall()
    conn.close()
    return receipts

# Function to delete a receipt by its ID
def delete_receipt(receipt_id):
    conn = sqlite3.connect('ReceiptsDB.db')
    c = conn.cursor()

    c.execute("DELETE FROM Receipts WHERE receipt_id = ?", (receipt_id,))
    conn.commit()
    conn.close()

# Example usage:
if __name__ == "__main__":
    create_database()

    # Adding clients and receipts
    add_client("John Doe")
    add_client("Jane Smith")

    add_receipt(1, '2023-07-02')
    add_receipt(2, '2023-07-10')
    add_receipt(1, '2023-08-15')

    # Querying receipts
    receipts_july_2023 = get_receipts_by_month_year('07', '2023')
    print("Receipts in July 2023:")
    for receipt in receipts_july_2023:
        print(receipt)

    receipts_john_doe = get_receipts_by_client(1)
    print("Receipts for John Doe:")
    for receipt in receipts_john_doe:
        print(receipt)

    # Deleting a receipt
    delete_receipt(1)

    # Printing the remaining receipts
    remaining_receipts = get_receipts_by_client(1)
    print("Remaining Receipts for John Doe:")
    for receipt in remaining_receipts:
        print(receipt)