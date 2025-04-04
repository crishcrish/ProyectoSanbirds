import os
import sys
import tkinter as tk
from tkinter import ttk
from backend.database import ConexionPostgres as psql
from PIL import Image, ImageTk

def obtener_ruta_recurso(ruta_relativa):
    try:
        base_path = sys._MEIPASS  # Carpeta temporal que usa PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

rutaImagenLogoSanbirds = os.path.abspath("frontend/assets/LOGOSANBIRDSDB.png")


print(rutaImagenLogoSanbirds)

db = psql()
db.conectar()

class Interfaz(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=1200, height=700)
        self.master = master
        self.db = db
        self.pack(expand=True, fill="both")
        self.frame_superior()
        self.area_resultados()
        
    def frame_superior(self):
        self.frame_superior = tk.Frame(self, bg="blue", height=100)
        self.frame_superior.pack(fill="x")

        contenedor = tk.Frame(self.frame_superior, bg = "blue")
        contenedor.pack(pady=20, side="left")

        logoSanbirdsOriginal = Image.open(rutaImagenLogoSanbirds)

        ancho_original, alto_original = logoSanbirdsOriginal.size

        logoSanbirdsRedimensionado = logoSanbirdsOriginal.resize((int(ancho_original*0.2), int(alto_original*0.2)))
        self.logoSanbirdsImagen = ImageTk.PhotoImage(logoSanbirdsRedimensionado)
        
        logoSanbirdsLabel = tk.Label(contenedor, image=self.logoSanbirdsImagen)
        logoSanbirdsLabel.pack(side="left", padx=10)

        boton_buscar = tk.Button(contenedor, text="Buscar datos", command=self.buscar_datos)
        boton_buscar.pack(side="left", padx=10)  

    def area_resultados(self):
        self.frame_inferior = tk.Frame(self)
        self.frame_inferior.pack(expand=True, fill="both", padx=20, pady=10)

        #Creacaión y encapsulación de frames
        frame_texto = tk.Frame(self.frame_inferior)
        frame_menu = tk.Frame(self.frame_inferior)

        # Pack de Frames
        frame_menu.pack(padx=20, pady=20, side="left", fill="y")
        frame_texto.pack(expand=True, fill="both", padx=20, pady=20, side="left")


        # Menú
        frasePrueba = tk.Label(frame_menu, text="hola")
        frasePrueba.pack()

        # Tabla de datos
        self.vista_datos = ttk.Treeview(frame_texto, columns=("col1","col2"))
        
        self.vista_datos.column("#0", width=150)
        self.vista_datos.column("col1", width=150, anchor="center")
        self.vista_datos.column("col2", width=150, anchor="center")

        self.vista_datos.heading("#0", text="Producto", anchor="center")
        self.vista_datos.heading("col1", text="Precio", anchor="center")
        self.vista_datos.heading("col2", text="Cantidad", anchor="center")

        self.vista_datos.pack(expand=True, fill="both")
        #self.texto_resultados = tk.Text(frame_texto, yscrollcommand=scrollbar.set)
        #self.texto_resultados.pack(expand=True, fill="both")
        #scrollbar.config(command=self.texto_resultados.yview)

    def buscar_datos(self):
        almacenamientoDatos = []
        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM productos")
                datos = cursor.fetchall()

                for i in datos:
                    almacenamientoDatos.append(i)

                if datos:
                    for fila in almacenamientoDatos:
                        self.vista_datos.insert("",tk.END, text=fila[0], values=(fila[1],fila[1]))
                else:
                    self.vista_datos.insert(tk.END, "No se encontraron datos.")

        except Exception as ex:
            self.vista_datos.insert(tk.END, f"Error al buscar datos: {ex}")


root = tk.Tk()
root.wm_title("Sanbirds")
app = Interfaz(master=root)
root.mainloop()

# Cerramos la conexión después de cerrar la ventana
db.cerrar_conexion()
