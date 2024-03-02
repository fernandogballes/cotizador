import mysql.connector
import os

def ddbb_connection_decorator(func):
    def wrapper(*args, **kwargs):
        conexion_db = Connection() # Obtener la instancia única de la conexión a la base de datos

        try:
            conexion_db.connect()
            resultado = func(*args, **kwargs)
            return resultado
        
        finally:
            conexion_db.close_connect()

    return wrapper

class Connection:
    """
    Clase que encapsula la conexión a una base de datos MySQL local.
    on the basis of the configuration file located in the same class. """
    _instancia = None
    _config = None

    def __new__(cls, *args, **kwargs):
        if not cls._instancia:
            cls._instancia = super(Connection, cls).__new__(cls, *args, **kwargs)
        return cls._instancia

    def __init__(self):
        self.cnx = None
        self.config = read_ddbb_config('ddbb_config.txt')

    def connect(self):
        if not self.cnx or not self.cnx.is_connected():
            self.cnx = mysql.connector.connect(user=self.config['user'],
                                                password=self.config['password'],
                                                host=self.config['host'],
                                                database=self.config['database'])
            print("Conexión estabilizada")

    def close_connect(self):
        if self.cnx and self.cnx.is_connected():
            self.cnx.close()
            print("Conexión cerrada")

    @ddbb_connection_decorator
    def execute_query(self, consulta):
        cursor = self.cnx.cursor()
        cursor.execute(consulta)
        results = cursor.fetchall()
        cursor.close()
        return results

    def read_ddbb_config(self, file):
        config = {}
        with open(file, 'r') as f:
            for linea in f:
                # Dividir la línea en clave y valor
                clave, valor = linea.strip().strip(",").split('=')
                # Quitar comillas y espacios de los valores
                valor = valor.strip().strip("'")
                config[clave] = valor
        return config
