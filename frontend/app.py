import os
import customtkinter as ctk
from PIL import Image
from backend.database import ConexionPostgres as psql
import tkinter.ttk as ttk

rutaImagenLogoSanbirds = os.path.abspath("frontend/assets/LOGOSANBIRDSDB.png")
rutaIconoAgregar = os.path.abspath("frontend/assets/icon_add.png")
rutaIconoEditar = os.path.abspath("frontend/assets/icon_edit.png")
rutaIconoEliminar = os.path.abspath("frontend/assets/icon_delete.png")
naranja_claro = "#FF914D"  # un poco más claro
naranja_oscuro = "#CC5C1C"  # un poco más oscuro

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

    def insertar_datos(self, datos):
        for fila in datos:
            self.tree.insert("", "end", values=fila)

    def frame_superior(self):
        frame_top = ctk.CTkFrame(self, height=100)
        frame_top.pack(fill="x", padx=10, pady=(10, 0))

        contenedor_logo = ctk.CTkFrame(frame_top)
        contenedor_logo.pack(pady=15, padx=20, side="left")

        logo = ctk.CTkImage(Image.open(rutaImagenLogoSanbirds), size=(250, 120))
        logo_label = ctk.CTkLabel(contenedor_logo, image=logo, text="")
        logo_label.pack(side="left", padx=10)

        contenedor_botones = ctk.CTkFrame(frame_top)
        contenedor_botones.pack(pady=15, padx=20, side="right")

        icono_add = ctk.CTkImage(Image.open(rutaIconoAgregar), size=(20, 20))
        icono_edit = ctk.CTkImage(Image.open(rutaIconoEditar), size=(20, 20))
        icono_delete = ctk.CTkImage(Image.open(rutaIconoEliminar), size=(20, 20))

        self.boton_agregar = ctk.CTkButton(
            contenedor_botones,
            text="Agregar",
            image=icono_add,
            compound="left",
            command=self.abrir_ventana_agregar,
            fg_color=naranja_claro,
            hover_color=naranja_oscuro
        )

        self.boton_editar = ctk.CTkButton(
            contenedor_botones,
            text="Editar",
            image=icono_edit,
            compound="left",
            command=self.abrir_ventana_editar,
            fg_color=naranja_claro,
            hover_color=naranja_oscuro
        )

        self.boton_eliminar = ctk.CTkButton(
            contenedor_botones,
            text="Eliminar",
            image=icono_delete,
            compound="left",
            command=self.eliminar_registro,
            fg_color=naranja_claro,
            hover_color=naranja_oscuro
        )


        self.boton_eliminar.pack(side="right", padx=10)
        self.boton_editar.pack(side="right", padx=10)
        self.boton_agregar.pack(side="right", padx=10)

    def area_resultados(self):
        frame_body = ctk.CTkFrame(self)
        frame_body.pack(expand=True, fill="both", padx=20, pady=10)

        self.frame_busqueda = ctk.CTkFrame(frame_body)
        self.frame_busqueda.pack(fill="x", pady=(0, 5))

        self.entry_busqueda = ctk.CTkEntry(self.frame_busqueda, placeholder_text="Buscar...")
        self.entry_busqueda.pack(side="left", padx=(10, 5), fill="x", expand=True)

        self.boton_buscar = ctk.CTkButton(
            self.frame_busqueda,
            text="Buscar",
            fg_color=naranja_claro,
            hover_color=naranja_oscuro,
            command=self.buscar_datos
        )
        self.boton_buscar.pack(side="right", padx=(5, 10))


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
                fg_color=naranja_claro,
                hover_color=naranja_oscuro,
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

        texto_busqueda = self.entry_busqueda.get().strip()

        try:
            with self.db.connection.cursor() as cursor:
                if texto_busqueda:
                    columnas = self.obtener_columnas()
                    condiciones = " OR ".join([f"{col}::text ILIKE %s" for col in columnas])
                    query = f"SELECT * FROM {self.tabla_seleccionada} WHERE {condiciones}"
                    valores = [f"%{texto_busqueda}%"] * len(columnas)
                    cursor.execute(query, valores)
                else:
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
        if not datos_seleccionados:
            return
        self.abrir_formulario("Editar", datos_seleccionados)

    def abrir_formulario(self, modo, datos=None):
        ventana = ctk.CTkToplevel(self)
        ventana.title(f"{modo} registro")
        ventana.geometry("400x400")
        ventana.configure(fg_color="#1e1e1e")

        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"+{x}+{y}")

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
                if valores != datos:
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
        self.boton_agregar.configure(state="disabled")
        self.boton_editar.configure(state="disabled")
        self.boton_eliminar.configure(state="disabled")

    def habilitar_ui(self):
        for boton in self.botones_menu:
            boton.configure(state="normal")
        self.boton_agregar.configure(state="normal")
        self.boton_editar.configure(state="normal")
        self.boton_eliminar.configure(state="normal")
        if isinstance(self.master, ctk.CTk):
            self.master.configure(fg_color="#1e1e1e")
