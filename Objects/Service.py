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

def check_if_fld_val_exists(field_code, field_val):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT FIELD_TYPE FROM pafieldcodep0 WHERE field_code = :fc AND del_flag = 'N'",
            {"fc": field_code}
        )

        result = cursor.fetchone()
        if not result:
            return {"status": "error", "message": "Invalid field_code"}
        
        field_type = result[0]
        if field_type == 'N':
            field_val = int(field_val)
            plsql_func = "CMN_VAL_PKG.isValNumExist"
        elif field_type in ['C', 'V']:
            plsql_func = "CMN_VAL_PKG.isValCharExist"
        else:
            return {"status": "error", "message": f"Unsupported field type {field_type}"}
        
        output = cursor.callfunc(
            plsql_func,
            int,
            [field_code, field_val]
        )

        if output > 0:
            return {"status": "success", "exists": True}
        elif output == 0:
            return {"status": "success", "exists": False}
        else:
            return {"status": "error", "message": "Oracle returned error"}

    except Exception as e:
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        connection.close()  # returns to pool  