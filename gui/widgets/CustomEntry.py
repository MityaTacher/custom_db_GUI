from tkinter.ttk import Style
from tkinter.font import Font


def style_entry() -> dict[str, str | dict[str, str]]:
    style = Style()
    style.theme_use("default")

    custom_font_heading = Font(family="Segoe UI", size=13, weight="bold")
    custom_font_cell = Font(family="Segoe UI", size=12)

    style.configure("Custom.TEntry",
                    selectforeground='white',
                    selectbackground='#0a4573'
                    )  # не работает если нормально применить шрифт

    style.map("Custom.TEntry",
              fieldbackground=[("focus", "#7ec5fc")],
              foreground=[("focus", "black")]
              )

    return {"style": "Custom.TEntry", "font": {'heading': custom_font_heading, 'cell': custom_font_cell}}
