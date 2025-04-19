import os
import customtkinter as ctk
from PIL import Image
from backend.database import ConexionPostgres as psql
import tkinter.ttk as ttk

rutaImagenLogoSanbirds = os.path.abspath("frontend/assets/LOGOSANBIRDSDB.png")

class Interfaz(ctk.CTkFrame):
    def __init__(self, master=None, db=None):
        super().__init__(master, fg_color="#1e1e1e")
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
        for widget in self.frame_tabla.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.frame_tabla, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        self.tree.pack(expand=True, fill="both", side="left")

        vsb = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        botones_frame = ctk.CTkFrame(self.frame_tabla)
        botones_frame.pack(fill="x", pady=(10, 0))

        ctk.CTkButton(botones_frame, text="Agregar", command=self.abrir_ventana_agregar).pack(side="left", padx=10)
        ctk.CTkButton(botones_frame, text="Editar", command=self.abrir_ventana_editar).pack(side="left", padx=10)
        ctk.CTkButton(botones_frame, text="Eliminar", command=self.eliminar_registro).pack(side="left", padx=10)

    def insertar_datos(self, datos):
        for fila in datos:
            self.tree.insert("", "end", values=fila)

    def frame_superior(self):
        frame_top = ctk.CTkFrame(self, height=100)
        frame_top.pack(fill="x", padx=10, pady=(10, 0))

        contenedor = ctk.CTkFrame(frame_top)
        contenedor.pack(pady=15, padx=20, side="left")

        logo = ctk.CTkImage(Image.open(rutaImagenLogoSanbirds), size=(100, 60))
        logo_label = ctk.CTkLabel(contenedor, image=logo, text="")
        logo_label.pack(side="left", padx=10)

        self.boton_buscar = ctk.CTkButton(contenedor, text="Buscar datos", command=self.buscar_datos)
        self.boton_buscar.pack(side="left", padx=10)

    def area_resultados(self):
        frame_body = ctk.CTkFrame(self)
        frame_body.pack(expand=True, fill="both", padx=20, pady=10)

        frame_menu = ctk.CTkFrame(frame_body, width=200)
        frame_menu.pack(side="left", fill="y", padx=(0, 10), pady=10)

        self.botones_menu = []

        tablas = ["cliente", "envio", "detalles_envio", "productos", "proveedor"]
        for tabla in tablas:
            boton = ctk.CTkButton(
                frame_menu,
                text=tabla.capitalize().replace("_", " "),
                width=160,
                corner_radius=10,
                command=lambda t=tabla: self.seleccionar_tabla(t)
            )
            boton.pack(pady=5, padx=10)
            self.botones_menu.append(boton)

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

    def abrir_ventana_agregar(self):
        self.abrir_formulario("Agregar")

    def abrir_ventana_editar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        datos_seleccionados = self.tree.item(seleccion[0])["values"]
        self.abrir_formulario("Editar", datos_seleccionados)

    def abrir_formulario(self, modo, datos=None):
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"{modo} registro")
        ventana.geometry("400x400")
        ventana.configure(fg_color="#1e1e1e")

        # Centrar ventana
        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"+{x}+{y}")

        # Hacer modal
        ventana.transient(self)
        ventana.grab_set()
        ventana.focus_force()

        self.deshabilitar_ui()

        def cerrar_formulario():
            ventana.grab_release()
            ventana.destroy()
            self.habilitar_ui()
            self.buscar_datos()

        ventana.protocol("WM_DELETE_WINDOW", cerrar_formulario)

        campos = self.obtener_columnas()
        entradas = {}

        for campo in campos:
            label = ctk.CTkLabel(ventana, text=campo)
            label.pack()
            entry = ctk.CTkEntry(ventana)
            entry.pack(pady=5)
            if datos:
                entry.insert(0, datos[campos.index(campo)])
            entradas[campo] = entry

        def guardar():
            valores = [entradas[c].get() for c in campos]
            if modo == "Agregar":
                self.insertar_en_bd(campos, valores)
            elif modo == "Editar":
                self.actualizar_en_bd(campos, valores, datos[0])
            cerrar_formulario()

        ctk.CTkButton(ventana, text="Guardar", command=guardar).pack(pady=10)

    def insertar_en_bd(self, columnas, valores):
        try:
            with self.db.connection.cursor() as cursor:
                columnas_str = ", ".join(columnas[1:])
                valores_str = ", ".join(["%s"] * len(valores[1:]))
                cursor.execute(
                    f"INSERT INTO {self.tabla_seleccionada} ({columnas_str}) VALUES ({valores_str})",
                    valores[1:]
                )
                self.db.connection.commit()
        except Exception as e:
            print(f"Error al insertar: {e}")

    def actualizar_en_bd(self, columnas, valores, id_valor):
        try:
            with self.db.connection.cursor() as cursor:
                set_str = ", ".join([f"{col}=%s" for col in columnas[1:]])
                cursor.execute(
                    f"UPDATE {self.tabla_seleccionada} SET {set_str} WHERE {columnas[0]} = %s",
                    valores[1:] + [id_valor]
                )
                self.db.connection.commit()
        except Exception as e:
            print(f"Error al actualizar: {e}")

    def eliminar_registro(self):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        datos = self.tree.item(seleccion[0])["values"]
        id_valor = datos[0]
        try:
            with self.db.connection.cursor() as cursor:
                cursor.execute(
                    f"DELETE FROM {self.tabla_seleccionada} WHERE {self.obtener_columnas()[0]} = %s",
                    (id_valor,)
                )
                self.db.connection.commit()
            self.buscar_datos()
        except Exception as e:
            print(f"Error al eliminar: {e}")

    def obtener_columnas(self):
        with self.db.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self.tabla_seleccionada} LIMIT 0")
            return [desc[0] for desc in cursor.description]

    def cerrar_aplicacion(self):
        if self.db:
            self.db.cerrar_conexion()
        self.master.destroy()

    def deshabilitar_ui(self):
        for boton in self.botones_menu:
            boton.configure(state="disabled")
        self.boton_buscar.configure(state="disabled")

    def habilitar_ui(self):
        for boton in self.botones_menu:
            boton.configure(state="normal")
        self.boton_buscar.configure(state="normal")

        # Solo configuramos el color si es un widget de CTk
        if isinstance(self.master, ctk.CTk):
            self.master.configure(fg_color="#1e1e1e")



