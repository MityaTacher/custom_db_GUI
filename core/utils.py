from tkinter import filedialog


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
            return file_path
    return None
