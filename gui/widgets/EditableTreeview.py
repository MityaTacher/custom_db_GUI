from tkinter import END
from tkinter.ttk import Treeview, Entry, Style

from gui.widgets.CustomEntry import style_entry

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    import customtkinter as ctk
    import tkinter as tk


def style_treeview() -> None:
    style = Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#2b2b2b",
                    foreground="white",
                    rowheight=30,
                    fieldbackground="#2b2b2b",
                    bordercolor="#444444",
                    borderwidth=1,
                    font=("Segoe UI", 12),
                    relief="solid"
                    )

    style.configure("Treeview.Heading",
                    background="#1f1f1f",
                    foreground="white",
                    font=("Segoe UI", 13, "bold")
                    )

    style.map("Treeview.Heading",
              background=[("active", "#7ec5fc")],
              foreground=[("active", "black")]
              )

    style.map("Treeview",
              background=[("selected", "#1f6aa5")],
              foreground=[("selected", "white")]
              )


class EditableTreeview(Treeview):
    def __init__(self, master: 'ctk.CTkFrame',
                 connection=None,
                 rename_header_func=None,
                 change_value_func=None,
                 insert_row_func=None,
                 new_header_func=None,
                 get_number_rows_func=None,
                 get_headers=None,
                 select_all=None, **kwargs):
        super().__init__(master, **kwargs)

        self.entry_style = style_entry()

        self.connection = connection
        self.rename_header = rename_header_func
        self.change_value = change_value_func
        self.insert_row = insert_row_func
        self.new_header = new_header_func
        self.get_number_rows = get_number_rows_func
        self.get_headers = get_headers
        self.select_all = select_all

        self.editing_entry = None
        self.bind("<Double-1>", self.on_double_click)

    def render_headings(self, column_names: list[str]) -> None:
        for column in column_names:
            self.heading(column, text=column)
        self.column("id", width=40, stretch=False)
        self.column("+", width=20, stretch=False)

    def render_rows(self, table_name: str) -> None:
        for row in self.get_children():
            self.delete(row)

        rows = self.select_all(self.connection, table_name)
        for index, row in enumerate(rows):
            row = [cell if cell is not None else '' for cell in row]
            self.insert("", "end", values=row, iid=f'row{index + 1}')
        self.insert("", "end", values=["+"], iid='add')

    def on_double_click(self, event: 'tk.Event') -> None:
        region = self.identify("region", event.x, event.y)
        print(region)
        if region == "cell":
            self.edit_cell(event)
        elif region == 'heading':
            self.edit_heading(event)

    def heading_bbox(self, column: str) -> Tuple[int, int, int, int]:
        x, _, width, _ = self.bbox('I001', column)
        y = 0
        height = 25
        return x, y, width, height

    def edit_heading(self, event: 'tk.Event') -> None:
        column = self.identify_column(event.x)
        column_index = int(column[1:]) - 1

        value = self["columns"][column_index]
        if value == 'id' or self.editing_entry is not None:
            return
        if value == '+':
            self.add_heading("new_heading")
            return
        x, y, width, height = self.heading_bbox(column)

        self.editing_entry = Entry(
            self,
            style=self.entry_style["style"],
            font=self.entry_style["font"]['heading']
        )
        self.editing_entry.insert(0, value)
        self.editing_entry.select_range(0, END)
        self.editing_entry.focus()

        self.editing_entry.place(x=x, y=y, width=width, height=height)

        def on_focus_out(_event: 'tk.Event') -> None:
            new_value = self.editing_entry.get()
            self.heading(value, text=new_value)
            if value != new_value and new_value in self.get_headers(self.connection, 'database'):
                self.editing_entry.focus()
                self.editing_entry.bind("<Return>", on_focus_out)
                self.editing_entry.bind("<FocusOut>", on_focus_out)
            else:
                self.rename_header(self.connection, 'database', value, new_value)
                self.event_generate("<<NeedRefresh>>")
                self.editing_entry.destroy()
                self.editing_entry = None

        self.editing_entry.bind("<Return>", on_focus_out)
        self.editing_entry.bind("<FocusOut>", on_focus_out)

    def edit_cell(self, event: 'tk.Event') -> None:
        row_id = self.identify_row(event.y)
        column = self.identify_column(event.x)

        if not column and not row_id:
            return
        if row_id == 'add':
            return

        x, y, width, height = self.bbox(row_id, column)
        print(f'|{row_id}|, |{column}|')
        value = self.set(row_id, column)
        row_index = int(row_id[3:])

        column_index = int(column[1:]) - 1
        column_value = self["columns"][column_index]

        if column == '#1' or column_value == '+' or self.editing_entry is not None:
            if value == '+':
                self.add_line()
            return

        self.editing_entry = Entry(
            self,
            style=self.entry_style["style"],
            font=self.entry_style["font"]['cell']
        )
        self.editing_entry.insert(0, value)
        self.editing_entry.select_range(0, END)
        self.editing_entry.focus()

        self.editing_entry.place(x=x, y=y, width=width, height=height)

        def on_focus_out(_event: 'tk.Event') -> None:
            new_value = self.editing_entry.get()
            self.set(row_id, column, new_value)
            self.change_value(self.connection, 'database', column_value,
                              self.editing_entry.get(), row_index)
            self.editing_entry.destroy()
            self.editing_entry = None

        self.editing_entry.bind("<Return>", on_focus_out)
        self.editing_entry.bind("<FocusOut>", on_focus_out)

    def add_line(self) -> None:
        number_rows = self.get_number_rows(self.connection, 'database')
        self.insert("", number_rows, values=[number_rows + 1])
        self.insert_row(self.connection, 'database', {"id": number_rows + 1})
        self.event_generate("<<NeedRefresh>>")

    def add_heading(self, name: str) -> None:
        self.new_header(self.connection, 'database', name)
        self.event_generate('<<NeedRefresh>>')
