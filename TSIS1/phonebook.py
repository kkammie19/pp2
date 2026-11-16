import json
import csv 
import os
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
    print("\n--- Paginated Contacts ---")

    try:
        limit = int(input("Contacts per page: "))

        if limit <= 0:
            print("Please enter a positive number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    connection = connect()

    if connection is None:
        return

    cursor = connection.cursor()

    page = 0

    try:
        while True:
            offset = page * limit

            cursor.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s)",
                (limit, offset)
            )

            contacts = cursor.fetchall()

            print(f"\n--- Page {page + 1} ---")

            if contacts:
                for contact in contacts:
                    print(
                        f"ID: {contact[0]} | "
                        f"Name: {contact[1]} | "
                        f"Phone: {contact[2]}"
                    )
            else:
                print("No contacts on this page.")

            print("\nCommands: next / prev / quit")

            command = input("Enter command: ").strip().lower()

            if command == "next":
                if len(contacts) < limit:
                    print("This is the last page.")
                else:
                    page += 1

            elif command == "prev":
                if page > 0:
                    page -= 1
                else:
                    print("You are already on the first page.")

            elif command == "quit":
                print("Returning to main menu.")
                break

            else:
                print("Invalid command.")

    except Exception as error:
        print("Error:", error)

    finally:
        cursor.close()
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


def filter_sort_contacts():
    print("\n--- Filter and Sort Contacts ---")

    group_name = input(
        "Enter group (Family/Work/Friend/Other) "
        "or press Enter for all: "
    ).strip()

    email_query = input(
        "Enter email search or press Enter to skip: "
    ).strip()

    print("\nSort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    sort_choice = input("Choose sorting option: ")

    sort_options = {
        "1": "c.first_name ASC",
        "2": "c.birthday ASC NULLS LAST",
        "3": "c.created_at DESC"
    }

    if sort_choice not in sort_options:
        print("Invalid sorting option.")
        return

    connection = connect()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                c.id,
                c.first_name,
                c.email,
                c.birthday,
                g.name AS group_name,
                COALESCE(
                    STRING_AGG(
                        p.phone || ' (' || p.type || ')',
                        ', '
                    ),
                    'No phones'
                ) AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE
                (%s = '' OR g.name ILIKE %s)
                AND
                (%s = '' OR c.email ILIKE %s)
            GROUP BY c.id, g.name
            ORDER BY """ + sort_options[sort_choice]

        cursor.execute(
            query,
            (
                group_name,
                group_name,
                email_query,
                f"%{email_query}%"
            )
        )

        contacts = cursor.fetchall()

        if contacts:
            print("\nFiltered contacts:")

            for contact in contacts:
                print("\n--------------------")
                print("ID:", contact[0])
                print("Name:", contact[1])
                print("Email:", contact[2])
                print("Birthday:", contact[3])
                print("Group:", contact[4])
                print("Phones:", contact[5])
        else:
            print("No contacts found.")

        cursor.close()

    except Exception as error:
        print("Error:", error)

    finally:
        connection.close()


def export_contacts_json():
    print("\n--- Export Contacts to JSON ---")

    filename = input(
        "Enter JSON filename (default: contacts.json): "
    ).strip()

    if not filename:
        filename = "contacts.json"

    if not filename.lower().endswith(".json"):
        filename += ".json"

    connection = connect()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                c.id,
                c.first_name,
                c.email,
                c.birthday,
                g.name,
                c.created_at
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
        """)

        contacts = cursor.fetchall()

        export_data = []

        for contact in contacts:
            contact_id = contact[0]

            cursor.execute("""
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s
                ORDER BY id
            """, (contact_id,))

            phones = cursor.fetchall()

            contact_data = {
                "name": contact[1],
                "email": contact[2],
                "birthday": (
                    contact[3].isoformat()
                    if contact[3] else None
                ),
                "group": contact[4],
                "created_at": (
                    contact[5].isoformat()
                    if contact[5] else None
                ),
                "phones": [
                    {
                        "phone": phone[0],
                        "type": phone[1]
                    }
                    for phone in phones
                ]
            }

            export_data.append(contact_data)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                export_data,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Successfully exported {len(export_data)} contacts "
            f"to {filename}."
        )

        cursor.close()

    except Exception as error:
        print("Export error:", error)

    finally:
        connection.close()


