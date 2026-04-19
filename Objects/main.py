from Service import get_data_from_db,check_if_fld_val_exists

if __name__ == "__main__":
    field_code = "C0001"
    field_val = "10" 
    response = check_if_fld_val_exists(field_code, field_val)
    print(response)