import psycopg2
from dotenv import load_dotenv
import os

class ConexionPostgres:
    def __init__(self):
        load_dotenv()  # Carga las variables del .env
        self.connection = None

    def conectar(self):
        try:
            DATABASE_URL = os.getenv("DATABASE_URL") # EStablece el url del .env
            print(os.getenv("DATABASE_URL"))
            self.connection = psycopg2.connect(DATABASE_URL) # Conexión
            print("✅ Conexión exitosa a Supabase")
        except Exception as ex:
            print(f"❌ Error al conectar: {ex}")

    def cerrar_conexion(self): # Función para cerrar la conexión
        if self.connection:
            self.connection.close()
            print("🔒 Conexión cerrada")

    def ejecutar_consulta(self, consulta, parametros=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(consulta, parametros)
                return cursor.fetchall()
        except Exception as ex:
            print(f"❌ Error al ejecutar consulta: {ex}")
            return None
