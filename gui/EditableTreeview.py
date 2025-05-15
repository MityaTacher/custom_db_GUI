from tkinter import END
from tkinter.ttk import Treeview, Entry

import core.crud


class EditableTreeview(Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.editing_entry = None
        self.bind("<Double-1>", self.on_double_click)
        # self.bind("<Return>", self.on_return)
        self.lines = None

    def on_double_click(self, event):
        region = self.identify("region", event.x, event.y)
        print(region)
        if region == "cell":
            self.edit_cell(event)
        elif region == 'heading':
            self.edit_heading(event)

    def heading_bbox(self, column):
        x, _, width, _ = self.bbox('I001', column)
        y = 0
        height = 25
        return x, y, width, height

    def edit_heading(self, event):
        column = self.identify_column(event.x)
        column_index = int(column[1:]) - 1

        value = self["columns"][column_index]
        if value == 'id':
            return
        if value == '+':
            self.add_heading("new_heading")
            return
        x, y, width, height = self.heading_bbox(column)

        self.editing_entry = Entry(self)
        self.editing_entry.insert(0, value)
        self.editing_entry.select_range(0, END)
        self.editing_entry.focus()

        self.editing_entry.place(x=x, y=y, width=width, height=height)

        def on_focus_out(event):
            new_value = self.editing_entry.get()
            self.heading(value, text=new_value)
            core.crud.rename_header(core.crud.get_connection(), 'contacts', value, new_value)
            self.event_generate("<<NeedRefresh>>")
            self.editing_entry.destroy()
            self.editing_entry = None

        self.editing_entry.bind("<Return>", on_focus_out)
        self.editing_entry.bind("<FocusOut>", on_focus_out)

    def edit_cell(self, event):
        row_id = self.identify_row(event.y)
        column = self.identify_column(event.x)

        if not column and not row_id:
            return

        x, y, width, height = self.bbox(row_id, column)
        print(f'|{row_id}|, |{column}|')
        value = self.set(row_id, column)
        row_index = row_id[-1]
        if column == '#1':
            if value == '+':
                self.add_line()
            return

        column_index = int(column[1:]) - 1
        column_value = self["columns"][column_index]

        self.editing_entry = Entry(self)
        self.editing_entry.insert(0, value)
        self.editing_entry.select_range(0, END)
        self.editing_entry.focus()

        self.editing_entry.place(x=x, y=y, width=width, height=height)

        def on_focus_out(event):
            new_value = self.editing_entry.get()
            self.set(row_id, column, new_value)
            core.crud.change_value(core.crud.get_connection(), 'contacts', column_value,
                                   self.editing_entry.get(), row_index)
            self.editing_entry.destroy()
            self.editing_entry = None

        self.editing_entry.bind("<Return>", on_focus_out)
        self.editing_entry.bind("<FocusOut>", on_focus_out)

    def add_line(self):
        conn = core.crud.get_connection()
        number_rows = core.crud.get_number_rows(conn, 'contacts')
        self.insert("", number_rows, values=[number_rows+1])
        core.crud.insert_row(conn, 'contacts', {"id": number_rows + 1})
        self.event_generate("<<NeedRefresh>>")

    def add_heading(self, name):
        core.crud.new_header(core.crud.get_connection(), 'contacts', name)
        self.event_generate('<<NeedRefresh>>')

