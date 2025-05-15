import sqlite3


def get_connection(db_path='test.db'):
    return sqlite3.connect(db_path)


def close_connection(conn: sqlite3.Connection):
    conn.close()


def create_table(conn, table_name: str, columns: dict):
    cursor = conn.cursor()

    column_defs = [f"{name} {dtype}" for name, dtype in columns.items()]
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_defs)});"

    print(f"Создание таблицы SQL: {sql}")
    cursor.execute(sql)
    conn.commit()


def insert_row(conn, table_name: str, values: dict):
    cursor = conn.cursor()

    columns = ', '.join(values.keys())
    placeholders = ', '.join(['?'] * len(values))
    sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
    print(sql_query)
    cursor.execute(sql_query, list(values.values()))
    conn.commit()


def select_all(conn, table_name: str):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    return cursor.fetchall()


def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    all_tablenames = [tablename for (tablename,) in tables[:-1]]

    return all_tablenames


def get_column_names(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
    return [description[0] for description in cursor.description]


def change_value(conn, table_name, heading, value, id):
    cursor = conn.cursor()
    sql_query = f'UPDATE {table_name} SET {heading} = ? WHERE id = ?'
    cursor.execute(sql_query, (value, id))
    conn.commit()


def rename_header(conn, table_name, old_name, new_name):
    cursor = conn.cursor()
    sql_query = f'ALTER TABLE "{table_name}" RENAME COLUMN "{old_name}" TO "{new_name}"'
    cursor.execute(sql_query)
    conn.commit()


def new_header(conn, table_name, name):
    cursor = conn.cursor()
    number_columns = len(get_column_names(conn, table_name))
    sql_query = f'ALTER TABLE {table_name} ADD COLUMN {name}{number_columns} TEXT'
    cursor.execute(sql_query)
    conn.commit()


def get_number_rows(conn, table_name):
    cursor = conn.cursor()
    sql_query = f'SELECT COUNT(1) FROM {table_name}'
    cursor.execute(sql_query)

    return cursor.fetchall()[0][0]


def select_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    all_data = {}
    for (table_name,) in tables:
        cursor.execute(f"SELECT * FROM {table_name};")
        all_data[table_name] = cursor.fetchall()

    return all_data

