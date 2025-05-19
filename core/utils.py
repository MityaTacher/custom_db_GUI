from tkinter import filedialog
from openpyxl import Workbook
import csv
from core.crud import create_table, get_connection, close_connection


def open_db_file() -> str | None:

    file_path = filedialog.askopenfilename(
        title="Откройте файл базы данных .db",
        filetypes=[("SQLite Database", "*.db")],
        initialfile="test.db"
    )

    if not file_path:
        return None
    return file_path


def create_db_file() -> str | None:
    file_path = filedialog.asksaveasfilename(
        defaultextension=".db",
        filetypes=[("SQLite database", "*.db")],
        title="Создать новый файл"
    )

    if not file_path:
        return None

    with open(file_path, "w"):
        conn = get_connection(file_path)
        create_table(conn, "database", {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT",
        })
        print("TABLE CREATED")
        close_connection(conn)
    return file_path


def export_database(full_dir: str, headers: list[str], data: list[list[str | int]]) -> None:
    filename = full_dir.split("/")[-1][:-3]
    initialdir = full_dir[:-len(filename) - 3]
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[("Книга Exel", "*.xlsx"),
                                                        ('CSV (разделители - запятые)', "*.csv")],
                                             title="Экспорт .xlsx",
                                             initialdir=initialdir,
                                             initialfile=filename,
                                             confirmoverwrite=True)
    if not file_path:
        return None

    full_data = [headers, *data]
    filetype = file_path.split('.')[-1]
    if filetype == 'xlsx':
        export_xlsx(file_path, full_data)
    elif filetype == 'csv':
        export_csv(file_path, full_data)
    else:
        print(f'cannot save, unknown type: {filetype}')


def export_xlsx(file_path: str, data: list[str]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Database"

    for row in data:
        ws.append(row)

    wb.save(file_path)
    wb.close()


def export_csv(file_path: str, data: list[str]) -> None:
    with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(data)
