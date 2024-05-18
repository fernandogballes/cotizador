import psycopg2

def ddbb_connection_decorator(func):
    def wrapper(*args, **kwargs):
        conexion_db = Connection()  # Obtener la instancia única de la conexión a la base de datos

        try:
            conexion_db.connect()
            resultado = func(*args, **kwargs)
            return resultado
        
        finally:
            conexion_db.close_connect()

    return wrapper

class Connection:
    """
    Clase que encapsula la conexión a una base de datos PostgreSQL local.
    """
    _instancia = None
    _config = None

    def __new__(cls, *args, **kwargs):
        if not cls._instancia:
            cls._instancia = super(Connection, cls).__new__(cls, *args, **kwargs)
        return cls._instancia

    def __init__(self):
        self.cnx = None
        self.config = self.read_ddbb_config('bbdd/config/ddbb_config.txt')

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
        # Ejecuta una consulta que no devuelve resultados (INSERT, UPDATE, DELETE, CREATE, etc.).
        try:
            cursor = self.cnx.cursor()
            cursor.execute(consulta)
            self.cnx.commit()  # Confirmar los cambios en la base de datos
            cursor.close()
            print("Consulta ejecutada correctamente")
        except psycopg2.Error as e:
            print(f"Error al ejecutar la consulta que no devuelve resultados: {e}")

    def read_ddbb_config(self, file):
        config = {}
        with open(file, 'r') as f:
            for linea in f:
                # Dividir la línea en clave y valor
                if '=' in linea:
                    clave, valor = linea.strip().split('=')
                    # Quitar espacios adicionales alrededor de la clave y el valor
                    clave = clave.strip()
                    valor = valor.strip()
                    # Almacenar la clave y el valor en el diccionario de configuración
                    config[clave] = valor
        return config
