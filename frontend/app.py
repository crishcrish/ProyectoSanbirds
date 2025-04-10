import os
import customtkinter as ctk
from PIL import Image
from backend.database import ConexionPostgres as psql
import tkinter.ttk as ttk

rutaImagenLogoSanbirds = os.path.abspath("frontend/assets/LOGOSANBIRDSDB.png")

class Interfaz(ctk.CTkFrame):
    def __init__(self, master=None, db=None):
        super().__init__(master)
        self.master = master
        self.db = db
        self.pack(expand=True, fill="both")
        self.master.title("SanbirdsDB")
        self.master.geometry("1200x700")
        self.master.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.tabla_seleccionada = "cliente"
        self.frame_superior()
        self.area_resultados()

    def crear_tabla(self, columnas):
        # Limpiar frame anterior
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(expand=True, fill="both", side="left")

        # Scrollbar
        vsb = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

    def insertar_datos(self, datos):
        for fila in datos:
            self.tree.insert("", "end", values=fila)

    def frame_superior(self):
        frame_top = ctk.CTkFrame(self, height=100)
        frame_top.pack(fill="x", padx=10, pady=(10, 0))

        contenedor = ctk.CTkFrame(frame_top, fg_color="transparent")
        contenedor.pack(pady=15, padx=20, side="left")

        logo = ctk.CTkImage(Image.open(rutaImagenLogoSanbirds), size=(100, 60))
        logo_label = ctk.CTkLabel(contenedor, image=logo, text="")
        logo_label.pack(side="left", padx=10)

        boton_buscar = ctk.CTkButton(contenedor, text="Buscar datos", command=self.buscar_datos)
        boton_buscar.pack(side="left", padx=10)

    def area_resultados(self):
        frame_body = ctk.CTkFrame(self)
        frame_body.pack(expand=True, fill="both", padx=20, pady=10)

        # Menú lateral
        frame_menu = ctk.CTkFrame(frame_body, width=200)
        frame_menu.pack(side="left", fill="y", padx=(0, 10), pady=10)

        tablas = ["cliente", "envio", "detalles_envio", "productos", "proveedor"]
        for tabla in tablas:
            ctk.CTkButton(
                frame_menu,
                text=tabla.capitalize().replace("_", " "),
                width=160,
                corner_radius=10,
                command=lambda t=tabla: self.seleccionar_tabla(t)
            ).pack(pady=5, padx=10)

        # Área para la tabla
        self.frame_tabla = ctk.CTkFrame(frame_body)
        self.frame_tabla.pack(expand=True, fill="both", pady=10)

    def seleccionar_tabla(self, nombre_tabla):
        self.tabla_seleccionada = nombre_tabla
        self.buscar_datos()

    def buscar_datos(self):
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.tabla_seleccionada}")
                datos = cursor.fetchall()
                columnas = [desc[0] for desc in cursor.description]

                self.crear_tabla(columnas)
                self.insertar_datos(datos)

        except Exception as e:
            label = ctk.CTkLabel(self.frame_tabla, text=f"Error al obtener datos: {e}", text_color="red")
            label.pack(pady=20)

    def cerrar_aplicacion(self):
        if self.db:
            self.db.cerrar_conexion()
        self.master.destroy()
