import sqlite3


def get_connection(db_path='test.db'):
    return sqlite3.connect(db_path)


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
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
    print(sql)
    cursor.execute(sql, list(values.values()))
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


def select_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    all_data = {}
    for (table_name,) in tables:
        cursor.execute(f"SELECT * FROM {table_name};")
        all_data[table_name] = cursor.fetchall()

    return all_data

