from Actividades import Actividades
from Actividad import Actividad
from Cobertura import Cobertura
from bbdd.code.Connection import Connection
import itertools
from Poliza import Poliza
from Cliente import Cliente
import json

def extract_coberturas(id_cliente):
    agravada_flag = 'false'
    ids_actividades = Connection().execute_select_query(f"SELECT id_actividad FROM actividad_cliente WHERE id_cliente = {id_cliente}")

    ids_coberturas = []
    for id_actividad in ids_actividades:
        ids_coberturas.append(Connection().execute_select_query(f"SELECT DISTINCT id_cobertura FROM actividad_cobertura WHERE id_actividad = {id_actividad}"))
        #if agravada_flag == 'false': agravada_flag = Connection().execute_select_query(f"SELECT agravada_flag FROM catalogo_actividades WHERE id_actividad = {id_actividad}")

    ids_coberturas = list(set(ids_coberturas))

    agravada_query = f"SELECT 1
                        FROM actividad_cliente ac
                        JOIN catalogo_actividades ca ON ac.id_actividad = ca.id_actividad
                        WHERE ac.id_cliente = {id_cliente} AND ca.agravada_flag = True
                        LIMIT 1"
    
    agravada_flag = bool(Connection().execute_select_query(agravada_query))

    return ids_coberturas, agravada_flag

def extract_client_info(id_cliente, id_oferta):
    ids_coberturas, agravada_flag = extract_coberturas(id_cliente)
    volumen_facturacion = Connection().execute_select_query(f"SELECT volumen_facturacion FROM clientes WHERE id_cliente = {id_cliente}")
    suma_asegurada = Connection().execute_select_query(f"SELECT volumen_facturacion FROM ofertas WHERE id_oferta = {id_oferta} AND id_cliente = {id_cliente}")
    #agravada_flag = Connection().execute_select_query(f"WITH actividad_agravadas AS (SELECT id_actividad, agravada_flag FROM catalogo_actividades WHERE agravada_flag = true) SELECT  ")

    return ids_coberturas, agravada_flag, volumen_facturacion, suma_asegurada


def create_oferta_poliza(id_cliente, id_oferta):
    ids_coberturas, agravada_flag, volumen_facturacion, suma_asegurada = extract_client_info(id_cliente, id_oferta)

    for id_cobertura in ids_coberturas:
        if id_cobertura == 1: id_franquicia, id_sublimite = rc_explotacion(volumen_facturacion, suma_asegurada, agravada_flag)
        if id_cobertura == 2: id_franquicia, id_sublimite = rc_accidentes_de_trabajo(suma_asegurada)
        if id_cobertura == 3: id_franquicia, id_sublimite = rc_pots_trabajos(suma_asegurada)
        if id_cobertura == 4: id_franquicia, id_sublimite = rc_derribos(volumen_facturacion)
        if id_cobertura == 5: id_franquicia, id_sublimite = rc_conducciones(volumen_facturacion)
        if id_cobertura == 6: id_franquicia, id_sublimite = rc_trabajos_en_caliente(volumen_facturacion)
        if id_cobertura == 7: id_franquicia, id_sublimite = rc_locativa(suma_asegurada)
        if id_cobertura == 8: id_franquicia, id_sublimite = rc_contaminacion_accidental(suma_asegurada)
        if id_cobertura == 9: id_franquicia, id_sublimite = rc_subsidiaria(id_cliente)
        if id_cobertura == 10: id_franquicia, id_sublimite = rc_danos_redes_de_comunicaciones_publicas(suma_asegurada)
        else: print("Error: Numero de cobertura inesperado")

        insert_cobertura_query = f"INSERT INTO oferta_cobertura (id_oferta, id_cobertura, id_franquicia, id_sublimite) VALUES ({id_oferta}, {id_cobertura}, {id_franquicia}, {id_sublimite})"
        Connection().execute_common_query(insert_cobertura_query)

    return 1

# INTRODUCCION DE LOS RANGOS EN LA BBDD
def rc_explotacion(volumen_facturacion, suma_asegurada, agravada_flag):
    if volumen_facturacion<=600000.0: franquicia='300 o 600'
    if volumen_facturacion>600000 and volumen_facturacion<=4000000.0: franquicia='600 o 1500'
    if volumen_facturacion>4000000 and volumen_facturacion<=15000000.0 and agravada_flag=='false': franquicia='1500 o 3000'
    if volumen_facturacion>4000000 and volumen_facturacion<=15000000.0 and agravada_flag=='true': franquicia='3000 o 6000'
    
    sublimite = str(suma_asegurada)

    id_franquicia = select_id_franquicia(franquicia)
    id_sublimite = select_id_sublimite(sublimite)

    return id_franquicia, id_sublimite

def rc_accidentes_de_trabajo(suma_asegurada, agravada_flag):
    franquicia='Sin franquicia'
    #Sin agravado
    if suma_asegurada==150000 or suma_asegurada==300000 and agravada_flag=='false': sublimite='150000'
    if suma_asegurada==600000 and agravada_flag==0: sublimite='300000'
    if suma_asegurada>=1000000 and suma_asegurada<=6000000 and agravada_flag=='false': sublimite='600000'
    if suma_asegurada==8000000 and agravada_flag==0: sublimite='750000'
    #Con agravado
    if suma_asegurada==1000000 or suma_asegurada==2000000 and agravada_flag=='true': sublimite='600000'
    if suma_asegurada>=3000000 and suma_asegurada<=10000000 and agravada_flag=='true': sublimite='750000'
    
    id_franquicia = select_id_franquicia(franquicia)
    id_sublimite = select_id_sublimite(sublimite)

    return id_franquicia, id_sublimite
    

def rc_pots_trabajos(id_cliente):
    return 1

def rc_derribos(id_cliente):
    return 1

def rc_conducciones(id_cliente):
    return 1

def rc_trabajos_en_caliente(id_cliente):
    return 1

def rc_locativa(id_cliente):
    return 1

def rc_contaminacion_accidental(id_cliente):
    return 1

def rc_subsidiaria(id_cliente):
    return 1

def rc_danos_redes_de_comunicaciones_publicas(id_cliente):
    return 1

def select_id_franquicia(franquicia):
    franquicia_explotacion_query = f"SELECT id_franquicia
                                    FROM franquicia_cobertura fc
                                    JOIN catalgo_franquicias cf
                                    ON fc.id_cobertura = cf.id_cobertura
                                    WHERE franquicia LIKE {franquicia}"
    
    franquicia = Connection().execute_select_query(franquicia_explotacion_query)

    return franquicia

def select_id_sublimite(sublimite):
    sublimite_explotacion_query = f"SELECT id_sublimite
                                    FROM sublimite_cobertura sc
                                    JOIN catalogo_sublimites cs
                                    ON sc.id_cobertura = cs.id_cobertura
                                    WHERE sublimite LIKE {sublimite}"
    id_sublimite = Connection().execute_select_query(sublimite_explotacion_query)

    return id_sublimite