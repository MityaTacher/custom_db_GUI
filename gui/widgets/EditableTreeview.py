from tkinter import END
from tkinter.ttk import Treeview, Entry, Style
from gui.widgets.CustomEntry import style_entry


def style_treeview():
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
    def __init__(self, master,
                 connection=None,
                 rename_header_func=None,
                 change_value_func=None,
                 insert_row_func=None,
                 new_header_func=None,
                 get_number_rows_func=None, **kwargs):
        super().__init__(master, **kwargs)

        self.entry_style = style_entry()

        self.connection = connection
        self.rename_header = rename_header_func
        self.change_value = change_value_func
        self.insert_row = insert_row_func
        self.new_header = new_header_func
        self.get_number_rows = get_number_rows_func

        self.editing_entry = None
        self.bind("<Double-1>", self.on_double_click)

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

        self.editing_entry = Entry(
            self,
            style=self.entry_style["style"],
            font=self.entry_style["font"]['heading']
        )
        self.editing_entry.insert(0, value)
        self.editing_entry.select_range(0, END)
        self.editing_entry.focus()

        self.editing_entry.place(x=x, y=y, width=width, height=height)

        def on_focus_out(event):
            new_value = self.editing_entry.get()
            self.heading(value, text=new_value)
            self.rename_header(self.connection, 'database', value, new_value)
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
        row_index = int(row_id[-1])

        if column == '#1':
            if value == '+':
                self.add_line()
            return
        if row_index == self.get_number_rows(self.connection, 'database') + 1:
            return

        column_index = int(column[1:]) - 1
        column_value = self["columns"][column_index]

        self.editing_entry = Entry(
            self,
            style=self.entry_style["style"],
            font=self.entry_style["font"]['cell']
        )
        self.editing_entry.insert(0, value)
        self.editing_entry.select_range(0, END)
        self.editing_entry.focus()

        self.editing_entry.place(x=x, y=y, width=width, height=height)

        def on_focus_out(event):
            new_value = self.editing_entry.get()
            self.set(row_id, column, new_value)
            self.change_value(self.connection, 'database', column_value,
                              self.editing_entry.get(), row_index)
            self.editing_entry.destroy()
            self.editing_entry = None

        self.editing_entry.bind("<Return>", on_focus_out)
        self.editing_entry.bind("<FocusOut>", on_focus_out)

    def add_line(self):
        number_rows = self.get_number_rows(self.connection, 'database')
        self.insert("", number_rows, values=[number_rows + 1])
        self.insert_row(self.connection, 'database', {"id": number_rows + 1})
        self.event_generate("<<NeedRefresh>>")

    def add_heading(self, name):
        self.new_header(self.connection, 'database', name)
        self.event_generate('<<NeedRefresh>>')
