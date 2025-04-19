from frontend.app import Interfaz
from backend.database import ConexionPostgres
import customtkinter as ctk

def main():
    db = ConexionPostgres()
    db.conectar()
    
    root = ctk.CTk()
    root.title("SanbirdsDB")
    root.geometry("1200x700") 
    app = Interfaz(master=root, db=db)
    app.pack(expand=True, fill="both")  
    root.mainloop()  

if __name__ == "__main__":
    main()
