from frontend.app import Interfaz
from backend.database import ConexionPostgres
from frontend.login import LoginScreen 
import customtkinter as ctk

def mostrar_interfaz(root, db):
    app = Interfaz(master=root, db=db)
    app.pack(expand=True, fill="both")  

def main():
    db = ConexionPostgres()
    db.conectar()

    root = ctk.CTk()
    root.withdraw()

    def on_login_success():
        root.deiconify() 
        mostrar_interfaz(root, db)

    LoginScreen(root, db, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()
