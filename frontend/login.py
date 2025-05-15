import customtkinter as ctk
from PIL import Image
import os

class LoginScreen(ctk.CTkToplevel):
    def __init__(self, master, db, on_login_success):
        super().__init__(master, fg_color="#C9A28D")
        
        self.db = db
        self.on_login_success = on_login_success
        self.title("Sanbirds DB")
        ancho = 500
        alto = 400
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.resizable(False, False)
        self.grab_set()


        # Colores personalizados
        naranja_claro = "#d07d44"
        naranja_oscuro = "#b4642d"

        # Frame de la izquierda: Imagen
        self.left_frame = ctk.CTkFrame(self, width=250, fg_color="#C9A28D")
        self.left_frame.pack(side="left", fill="both", expand=False)

        image_path = os.path.join("frontend", "assets", "login_image.png")
        image = ctk.CTkImage(light_image=Image.open(image_path), size=(250, 400))
        self.image_label = ctk.CTkLabel(self.left_frame, image=image, text="")
        self.image_label.pack(fill="both", expand=True)

        # Frame de la derecha: Formulario
        self.right_frame = ctk.CTkFrame(self, fg_color="#E5E5E5")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        self.label_user = ctk.CTkLabel(self.right_frame, text="Usuario", text_color="black")
        self.label_user.pack(pady=10)
        self.entry_user = ctk.CTkEntry(self.right_frame)
        self.entry_user.pack()

        self.label_pass = ctk.CTkLabel(self.right_frame, text="Contraseña", text_color="black")
        self.label_pass.pack(pady=10)
        self.entry_pass = ctk.CTkEntry(self.right_frame, show="*")
        self.entry_pass.pack()

        self.login_button = ctk.CTkButton(
            self.right_frame, 
            text="Iniciar sesión", 
            command=self.login,
            fg_color=naranja_claro, 
            hover_color=naranja_oscuro,
            text_color="white"
        )
        self.login_button.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

    def cerrar_aplicacion(self):
        self.master.destroy()

    def login(self):
        usuario = self.entry_user.get()
        contrasena = self.entry_pass.get()
        if self.db.verificar_usuario(usuario, contrasena):
            self.destroy()
            self.on_login_success()
        else:
            ctk.CTkLabel(self.right_frame, text="Usuario o contraseña incorrectos", text_color="red").pack()
