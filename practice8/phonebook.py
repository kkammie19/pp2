from connect import connect


def search_contacts():
    pattern = input("Enter name or phone to search: ")

    connection = connect()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM search_contacts_by_pattern(%s)",
            (pattern,)
        )

        contacts = cursor.fetchall()

        if contacts:
            print("\nContacts found:")
            for contact in contacts:
                print(contact)
        else:
            print("No contacts found.")

        cursor.close()

    except Exception as error:
        print("Error:", error)

    finally:
        connection.close()


def upsert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    connection = connect()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        cursor.execute(
            "CALL upsert_contact(%s, %s)",
            (name, phone)
        )

        connection.commit()
        cursor.close()

        print("Contact added or updated successfully.")

    except Exception as error:
        print("Error:", error)

    finally:
        connection.close()


def insert_many_contacts():
    names_input = input("Enter names separated by commas: ")
    phones_input = input("Enter phones separated by commas: ")

    names = [name.strip() for name in names_input.split(",")]
    phones = [phone.strip() for phone in phones_input.split(",")]

    if len(names) != len(phones):
        print("The number of names and phones must be the same.")
        return

    connection = connect()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        cursor.execute(
            "CALL insert_many_contacts(%s, %s, %s)",
            (names, phones, [])
        )

        incorrect_data = cursor.fetchone()

        connection.commit()
        cursor.close()

        print("Contacts processed successfully.")

        if incorrect_data:
            print("Incorrect data:", incorrect_data)

    except Exception as error:
        print("Error:", error)

    finally:
        connection.close()


def show_paginated_contacts():
    try:
        limit = int(input("How many contacts do you want to see? "))
        offset = int(input("How many contacts should be skipped? "))
    except ValueError:
        print("Please enter numbers only.")
        return

    connection = connect()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (limit, offset)
        )

        contacts = cursor.fetchall()

        if contacts:
            print("\nContacts:")
            for contact in contacts:
                print(contact)
        else:
            print("No contacts found.")

        cursor.close()

    except Exception as error:
        print("Error:", error)

    finally:
        connection.close()


def delete_contact():
    value = input("Enter name or phone to delete: ")

    connection = connect()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        cursor.execute(
            "CALL delete_contact(%s)",
            (value,)
        )

        connection.commit()
        cursor.close()

        print("Contact deleted successfully.")

    except Exception as error:
        print("Error:", error)

    finally:
        connection.close()


def main():
    while True:
        print("\n--- PhoneBook Practice 8 ---")
        print("1. Search contacts by pattern")
        print("2. Add or update contact")
        print("3. Insert many contacts")
        print("4. Show contacts with pagination")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            search_contacts()

        elif choice == "2":
            upsert_contact()

        elif choice == "3":
            insert_many_contacts()

        elif choice == "4":
            show_paginated_contacts()

        elif choice == "5":
            delete_contact()

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()