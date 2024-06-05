import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import paths

def ddbb_connection_decorator(func):
    def wrapper(*args, **kwargs):
        conexion_db = Connection()
        try:
            conexion_db.connect()
            resultado = func(*args, **kwargs)
            return resultado
        finally:
            conexion_db.close_connect()
    return wrapper

class Connection:
    _instancia = None

    def __new__(cls, *args, **kwargs):
        if not cls._instancia:
            cls._instancia = super(Connection, cls).__new__(cls, *args, **kwargs)
        return cls._instancia

    def __init__(self):
        self.cnx = None
        self.config = self.read_ddbb_config()

    def connect(self):
        if not self.cnx or self.cnx.closed:
            try:
                self.cnx = psycopg2.connect(
                    user=self.config['user'],
                    password=self.config['password'],
                    host=self.config['host'],
                    port=int(self.config['port']),
                    database=self.config['database']
                )
                print("Conexión establecida correctamente")
            except psycopg2.Error as e:
                print(f"Error al conectar a la base de datos PostgreSQL: {e}")

    def close_connect(self):
        if self.cnx and not self.cnx.closed:
            self.cnx.close()
            print("Conexión cerrada")

    @ddbb_connection_decorator
    def execute_select_query(self, consulta):
        try:
            cursor = self.cnx.cursor()
            cursor.execute(consulta)
            results = cursor.fetchall()
            cursor.close()
            return results
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    @ddbb_connection_decorator
    def execute_common_query(self, consulta):
        try:
            cursor = self.cnx.cursor()
            cursor.execute(consulta)
            self.cnx.commit()
            cursor.close()
            print("Consulta ejecutada correctamente")
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta que no devuelve resultados: {e}")

    def read_ddbb_config(self):
        config = {
            'user': os.environ.get('DATABASE_USER', 'default_user'),
            'password': os.environ.get('DATABASE_PASSWORD', 'default_password'),
            'host': os.environ.get('DATABASE_HOST', 'localhost'),
            'port': os.environ.get('DATABASE_PORT', '5432'),
            'database': os.environ.get('DATABASE_NAME', 'default_database')
        }
        return config
