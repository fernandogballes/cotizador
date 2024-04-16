from Actividades import Actividades
from Cliente import Cliente
from bbdd.Connection import Connection
import itertools
import unicodedata
import sys

def text_to_num(text):
    try:
        num = float(text)
        return num
    except ValueError:
        print('El valor introducido no es un numero, por favor ingrese un valor correcto.')
        return False
    
def activity_format(activitie):
    normalized_string = unicodedata.normalize('NFKD', activitie)
    stripped_string = ''.join(c for c in normalized_string if not unicodedata.combining(c))
    formatted_string = stripped_string.lower()
    words = formatted_string.split()
    formatted_string = "".join(words)    
    return formatted_string

def insert_activities():
    ddbb_connection = Connection()

    print("A continuacion introduce de una en una las actividades que realiza la empresa, escriba salir cuando ya no quiera introducir ninguna mas.")

    activities_ids = []
    activity = ''
    while activity != 'salir':
        activity = input("Introduzca una nueva actividad o salir en caso de no querer introducir ninguna mas: ")
        activity = activity_format(activity)

        try:
            query = f"SELECT id_actividad FROM catalogo_actividades WHERE nombre_actividad = {activity}"
            id_activity = ddbb_connection.execute_query(query)
            activities_ids.append(id_activity)

        except:
            print("No existe ninguna actividad con ese nombre.")

    # Añadir a la tabla actividad_empresa (cambiar empresa por cliente) todas las actividades, cada fila id_cliente, id_actividad
    

    return 1

def create_client():
    name = input("\nIntroduzca el nombre de la empresa: ")
    invoicing_volume = '' # Volumen de facturacion

    while text_to_num(invoicing_volume) == False:
        invoicing_volume=input("Intproduzca el volumen de facturacion de la empresa: ") 

    activities = insert_activities()
    client  = Cliente(name, invoicing_volume, activities)

    return 1

def consult_data_client():
    return 1

def list_clients():
    return 1

def list_activities():
    return 1

def menu():
    while True:
        option = input('Select option: ')

        if option == '1': create_client()
        elif option == '2': consult_data_client()
        elif option == '3': list_clients()
        elif option == '4': list_activities()
        elif option == '99': break
        else: print('Option not valid')

    return 1

if __name__== '__main__':
    menu()