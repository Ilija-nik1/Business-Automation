# Keep in mind that this is just the boilerplate code I can share for demonstration of my project. 
# This code has most of the functions of the code I used at my job, just modified to not infringe on my NDA.

import sqlite3
import logging
import sys
import csv
from datetime import datetime

# Configuration
DATABASE_NAME = 'client_database.db'
LOG_FILE_NAME = 'receipt_generator.log'

# Logging configuration
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection function
def connect_to_database():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        logging.error("Error connecting to the database: %s", str(e))
        sys.exit("Error connecting to the database")

# Create clients table if it doesn't exist
def create_clients_table():
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                amount_to_be_paid REAL NOT NULL
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        logging.error("Error creating clients table: %s", str(e))
    finally:
        cursor.close()
        conn.close()

# Validate the name entered by the user
def validate_name(name):
    if not name:
        print("Name cannot be empty.")
        return False
    return True

# Validate the address entered by the user
def validate_address(address):
    if not address:
        print("Address cannot be empty.")
        return False
    return True

# Validate the amount entered by the user
def validate_amount(amount):
    try:
        amount = float(amount)
        if amount <= 0:
            print("Amount must be greater than zero.")
            return False
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return False
    return True

# Retrieve client data from the database based on client_id
def retrieve_client_data(client_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name, address, amount_to_be_paid FROM clients WHERE client_id = ?", (client_id,))
        client_data = cursor.fetchone()

        if client_data:
            return {
                'name': client_data[0],
                'address': client_data[1],
                'amount_to_be_paid': client_data[2]
            }
        else:
            logging.error("Client ID %s not found in the database", client_id)
            return None

    except sqlite3.Error as e:
        logging.error("Error retrieving client data: %s", str(e))
        return None

    finally:
        cursor.close()
        conn.close()

# Generate the receipt using the updated information
def generate_receipt(client_id):
    client_data = retrieve_client_data(client_id)
    if client_data:
        client_name = client_data['name']
        client_address = client_data['address']
        amount_to_be_paid = client_data['amount_to_be_paid']

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receipt = """
        --------------- Receipt ---------------
        Date: {}
        Client Name: {}
        Address: {}
        Amount to be Paid: ${}
        ---------------------------------------
        """.format(timestamp, client_name, client_address, amount_to_be_paid)

        filename = get_receipt_filename(client_id)
        with open(filename, 'w') as receipt_file:
            receipt_file.write(receipt)

        print(receipt)
        logging.info("Receipt generated for client ID %s", client_id)
    else:
        print("Client ID not found in the database.")
        logging.error("Client ID %s not found in the database", client_id)

# Get a unique filename for each receipt
def get_receipt_filename(client_id):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "receipt_{}_{}.txt".format(client_id, timestamp)
    return filename

# Print client data in a formatted manner
def print_client_data(client_data):
    print("---- Client Data ----")
    print("Name: {}".format(client_data['name']))
    print("Address: {}".format(client_data['address']))
    print("Amount to be Paid: {}".format(client_data['amount_to_be_paid']))
    print("---------------------")

# Update Client Data
def update_client_data(client_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        client_data = retrieve_client_data(client_id)
        if client_data:
            print("Current Client Data:")
            print_client_data(client_data)

            print("\nEnter new client data:")
            new_name = input("Name: ")
            new_address = input("Address: ")
            new_amount = input("Amount to be Paid: ")

            if validate_name(new_name) and validate_address(new_address) and validate_amount(new_amount):
                cursor.execute("UPDATE clients SET name = ?, address = ?, amount_to_be_paid = ? WHERE client_id = ?",
                               (new_name, new_address, new_amount, client_id))
                conn.commit()
                print("Client data updated successfully.")
                logging.info("Client data updated for client ID %s", client_id)
        else:
            print("Client ID not found in the database.")
            logging.error("Client ID %s not found in the database", client_id)

    except sqlite3.Error as e:
        logging.error("Error updating client data: %s", str(e))

    finally:
        cursor.close()
        conn.close()

# Add New Client
def add_new_client():
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        new_name = input("Enter client name: ")
        new_address = input("Enter client address: ")
        new_amount = input("Enter amount to be paid: ")

        if validate_name(new_name) and validate_address(new_address) and validate_amount(new_amount):
            cursor.execute("INSERT INTO clients (name, address, amount_to_be_paid) VALUES (?, ?, ?)",
                           (new_name, new_address, new_amount))
            conn.commit()
            print("New client added successfully.")
            logging.info("New client added: %s", new_name)

    except sqlite3.Error as e:
        logging.error("Error adding new client: %s", str(e))

    finally:
        cursor.close()
        conn.close()

# Delete Client
def delete_client(client_id):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        client_data = retrieve_client_data(client_id)
        if client_data:
            print("Client Data:")
            print_client_data(client_data)

            confirm = input("\nAre you sure you want to delete this client? (y/n): ")
            if confirm.lower() == 'y':
                cursor.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
                conn.commit()
                print("Client deleted successfully.")
                logging.info("Client deleted: %s", client_data['name'])
            else:
                print("Deletion canceled.")
        else:
            print("Client ID not found in the database.")
            logging.error("Client ID %s not found in the database", client_id)

    except sqlite3.Error as e:
        logging.error("Error deleting client: %s", str(e))

    finally:
        cursor.close()
        conn.close()

# View All Clients
def view_all_clients():
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM clients")
        all_clients = cursor.fetchall()

        if all_clients:
            print("---- All Clients ----")
            for client in all_clients:
                print("Client ID: {}".format(client[0]))
                print("Name: {}".format(client[1]))
                print("Address: {}".format(client[2]))
                print("Amount to be Paid: {}".format(client[3]))
                print("----------------------")
        else:
            print("No clients found in the database.")

    except sqlite3.Error as e:
        logging.error("Error retrieving clients: %s", str(e))

    finally:
        cursor.close()
        conn.close()

# Search Client by Name
def search_client_by_name(name):
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM clients WHERE name LIKE ?", ('%' + name + '%',))
        matching_clients = cursor.fetchall()

        if matching_clients:
            print("---- Matching Clients ----")
            for client in matching_clients:
                print("Client ID: {}".format(client[0]))
                print("Name: {}".format(client[1]))
                print("Address: {}".format(client[2]))
                print("Amount to be Paid: {}".format(client[3]))
                print("--------------------------")
        else:
            print("No clients found with the given name.")

    except sqlite3.Error as e:
        logging.error("Error searching client by name: %s", str(e))

    finally:
        cursor.close()
        conn.close()

# Export Clients to CSV
def export_clients_to_csv():
    conn = connect_to_database()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM clients")
        all_clients = cursor.fetchall()

        if all_clients:
            filename = input("Enter the CSV file name to save the client data: ")
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Client ID', 'Name', 'Address', 'Amount to be Paid'])
                for client in all_clients:
                    writer.writerow(client)
            print("Client data exported to CSV successfully.")
        else:
            print("No clients found in the database.")

    except sqlite3.Error as e:
        logging.error("Error exporting clients to CSV: %s", str(e))

    finally:
        cursor.close()
        conn.close()

# Main function to generate receipt based on user input
def main():
    while True:
        print("\n------ Receipt Generator Menu ------")
        print("1. Generate Receipt")
        print("2. Update Client Data")
        print("3. Add New Client")
        print("4. Delete Client")
        print("5. View All Clients")
        print("6. Search Client by Name")
        print("7. Export Clients to CSV")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            client_id = input("Enter client ID: ")
            generate_receipt(client_id)

        elif choice == '2':
            client_id = input("Enter client ID: ")
            update_client_data(client_id)

        elif choice == '3':
            add_new_client()

        elif choice == '4':
            client_id = input("Enter client ID: ")
            delete_client(client_id)

        elif choice == '5':
            view_all_clients()

        elif choice == '6':
            name = input("Enter client name: ")
            search_client_by_name(name)

        elif choice == '7':
            export_clients_to_csv()

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a valid option (1-8).")

if __name__ == '__main__':
    create_clients_table()
    main()