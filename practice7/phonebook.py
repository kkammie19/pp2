import os
import csv
from connect import connect


def add_contact():
    name = input("Enter first name: ").strip()
    phone = input("Enter phone number: ").strip()

    if not name or not phone:
        print("Name and phone cannot be empty.")
        return

    connection = connect()
    if connection is None:
        return

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
                    (name, phone)
                )
        print("Contact added!")
    except Exception as error:
        print("Error:", error)
    finally:
        connection.close()


def show_contacts():
    connection = connect()
    if connection is None:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, first_name, phone FROM contacts ORDER BY id"
            )
            contacts = cursor.fetchall()

        if contacts:
            for contact in contacts:
                print(contact)
        else:
            print("PhoneBook is empty.")
    except Exception as error:
        print("Error:", error)
    finally:
        connection.close()


def search_contacts():
    print("1. Search by name")
    print("2. Search by phone prefix")
    choice = input("Choose: ").strip()

    if choice == "1":
        value = input("Enter name: ").strip()
        query = "SELECT id, first_name, phone FROM contacts WHERE first_name ILIKE %s"
        params = (f"%{value}%",)
    elif choice == "2":
        value = input("Enter phone prefix: ").strip()
        query = "SELECT id, first_name, phone FROM contacts WHERE phone LIKE %s"
        params = (f"{value}%",)
    else:
        print("Invalid choice.")
        return

    connection = connect()
    if connection is None:
        return

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()

        for contact in results:
            print(contact)

        if not results:
            print("No contacts found.")
    except Exception as error:
        print("Error:", error)
    finally:
        connection.close()


def update_contact():
    contact_id = input("Enter contact ID: ").strip()
    print("1. Update name")
    print("2. Update phone")
    choice = input("Choose: ").strip()
    value = input("Enter new value: ").strip()

    if not contact_id.isdigit() or not value:
        print("Invalid input.")
        return

    if choice == "1":
        query = "UPDATE contacts SET first_name = %s WHERE id = %s"
    elif choice == "2":
        query = "UPDATE contacts SET phone = %s WHERE id = %s"
    else:
        print("Invalid choice.")
        return

    connection = connect()
    if connection is None:
        return

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (value, int(contact_id)))
                print("Contact updated." if cursor.rowcount else "Contact not found.")
    except Exception as error:
        print("Error:", error)
    finally:
        connection.close()


def delete_contact():
    print("1. Delete by name")
    print("2. Delete by phone")
    choice = input("Choose: ").strip()
    value = input("Enter name or phone: ").strip()

    if choice == "1":
        query = "DELETE FROM contacts WHERE first_name = %s"
    elif choice == "2":
        query = "DELETE FROM contacts WHERE phone = %s"
    else:
        print("Invalid choice.")
        return

    connection = connect()
    if connection is None:
        return

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (value,))
                print(f"Deleted contacts: {cursor.rowcount}")
    except Exception as error:
        print("Error:", error)
    finally:
        connection.close()


def import_csv():
    file_path = os.path.join(os.path.dirname(__file__), "contacts.csv")

    if not os.path.exists(file_path):
        print("contacts.csv not found.")
        return

    connection = connect()
    if connection is None:
        return

    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            with connection:
                with connection.cursor() as cursor:
                    for row in reader:
                        name = row.get("first_name", "").strip()
                        phone = row.get("phone", "").strip()

                        if name and phone:
                            cursor.execute(
                                """
                                INSERT INTO contacts (first_name, phone)
                                VALUES (%s, %s)
                                ON CONFLICT (phone) DO NOTHING
                                """,
                                (name, phone)
                            )

        print("CSV import completed.")
    except Exception as error:
        print("Import error:", error)
    finally:
        connection.close()


def main():
    while True:
        print("\n===== PHONEBOOK =====")
        print("1. Add contact")
        print("2. Show all contacts")
        print("3. Search contacts")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Import contacts from CSV")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            search_contacts()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            import_csv()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
