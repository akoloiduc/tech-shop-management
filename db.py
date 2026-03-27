import pyodbc

def get_db_connection():
    # Kết nối database
    cn_str = (
        "DRIVER={SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=DuLieu;"
        "UID=sa;"
        "PWD=dung0;"
    )
    return pyodbc.connect(cn_str)

def rows_to_dict_list(cursor):
    # Chuyển từ query về dạng dict
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]