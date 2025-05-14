import customtkinter as ctk
from core.utils import open_db_file, create_db_file


class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1, 2), weight=1)

        welcome_label = ctk.CTkLabel(self, text="Добро пожаловать!")
        welcome_label.grid(column=1, row=0, columnspan=1, rowspan=1)

        open_existing_label = ctk.CTkLabel(self, text="Открыть существующий")
        open_existing_label.grid(column=0, row=1, columnspan=1, rowspan=1)

        open_existing_button = ctk.CTkButton(self, text="Выберите файл", command=lambda: self.open_file())
        open_existing_button.grid(column=0, row=2, columnspan=1, rowspan=1)

        create_new_label = ctk.CTkLabel(self, text="Создать новый")
        create_new_label.grid(column=2, row=1, columnspan=1, rowspan=1)

        create_new_button = ctk.CTkButton(self, text="Выберите файл", command=lambda: self.open_file(create_new=1))
        create_new_button.grid(column=2, row=2, columnspan=1, rowspan=1)

    def refresh(self):
        self.master.title("db redactor")

    def open_file(self, create_new=0):
        if create_new:
            path = create_db_file()
        else:
            path = open_db_file()
        if path is not None:
            self.master.filename = path
            self.master.show_page("RedactorPage")
        else:
            print("No path")

