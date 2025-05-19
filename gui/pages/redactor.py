import customtkinter as ctk
from core import crud
from gui.widgets.EditableTreeview import EditableTreeview, style_treeview
from core.utils import export_database

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.app import App


class RedactorPage(ctk.CTkFrame):
    def __init__(self, master: 'App', **kwargs):
        super().__init__(master, **kwargs)

        self.master: 'App' = master

        style_treeview()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.mainframe = self.create_main_frame()

        self.create_buttons_block()

        self.tree = EditableTreeview(self, self.mainframe)
        self.connection = None

    def create_buttons_block(self) -> None:
        buttons_frame = ctk.CTkFrame(self.mainframe)
        buttons_frame.grid_rowconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        buttons_frame.grid(column=0, row=0, pady=(20, 10), padx=20, columnspan=2, sticky='nsew')

        back_button = ctk.CTkButton(buttons_frame,
                                    text="Назад на главную",
                                    font=("Segoe UI", 14),
                                    border_width=1,
                                    border_spacing=5,
                                    border_color='white',
                                    command=lambda: self.master.show_page("HomePage"))

        back_button.grid(column=0, row=0, columnspan=1, rowspan=1)

        export_button = ctk.CTkButton(buttons_frame,
                                      text="Экспорт файла",
                                      font=("Segoe UI", 14),
                                      border_width=1,
                                      border_spacing=5,
                                      border_color='white',
                                      command=lambda:
                                      export_database(self.master.filename,
                                                      crud.get_headers(self.connection, 'database'),
                                                      crud.select_all(self.connection, 'database')))
        export_button.grid(column=1, row=0, columnspan=1, rowspan=1)

    def create_main_frame(self) -> ctk.CTkFrame:
        mainframe = ctk.CTkFrame(self)
        mainframe.grid_columnconfigure((0, 1), weight=1)
        mainframe.grid_rowconfigure((0, 1), weight=1)
        mainframe.grid(column=0, row=0, padx=20, pady=20, sticky='nsew')
        return mainframe

    def refresh(self) -> None:
        self.tree.destroy()
        self.connection = None
        filepath = self.master.filename
        self.master.title(filepath)
        print(f"\tINSTANT REFRESHING TABLE {filepath}")

        self.read_table(filepath)

    # open bd and get all sheets
    def read_table(self, filepath: str) -> None:
        self.connection = crud.get_connection(filepath)
        table_names = crud.get_table_names(self.connection)
        print(table_names)
        for sheet in table_names:
            print(crud.get_headers(self.connection, sheet))
            self.render_table(crud.get_headers(self.connection, sheet))
            self.tree.render_rows(sheet)
            return

    # open one sheet
    def render_table(self, column_names: list) -> None:
        column_names.append("+")
        self.tree = EditableTreeview(self.mainframe, columns=column_names, show="headings", height=10,
                                     connection=self.connection,
                                     rename_header_func=crud.rename_header,
                                     change_value_func=crud.change_value,
                                     insert_row_func=crud.insert_row,
                                     new_header_func=crud.new_header,
                                     get_number_rows_func=crud.get_number_rows,
                                     get_headers=crud.get_headers,
                                     select_all=crud.select_all)
        self.tree.bind("<<NeedRefresh>>", lambda event: self.refresh())

        self.tree.render_headings(column_names=column_names)

        self.tree.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
