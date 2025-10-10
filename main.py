import customtkinter as ctk
from ui.main_window import MainWindow

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("GreenCode - Gestão Energética")
    app.geometry("1200x700")

    MainWindow(app)
    app.mainloop()