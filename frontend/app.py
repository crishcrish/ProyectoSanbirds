import os
import sys
import tkinter as tk
from tkinter import ttk
from backend.database import ConexionPostgres as psql
from PIL import Image, ImageTk

rutaImagenLogoSanbirds = os.path.abspath("frontend/assets/LOGOSANBIRDSDB.png")


class Interfaz(tk.Frame):
    def __init__(self, master=None, db = None): # Iniciar, pidiendo el master y la base de datos
        super().__init__(master, width=1200, height=700) # Tamaño de la pestaña
        self.master = master
        self.db = db
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion) # Protocolo para cerrar la app
        self.pack(expand=True, fill="both") # Hace que el frame principal ocupe toda la ventana
        self.frame_superior() # Pone el frame superior
        self.area_resultados() # Pone el area de resultados
        
    def frame_superior(self):   # Contenedor con la imagen y el botón

        self.frame_superior = tk.Frame(self, bg="blue", height=100) # Creación del frame
        self.frame_superior.pack(fill="x")

        # Creación de un contenedor dentro del frame superior
        contenedor = tk.Frame(self.frame_superior, bg = "blue") 
        contenedor.pack(pady=20, side="left")

        # Abrir y redimensión de la imagen
        logoSanbirdsOriginal = Image.open(rutaImagenLogoSanbirds)
        ancho_original, alto_original = logoSanbirdsOriginal.size
        logoSanbirdsRedimensionado = logoSanbirdsOriginal.resize((int(ancho_original*0.2), int(alto_original*0.2)))
        self.logoSanbirdsImagen = ImageTk.PhotoImage(logoSanbirdsRedimensionado)
        
        # Poner imagen en un label
        logoSanbirdsLabel = tk.Label(contenedor, image=self.logoSanbirdsImagen)
        logoSanbirdsLabel.pack(side="left", padx=10)

        # Botón con la función buscar
        boton_buscar = tk.Button(contenedor, text="Buscar datos", command=self.buscar_datos)
        boton_buscar.pack(side="left", padx=10)  

    def area_resultados(self):
        self.frame_inferior = tk.Frame(self)
        self.frame_inferior.pack(expand=True, fill="both", padx=20, pady=10)

        #Creación y encapsulación de frames
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
        
        # Creación de columnas
            # Creación de columnas centradas
        self.vista_datos.column("#0", width=150)
        self.vista_datos.column("col1", width=150, anchor="center") 
        self.vista_datos.column("col2", width=150, anchor="center")

            # Titulos a las columnas
        self.vista_datos.heading("#0", text="Producto", anchor="center")
        self.vista_datos.heading("col1", text="Precio", anchor="center")
        self.vista_datos.heading("col2", text="Cantidad", anchor="center")

            # Empaquetar
        self.vista_datos.pack(expand=True, fill="both")


    def buscar_datos(self):
        almacenamientoDatos = [] # Se guardan los datos
        try:
            # Se buscan los datos
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
    
    # Cerrar la aplicación
    def cerrar_aplicacion(self):
        if self.db: # Si está conectada la base de datos entonces cierra la conexión
            self.db.cerrar_conexion()
        self.master.destroy() # Destruye el master con la interfaz
