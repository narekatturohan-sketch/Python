from db import get_db_connection

def get_data_from_db(field_code):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Step 1: Get FIELD_TYPE
        cursor.execute(
            "SELECT FIELD_TYPE FROM pafieldcodep0 WHERE field_code = :fc AND del_flag = 'N'",
            {"fc": field_code}
        )

        result = cursor.fetchone()

        if not result:
            print("No FIELD_TYPE found")
            return None

        field_type = result[0]

        # Step 2: Decide query
        if field_type == 'N':
            query = """
                SELECT num_field_val, description 
                FROM pafldvalnumv0 
                WHERE field_code = :fc AND del_flag = 'N'
            """
        elif field_type in ['C', 'V']:
            query = """
                SELECT char_field_val, description
                FROM pafldvalcharv0 
                WHERE field_code = :fc AND del_flag = 'N'
            """
        else:
            print(f"Unsupported field type: {field_type}")
            return None

        # Step 3: Execute second query
        cursor.execute(query, {"fc": field_code})

        for row in cursor.fetchall():
            print(row)

    finally:
        cursor.close()
        connection.close()  # returns to pool


if __name__ == "__main__":
    field_code = input("Enter the field code: ")
    get_data_from_db(field_code)