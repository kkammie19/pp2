CREATE OR REPLACE FUNCTION search_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.phone
    FROM contacts c
    WHERE c.first_name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%';
END;
$$;
"""получает pattern для поиска и возвращает контакты, у которых имя или номер телефона совпадают с этим pattern."""

CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    id INTEGER,
    first_name VARCHAR,
    phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$;
"""возвращает контакты с пагинацией, используя limit и offset."""



-- =========================================
-- TSIS 1: Advanced contact search
-- =========================================

CREATE OR REPLACE FUNCTION search_contacts(
    p_query TEXT
)
RETURNS TABLE (
    contact_id INTEGER,
    first_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones_list TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.first_name,
        c.email,
        c.birthday,
        g.name,
        COALESCE(
            (
                SELECT STRING_AGG(
                    p.phone || ' (' || p.type || ')',
                    ', '
                )
                FROM phones p
                WHERE p.contact_id = c.id
            ),
            'No phones'
        )
    FROM contacts c
    LEFT JOIN groups g
        ON c.group_id = g.id
    WHERE
        c.first_name ILIKE '%' || p_query || '%'
        OR COALESCE(c.email, '') ILIKE '%' || p_query || '%'
        OR EXISTS (
            SELECT 1
            FROM phones p
            WHERE p.contact_id = c.id
              AND p.phone ILIKE '%' || p_query || '%'
        )
    ORDER BY c.first_name;

END;
$$;
