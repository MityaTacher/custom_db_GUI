import customtkinter as ctk
from core.utils import open_db_file, create_db_file
from PIL import Image

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.app import App


class HomePage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master: 'App' = master
        self.configure_grid()
        self.create_side_image()
        self.mainframe = self.create_main_frame()
        self.create_logo()

        self.create_action_block(
            column=0,
            title="Открыть существующий",
            button_text="Выберите файл",
            command=self.open_file,
            padx=20
        )
        self.create_action_block(
            column=1,
            title="Создать новый",
            button_text="Выберите файл",
            command=lambda: self.open_file(create_new=True),
            padx=(0, 20)
        )

    def configure_grid(self) -> None:
        self.grid_columnconfigure(0, weight=0, minsize=320)  # 280 + 20 * 2 padx
        self.grid_columnconfigure(1, weight=1)

    def create_side_image(self) -> None:
        side_image = ctk.CTkImage(dark_image=Image.open("Resourсes/home_image.png"), size=(280, 500))
        side_image_label = ctk.CTkLabel(self, image=side_image, text='')
        side_image_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    def create_main_frame(self) -> ctk.CTkFrame:
        mainframe = ctk.CTkFrame(self)
        mainframe.grid_columnconfigure((0, 1), weight=1)
        mainframe.grid_rowconfigure((0, 1), weight=1)
        mainframe.grid(column=1, row=0, padx=(0, 20), pady=20, sticky='nsew')
        return mainframe

    def create_logo(self) -> None:
        logo_image = ctk.CTkImage(dark_image=Image.open('Resourсes/logo.png'), size=(531, 190))
        welcome_label = ctk.CTkLabel(self.mainframe, image=logo_image, text="")
        welcome_label.grid(column=0, row=0, columnspan=2, padx=20, pady=(20, 0))

    def create_action_block(self, column, title, button_text, command, padx) -> None:

        frame = ctk.CTkFrame(self.mainframe)
        frame.grid(column=column, row=1, padx=padx, pady=(0, 20), sticky='')

        label = ctk.CTkLabel(frame, text=title, font=('Segoe UI', 14))
        label.grid(column=0, row=0, padx=20, pady=20)

        button = ctk.CTkButton(
            frame,
            text=button_text,
            font=("Segoe UI", 14),
            border_width=1,
            border_spacing=5,
            border_color='white',
            command=command
        )
        button.grid(column=0, row=1, padx=20, pady=(0, 20))

    def refresh(self) -> None:
        self.master.title("db redactor")

    def open_file(self, create_new: bool = False) -> None:
        path = create_db_file() if create_new else open_db_file()
        if path is not None:
            self.master.filename = path
            self.master.show_page("RedactorPage")
        else:
            print("No path")
