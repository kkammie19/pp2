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