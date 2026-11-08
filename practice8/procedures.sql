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