from fastapi import FastAPI, HTTPException
from db import get_db_connection

app = FastAPI()

@app.get("/field-values/{field_code}")
def get_field_values(field_code: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Step 1: Get field type
        cursor.execute("SELECT FIELD_TYPE FROM pafieldcodep0 WHERE field_code = :fc AND del_flag = 'N'",
            {"fc": field_code}
        )

        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Field code not found")
        
        field_type = result[0]

        # Step 2: Prepare second query based on field type
        if field_type == 'N':
            query = """
                SELECT num_field_val, description
                FROM pafldvalnumv0"""
        elif field_type in ['C', 'V']:
            query = """
                SELECT char_field_val, description
                FROM pafldvalcharv0"""
        else:
            raise HTTPException(status_code=400, detail="Unsupported field type")
        
        # Step 3: Execute second query
        cursor.execute(query + " WHERE field_code = :fc AND del_flag = 'N'",
            {"fc": field_code}
        )
        results = cursor.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

    return results  