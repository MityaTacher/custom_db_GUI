import customtkinter as ctk
from core import crud
from gui.EditableTreeview import EditableTreeview
from core.utils import export_database


class RedactorPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure([i for i in range(5)], weight=1)

        back_button = ctk.CTkButton(self, text="Назад на главную",
                                    command=lambda: master.show_page("HomePage"))
        back_button.grid(column=0, row=0, columnspan=1, rowspan=1)

        export_button = ctk.CTkButton(self, text="Экспорт .xlsx",
                                      command=lambda:
                                      export_database(self.master.filename,
                                                      crud.get_column_names(self.connection, 'database'),
                                                      crud.select_all(self.connection, 'database')))
        export_button.grid(column=4, row=0, columnspan=1, rowspan=1)

        self.tree = EditableTreeview(self)
        self.connection = None

    def refresh(self):
        self.tree.destroy()
        self.connection = None
        filepath = self.master.filename
        self.master.title(filepath)
        print(f"\tINSTANT REFRESHING TABLE {filepath}")

        self.read_table(filepath)

    # open bd and get all sheets
    def read_table(self, filepath):
        self.connection = crud.get_connection(filepath)
        table_names = crud.get_table_names(self.connection)
        print(table_names)
        for sheet in table_names:
            print(crud.get_column_names(self.connection, sheet))
            self.render_table(crud.get_column_names(self.connection, sheet))
            self.show_all_rows(sheet)
            return

    # open one sheet
    def render_table(self, column_names):
        column_names.append("+")
        self.tree = EditableTreeview(self, columns=column_names, show="headings", height=10,
                                     connection=self.connection,
                                     rename_header_func=crud.rename_header,
                                     change_value_func=crud.change_value,
                                     insert_row_func=crud.insert_row,
                                     new_header_func=crud.new_header,
                                     get_number_rows_func=crud.get_number_rows)
        self.tree.bind("<<NeedRefresh>>", lambda event: self.refresh())

        for column in column_names:
            self.tree.heading(column, text=column)
        self.tree.column("id", width=20, stretch=False)
        self.tree.column("+", width=20, stretch=False)

        self.tree.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

    def show_all_rows(self, table_name):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = crud.select_all(self.connection, table_name)
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.tree.insert("", "end", values=["+"])
