import customtkinter as ctk
from core.utils import open_db_file, create_db_file
from PIL import Image


class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure_grid()
        self.create_side_image()
        self.mainframe = self.create_main_frame()
        self.create_logo()

        # Два блока с кнопками
        self.create_action_block(
            parent=self.mainframe,
            column=0,
            title="Открыть существующий",
            button_text="Выберите файл",
            command=self.open_file
        )
        self.create_action_block(
            parent=self.mainframe,
            column=1,
            title="Создать новый",
            button_text="Выберите файл",
            command=lambda: self.open_file(create_new=True),
            padx=(0, 20)
        )

    def configure_grid(self):
        self.grid_columnconfigure(0, weight=0, minsize=320)  # 280 + 20 * 2 padx
        self.grid_columnconfigure(1, weight=1)

    def create_side_image(self):
        side_image = ctk.CTkImage(dark_image=Image.open("Resourses/home_image.png"), size=(280, 500))
        side_image_label = ctk.CTkLabel(self, image=side_image, text='')
        side_image_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    def create_main_frame(self):
        mainframe = ctk.CTkFrame(self)
        mainframe.grid_columnconfigure((0, 1), weight=1)
        mainframe.grid_rowconfigure((0, 1), weight=1)
        mainframe.grid(column=1, row=0, padx=(0, 20), pady=20, sticky='nsew')
        return mainframe

    def create_logo(self):
        logo_image = ctk.CTkImage(dark_image=Image.open('Resourses/logo.png'), size=(531, 190))
        welcome_label = ctk.CTkLabel(self.mainframe, image=logo_image, text="")
        welcome_label.grid(column=0, row=0, columnspan=2, padx=20, pady=20)

    def create_action_block(self, parent, column, title, button_text, command, padx=20):
        frame = ctk.CTkFrame(parent)
        frame.grid(column=column, row=1, padx=padx, pady=20, sticky='')

        label = ctk.CTkLabel(frame, text=title)
        label.grid(column=0, row=0, padx=20, pady=20)

        button = ctk.CTkButton(frame, text=button_text, command=command)
        button.grid(column=0, row=1, padx=20, pady=(0, 20))

    def refresh(self):
        self.master.title("db redactor")

    def open_file(self, create_new=False):
        path = create_db_file() if create_new else open_db_file()
        if path is not None:
            self.master.filename = path
            self.master.show_page("RedactorPage")
        else:
            print("No path")