def import_contacts_json():
    print("\n--- Import Contacts from JSON ---")

    filename = input("Enter JSON filename: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            contacts_data = json.load(file)

        if not isinstance(contacts_data, list):
            print("JSON must contain a list of contacts.")
            return

    except FileNotFoundError:
        print("File not found.")
        return

    except json.JSONDecodeError:
        print("Invalid JSON file.")
        return

    connection = connect()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        imported = 0
        skipped = 0

        for contact in contacts_data:

            name = contact.get("name")
            email = contact.get("email")
            birthday = contact.get("birthday")
            group_name = contact.get("group") or "Other"
            phones = contact.get("phones", [])

            if not isinstance(name, str) or not name.strip():
                print("Invalid contact name. Skipping.")
                skipped += 1
                continue

            if not isinstance(phones, list):
                print(f"Invalid phones for {name}. Skipping.")
                skipped += 1
                continue

            valid_phones = True

            for phone_data in phones:
                if not isinstance(phone_data, dict):
                    valid_phones = False
                    break

                phone = phone_data.get("phone")
                phone_type = phone_data.get("type")

                if (
                    not isinstance(phone, str)
                    or not phone.strip()
                    or phone_type not in ("home", "work", "mobile")
                ):
                    valid_phones = False
                    break

            if not valid_phones:
                print(f"Invalid phone data for {name}. Skipping.")
                skipped += 1
                continue

            try:
                cursor.execute("""
                    SELECT id
                    FROM contacts
                    WHERE first_name = %s
                """, (name.strip(),))

                existing = cursor.fetchall()

                if existing:
                    action = input(
                        f"{name} already exists. "
                        "Choose skip or overwrite: "
                    ).strip().lower()

                    if action == "skip":
                        skipped += 1
                        continue

                    elif action != "overwrite":
                        print("Invalid choice. Contact skipped.")
                        skipped += 1
                        continue

                    if len(existing) > 1:
                        print(
                            f"Multiple contacts named {name}. "
                            "Cannot safely overwrite."
                        )
                        skipped += 1
                        continue

                    contact_id = existing[0][0]

                else:
                    contact_id = None

                # Create group if it does not exist
                cursor.execute("""
                    INSERT INTO groups (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                """, (group_name,))

                cursor.execute("""
                    SELECT id FROM groups
                    WHERE name = %s
                """, (group_name,))

                group_id = cursor.fetchone()[0]

                # First phone is also saved in the old phone field
                # for Practice 7-8 compatibility.
                legacy_phone = (
                    phones[0]["phone"] if phones else None
                )

                if contact_id is not None:

                    # Update existing contact
                    cursor.execute("""
                        UPDATE contacts
                        SET
                            email = %s,
                            birthday = %s,
                            group_id = %s,
                            phone = %s
                        WHERE id = %s
                    """, (
                        email,
                        birthday,
                        group_id,
                        legacy_phone,
                        contact_id
                    ))

                    # Replace old phone numbers
                    cursor.execute("""
                        DELETE FROM phones
                        WHERE contact_id = %s
                    """, (contact_id,))

                else:

                    # Insert new contact
                    cursor.execute("""
                        INSERT INTO contacts (
                            first_name,
                            phone,
                            email,
                            birthday,
                            group_id
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        name.strip(),
                        legacy_phone,
                        email,
                        birthday,
                        group_id
                    ))

                    contact_id = cursor.fetchone()[0]

                # Insert all phone numbers
                for phone_data in phones:
                    cursor.execute("""
                        INSERT INTO phones (
                            contact_id,
                            phone,
                            type
                        )
                        VALUES (%s, %s, %s)
                    """, (
                        contact_id,
                        phone_data["phone"],
                        phone_data["type"]
                    ))

                connection.commit()
                imported += 1

                print(f"Imported: {name}")

            except Exception as error:
                connection.rollback()
                skipped += 1
                print(f"Error importing {name}: {error}")

        print("\n--- Import Summary ---")
        print("Imported:", imported)
        print("Skipped:", skipped)

        cursor.close()

    except Exception as error:
        connection.rollback()
        print("Import error:", error)

    finally:
        connection.close()


def import_contacts_csv():
    print("\n--- Import Contacts from CSV ---")

    filename = input(
        "Enter CSV filename (default: contacts.csv): "
    ).strip()

    if not filename:
        filename = "contacts.csv"

    required_columns = {
        "name",
        "email",
        "birthday",
        "group",
        "phone",
        "phone_type"
    }

    
    try:
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            filename
        )

        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames or not required_columns.issubset(
                set(reader.fieldnames)
            ):
                print("CSV file has missing columns.")
                return

            rows = list(reader)

    except FileNotFoundError:
        print("CSV file not found.")
        return

    connection = connect()

    if connection is None:
        return

    imported = 0
    skipped = 0

    try:
        cursor = connection.cursor()

        for row in rows:
            try:
                name = (row["name"] or "").strip()
                email = (row["email"] or "").strip() or None
                birthday = (row["birthday"] or "").strip() or None
                group_name = (row["group"] or "").strip() or "Other"
                phone = (row["phone"] or "").strip()
                phone_type = (row["phone_type"] or "").strip().lower()

                if not name or not phone:
                    print("Missing name or phone. Skipping row.")
                    skipped += 1
                    continue

                if phone_type not in ("home", "work", "mobile"):
                    print(f"Invalid phone type for {name}. Skipping.")
                    skipped += 1
                    continue

                if birthday:
                    from datetime import date
                    date.fromisoformat(birthday)

                # Find existing contact
                cursor.execute("""
                    SELECT id
                    FROM contacts
                    WHERE first_name = %s
                """, (name,))

                existing = cursor.fetchall()

                if len(existing) > 1:
                    print(f"Duplicate contact name: {name}. Skipping.")
                    skipped += 1
                    continue

                # Create group if needed
                cursor.execute("""
                    INSERT INTO groups (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                """, (group_name,))

                cursor.execute("""
                    SELECT id
                    FROM groups
                    WHERE name = %s
                """, (group_name,))

                group_id = cursor.fetchone()[0]

                if existing:
                    contact_id = existing[0][0]

                    cursor.execute("""
                        UPDATE contacts
                        SET
                            email = COALESCE(%s, email),
                            birthday = COALESCE(%s, birthday),
                            group_id = %s,
                            phone = CASE
                                WHEN phone IS NULL OR phone = ''
                                THEN %s
                                ELSE phone
                            END
                        WHERE id = %s
                    """, (
                        email,
                        birthday,
                        group_id,
                        phone,
                        contact_id
                    ))

                else:
                    cursor.execute("""
                        INSERT INTO contacts (
                            first_name,
                            phone,
                            email,
                            birthday,
                            group_id
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        name,
                        phone,
                        email,
                        birthday,
                        group_id
                    ))

                    contact_id = cursor.fetchone()[0]

                # Avoid importing the same phone twice
                cursor.execute("""
                    SELECT 1
                    FROM phones
                    WHERE contact_id = %s
                      AND phone = %s
                """, (contact_id, phone))

                if cursor.fetchone() is None:
                    cursor.execute("""
                        INSERT INTO phones (
                            contact_id,
                            phone,
                            type
                        )
                        VALUES (%s, %s, %s)
                    """, (
                        contact_id,
                        phone,
                        phone_type
                    ))

                connection.commit()
                imported += 1
                print(f"Imported: {name} - {phone}")

            except Exception as error:
                connection.rollback()
                skipped += 1
                print(f"Error importing row: {error}")

        print("\n--- CSV Import Summary ---")
        print("Processed successfully:", imported)
        print("Skipped:", skipped)

        cursor.close()

    except Exception as error:
        connection.rollback()
        print("CSV import error:", error)

    finally:
        connection.close()


def main():
    while True:
        print("\n========== PhoneBook TSIS 1 ==========")
        print("1. Search contacts by pattern")
        print("2. Add or update contact")
        print("3. Insert many contacts")
        print("4. Show contacts with pagination")
        print("5. Delete contact")
        print("6. Filter and sort contacts")
        print("7. Export contacts to JSON")
        print("8. Import contacts from JSON")
        print("9. Import contacts from CSV")
        print("0. Exit")

        choice = input("\nChoose an option: ")

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

        elif choice == "6":
            filter_sort_contacts()

        elif choice == "7":
            export_contacts_json()

        elif choice == "8":
            import_contacts_json()    

        elif choice == "0":
            print("Goodbye!")
            break
        elif choice == "9":
            import_contacts_csv()
        
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()