from frontend.app import Interfaz
from backend.database import ConexionPostgres

def main():
    # Establecer conexión a la base de datos
    db = ConexionPostgres()
    db.conectar()  # Intenta conectar a Supabase

    # Iniciar la aplicación gráfica
    app = Interfaz()
    app.mainloop()  # Arranca la UI

    # Cerrar la conexión al salir
    db.cerrar_conexion()

if __name__ == "__main__":
    main()
