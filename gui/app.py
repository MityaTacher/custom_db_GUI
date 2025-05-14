import customtkinter as ctk
from gui.pages.home import HomePage
from gui.pages.redactor import RedactorPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)  # TODO beautiful home buttons & labels + any static image on side
        self.grid_columnconfigure(0, weight=1)

        self.filename = ''

        self.pages = {}

        for PageClass in (HomePage, RedactorPage):
            page = PageClass(self)
            self.pages[PageClass.__name__] = page
            page.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.show_page("HomePage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        if hasattr(page, "refresh"):
            page.refresh()
        page.tkraise()

