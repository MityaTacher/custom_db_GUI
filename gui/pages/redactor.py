import customtkinter as ctk
import tkinter.ttk as ttk
from core.crud import select_all, get_connection, get_table_names, get_column_names


class RedactorPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        back = ctk.CTkButton(self, text="Назад на главную",
                             command=lambda: master.show_page("HomePage"))
        back.pack()

        self.tree = ttk.Treeview(self)
        self.connection = None

    def refresh(self):
        self.tree.destroy()
        filepath = self.master.filename
        self.master.title(filepath)

        self.read_table(filepath)

    # open bd and get all sheets
    def read_table(self, filepath):
        self.connection = get_connection(filepath)
        table_names = get_table_names(self.connection)
        print(table_names)
        for sheet in table_names:
            print(get_column_names(self.connection, sheet))
            self.render_table(get_column_names(self.connection, sheet))
            self.show_all_rows(sheet)

    # open one sheet
    def render_table(self, column_names):
        self.tree = ttk.Treeview(self, columns=column_names, show="headings", height=10)

        for column in column_names:
            self.tree.heading(column, text=column)
        self.tree.column("id", width=20)

        self.tree.pack()
        # self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
    def show_all_rows(self, table_name):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rows = select_all(self.connection, table_name)
        for row in rows:
            self.tree.insert("", "end", values=row)