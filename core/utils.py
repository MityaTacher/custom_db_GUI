from tkinter import filedialog

import core.crud


def open_db_file():

    file_path = filedialog.askopenfilename(
        title="Откройте файл базы данных .db",
        filetypes=[("SQLite Database", "*.db")],
        initialfile="test.db"
    )

    if file_path:
        return file_path
    else:
        return None


def create_db_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".db",
        filetypes=[("SQLite database", "*.db")],
        title="Создать новый файл"
    )

    if file_path:
        with open(file_path, "w"):
            core.crud.create_table(core.crud.get_connection(), "contacts", {
                "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
                "name": "TEXT",
            })
            # core.crud.insert_row(core.crud.get_connection(), 'contacts', {'id': '1'})
            print("TABLE CREATED: ", end='')
            print(core.crud.select_all(core.crud.get_connection(), 'contacts'))
            return file_path
    return None
