CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE first_name = p_first_name
    ) THEN
        UPDATE contacts
        SET phone = p_phone
        WHERE first_name = p_first_name;
    ELSE
        INSERT INTO contacts (first_name, phone)
        VALUES (p_first_name, p_phone);
    END IF;
END;
$$;
"""вставляет новый контакт, если имя не существует, или обновляет номер телефона, если имя уже существует."

CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names VARCHAR[],
    p_phones VARCHAR[],
    INOUT incorrect_data TEXT[] DEFAULT ARRAY[]::TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INTEGER;
    current_name VARCHAR;
    current_phone VARCHAR;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP

        current_name := p_names[i];
        current_phone := p_phones[i];

        IF current_phone ~ '^\+?[0-9]{10,15}$' THEN

            INSERT INTO contacts (first_name, phone)
            VALUES (current_name, current_phone)
            ON CONFLICT (phone) DO NOTHING;

        ELSE
            incorrect_data := array_append(
                incorrect_data,
                current_name || ': ' || current_phone
            );
        END IF;

    END LOOP;
END;
$$;
"""вставляет несколько контактов, проверяя корректность номеров телефонов. Некорректные данные возвращаются в массиве incorrect_data."

CREATE OR REPLACE PROCEDURE delete_contact(
    p_value VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_value
       OR phone = p_value;
END;
$$;
"""удаляет контакт по имени или номеру телефона."""


-- =========================================
-- TSIS 1: Add phone number
-- =========================================

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_count INTEGER;
    v_type VARCHAR;
BEGIN
    v_type := LOWER(TRIM(p_type));

    -- Check phone type
    IF v_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION
            'Invalid phone type. Use home, work or mobile.';
    END IF;

    -- Find contact
    SELECT COUNT(*)
    INTO v_count
    FROM contacts
    WHERE first_name = p_contact_name;

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Contact % not found.', p_contact_name;
    END IF;

    IF v_count > 1 THEN
        RAISE EXCEPTION
            'More than one contact has this name.';
    END IF;

    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE first_name = p_contact_name;

    -- Check duplicate phone
    IF EXISTS (
        SELECT 1
        FROM phones
        WHERE contact_id = v_contact_id
          AND phone = p_phone
    ) THEN
        RAISE EXCEPTION 'This phone already exists.';
    END IF;

    -- Insert new phone
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, v_type);

END;
$$;



-- =========================================
-- TSIS 1: Move contact to group
-- =========================================

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
    v_count INTEGER;
BEGIN
    -- Check whether contact exists
    SELECT COUNT(*)
    INTO v_count
    FROM contacts
    WHERE first_name = p_contact_name;

    IF v_count = 0 THEN
        RAISE EXCEPTION 'Contact % not found.', p_contact_name;
    END IF;

    IF v_count > 1 THEN
        RAISE EXCEPTION
            'More than one contact has this name.';
    END IF;

    -- Create group if it does not exist
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    -- Get group ID
    SELECT id
    INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    -- Update contact group
    UPDATE contacts
    SET group_id = v_group_id
    WHERE first_name = p_contact_name;

END;
$$;
