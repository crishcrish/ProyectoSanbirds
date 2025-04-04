from frontend.app import Interfaz
from backend.database import ConexionPostgres
import tkinter as tk

def main():
    db = ConexionPostgres()
    db.conectar()
    
    root = tk.Tk()
    root.title("SanbirdsDB")
    app = Interfaz(master=root, db=db)
    app.mainloop()

if __name__ == "__main__":
    main()
