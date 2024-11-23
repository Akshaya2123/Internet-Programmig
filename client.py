# client.py

import requests

SERVER_URL = 'http://127.0.0.1:5000'

def admin_login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    response = requests.post(f"{SERVER_URL}/admin_login", json={'username': username, 'password': password})
    if response.status_code == 200:
        print(response.json()['message'])
        return username, password
    else:
        print(f"Error: {response.json().get('message', 'Unauthorized')}")
        return None, None

def add_record(admin_credentials):
    username, password = admin_credentials
    data = {
        'username': username,
        'password': password,
        'name': input("Enter item name: "),
        'category': input("Enter item category: "),
        'quantity': int(input("Enter item quantity: "))
    }
    response = requests.post(f"{SERVER_URL}/add_record", json=data)
    print(response.json()['message'])

def view_records():
    response = requests.get(f"{SERVER_URL}/view_records")
    records = response.json()
    for record in records:
        print(record)

def update_record(admin_credentials):
    username, password = admin_credentials
    data = {
        'username': username,
        'password': password,
        'name': input("Enter the item name to update: "),
        'quantity': int(input("Enter new quantity: "))
    }
    response = requests.put(f"{SERVER_URL}/update_record", json=data)
    print(response.json()['message'])

def delete_record(admin_credentials):
    username, password = admin_credentials
    data = {
        'username': username,
        'password': password,
        'name': input("Enter the item name to delete: ")
    }
    response = requests.delete(f"{SERVER_URL}/delete_record", json=data)
    print(response.json()['message'])

def user_menu():
    while True:
        print("\nUser Menu")
        print("1. View Items")
        print("2. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_records()
        elif choice == '2':
            print("Exiting user menu...")
            break
        else:
            print("Invalid choice, please try again.")

def admin_menu(admin_credentials):
    while True:
        print("\nAdmin Menu")
        print("1. Add Record")
        print("2. Update Record")
        print("3. Delete Record")
        print("4. View Items")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_record(admin_credentials)
        elif choice == '2':
            update_record(admin_credentials)
        elif choice == '3':
            delete_record(admin_credentials)
        elif choice == '4':
            view_records()
        elif choice == '5':
            print("Exiting admin menu...")
            break
        else:
            print("Invalid choice, please try again.")

def main_menu():
    while True:
        print("\nERP System")
        print("1. Login as Admin")
        print("2. Continue as User")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            admin_credentials = admin_login()
            if admin_credentials[0]:
                admin_menu(admin_credentials)
        elif choice == '2':
            user_menu()
        elif choice == '3':
            print("Exiting the system...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main_menu()
