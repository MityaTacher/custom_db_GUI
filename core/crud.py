import sqlite3


def quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def get_connection(db_path: str = 'test.db') -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def close_connection(conn: sqlite3.Connection) -> None:
    conn.close()


def create_table(conn: sqlite3.Connection, table_name: str, columns: dict[str, str]) -> None:
    cursor = conn.cursor()
    table_name = quote_identifier(table_name)
    column_defs = [f"{quote_identifier(name)} {dtype}" for name, dtype in columns.items()]
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_defs)});"

    print(f"Создание таблицы SQL: {sql}")
    cursor.execute(sql)
    conn.commit()


def insert_row(conn: sqlite3.Connection, table_name: str, values: dict[str, str | int]) -> None:
    table_name = quote_identifier(table_name)
    columns = ', '.join(quote_identifier(name) for name in values.keys())
    placeholders = ', '.join(['?'] * len(values))

    cursor = conn.cursor()
    sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
    print(sql_query)
    cursor.execute(sql_query, list(values.values()))
    conn.commit()


def select_all(conn: sqlite3.Connection, table_name: str) -> list[list[str | int]]:
    table_name = quote_identifier(table_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()


def get_table_names(conn: sqlite3.Connection) -> list[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    all_tablenames = [tablename for (tablename,) in tables[:-1]]
    return all_tablenames


def get_headers(conn: sqlite3.Connection, table_name: str) -> list[str]:
    table_name = quote_identifier(table_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
    return [description[0] for description in cursor.description]


def change_value(conn: sqlite3.Connection, table_name: str, heading: str, value: str, row_id: int | str) -> None:
    table_name = quote_identifier(table_name)
    heading = quote_identifier(heading)
    cursor = conn.cursor()
    sql_query = f'UPDATE {table_name} SET {heading} = ? WHERE id = ?'
    print(heading, sql_query)
    cursor.execute(sql_query, (value, row_id))
    conn.commit()


def rename_header(conn: sqlite3.Connection, table_name: str, old_name: str, new_name: str) -> None:
    table_name = quote_identifier(table_name)
    old_name = quote_identifier(old_name)
    new_name = quote_identifier(new_name)
    cursor = conn.cursor()
    sql_query = f'ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name}'
    cursor.execute(sql_query)
    conn.commit()


def new_header(conn: sqlite3.Connection, table_name: str, name: str) -> None:
    number_columns = len(get_headers(conn, table_name))
    table_name = quote_identifier(table_name)
    new_name = quote_identifier(name + str(number_columns))
    cursor = conn.cursor()
    sql_query = f'ALTER TABLE {table_name} ADD COLUMN {new_name} TEXT'
    cursor.execute(sql_query)
    conn.commit()


def get_number_rows(conn: sqlite3.Connection, table_name: str) -> int:
    table_name = quote_identifier(table_name)
    cursor = conn.cursor()
    sql_query = f'SELECT COUNT(1) FROM {table_name}'
    cursor.execute(sql_query)

    return cursor.fetchall()[0][0]
