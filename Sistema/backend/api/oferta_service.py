from .models import *
import logging
logger = logging.getLogger('oferta_manager')
import datetime
import json
import joblib
import pandas as pd

class OfertaManager:
    @staticmethod
    def create_suma_asegurada_limite_anualidad(cliente):
        agravada_flag = OfertaManager.extract_agravada_flag(cliente.id_cliente)
        volumen_facturacion = cliente.volumen_facturacion
        
        if not agravada_flag:
            if volumen_facturacion <= 150000.0: suma_asegurada = 150000.0
            elif volumen_facturacion > 150000.0 and volumen_facturacion <= 300000.0: suma_asegurada = 300000.0
            elif volumen_facturacion > 300000.0 and volumen_facturacion <= 1000000.0: suma_asegurada = 600000.0
            elif volumen_facturacion > 1000000.0 and volumen_facturacion <= 2000000.0: suma_asegurada = 1000000.0
            elif volumen_facturacion > 2000000.0 and volumen_facturacion <= 3000000.0: suma_asegurada = 2000000.0
            elif volumen_facturacion > 3000000.0 and volumen_facturacion <= 4000000.0: suma_asegurada = 3000000.0
            elif volumen_facturacion > 4000000.0 and volumen_facturacion <= 5000000.0: suma_asegurada = 4000000.0
            elif volumen_facturacion > 5000000.0 and volumen_facturacion <= 10000000.0: suma_asegurada = 6000000.0
            elif volumen_facturacion > 10000000.0 and volumen_facturacion <= 15000000.0: suma_asegurada = 8000000.0
        else:
            if volumen_facturacion <= 150000.0: suma_asegurada = 300000.0
            elif volumen_facturacion > 150000.0 and volumen_facturacion <= 300000.0: suma_asegurada = 600000.0
            elif volumen_facturacion > 300000.0 and volumen_facturacion <= 1000000.0: suma_asegurada = 1000000.0
            elif volumen_facturacion > 1000000.0 and volumen_facturacion <= 2000000.0: suma_asegurada = 2000000.0
            elif volumen_facturacion > 2000000.0 and volumen_facturacion <= 3000000.0: suma_asegurada = 3000000.0
            elif volumen_facturacion > 3000000.0 and volumen_facturacion <= 4000000.0: suma_asegurada = 4000000.0
            elif volumen_facturacion > 4000000.0 and volumen_facturacion <= 5000000.0: suma_asegurada = 6000000.0
            elif volumen_facturacion > 5000000.0 and volumen_facturacion <= 10000000.0: suma_asegurada = 8000000.0
            elif volumen_facturacion > 10000000.0 and volumen_facturacion <= 15000000.0: suma_asegurada = 10000000.0

        limite_anualidad = suma_asegurada * 2
        return suma_asegurada, limite_anualidad

    @staticmethod
    def create_oferta(cliente, provincia):
        suma_asegurada, limite_anualidad = OfertaManager.create_suma_asegurada_limite_anualidad(cliente)
        semaforo = OfertaManager.predict_semaforo(provincia)
        
        oferta = Oferta.objects.create(
            id_cliente=cliente,
            suma_asegurada=suma_asegurada,
            limite_anualidad=limite_anualidad,
            semaforo=semaforo
        )
        
        OfertaManager.create_coberturas_oferta(oferta)
        return oferta
    
    @staticmethod
    def select_id_provincia(provincia):
        return CatalogoProvincias.objects.get(provincia=provincia).id_provincia
    
    @staticmethod
    def predict_semaforo(provincia):
        anio  = datetime.date.today().strftime("%Y")
        with open('test_interfaz/diccionario_comunidades_provincias.json', 'r') as file:
            comunidades_dict = json.load(file)
        
        comunidad_autonoma = comunidades_dict.get(provincia.lower(), "Comunidad no encontrada")
        semaforo = OfertaManager.use_model(anio, provincia, comunidad_autonoma)

        return semaforo
    
    @staticmethod
    def use_model(anio, provincia, comunidad_autonoma):
        with open('C:/Users/garci/proyectos/cotizador/KDD/Algoritmos/cluster_data/semaforo_dict.json', 'r') as file:
            semaforizacion_dict = json.load(file)
        rf_classifier = joblib.load('C:/Users/garci/proyectos/cotizador/KDD/Algoritmos/trained_models/random_forest_cluster_predictor.joblib')
        preprocessor = joblib.load('C:/Users/garci/proyectos/cotizador/KDD/Algoritmos/trained_models/preprocessor.joblib')
        
        new_data = pd.DataFrame({
            'anio': [anio],
            'provincia': [provincia],
            'comunidad_autonoma': [comunidad_autonoma]
        })
        # Preprocesar los nuevos datos
        X_new = preprocessor.transform(new_data)
        # Realizar predicción
        new_cluster_prediction = rf_classifier.predict(X_new)
        predicted_cluster = new_cluster_prediction[0]
        # Obtener el semáforo correspondiente al cluster predicho
        predicted_semaforo = semaforizacion_dict[str(predicted_cluster)]
        
        return predicted_semaforo


    @staticmethod
    def create_coberturas_oferta(oferta):
        id_cliente = oferta.id_cliente.id_cliente
        ids_coberturas, agravada_flag = OfertaManager.extract_coberturas(id_cliente)
        ids_coberturas = sorted(ids_coberturas)
        suma_asegurada = oferta.suma_asegurada
        volumen_facturacion = oferta.id_cliente.volumen_facturacion
        print(f"Creating OfertaCobertura: id_cliente={id_cliente}, id_oferta={oferta.id_oferta}, agravada_flag={agravada_flag}, suma asegurada={suma_asegurada}, volumen facturacion={volumen_facturacion}, ids_coberturas={ids_coberturas}")
        
        try:
            for id_cobertura in ids_coberturas:
                if id_cobertura == 1: id_franquicia, id_sublimite = OfertaManager.rc_explotacion(volumen_facturacion, suma_asegurada, agravada_flag)
                elif id_cobertura == 2: id_franquicia, id_sublimite = OfertaManager.rc_accidentes_de_trabajo(suma_asegurada, agravada_flag)
                elif id_cobertura == 3: id_franquicia, id_sublimite = OfertaManager.rc_post_trabajos(oferta.id_oferta, suma_asegurada)
                elif id_cobertura == 4: id_franquicia, id_sublimite = OfertaManager.rc_derribos(suma_asegurada, volumen_facturacion, agravada_flag)
                elif id_cobertura == 5: id_franquicia, id_sublimite = OfertaManager.rc_conducciones(suma_asegurada, volumen_facturacion, agravada_flag)
                elif id_cobertura == 6: id_franquicia, id_sublimite = OfertaManager.rc_trabajos_en_caliente(volumen_facturacion, suma_asegurada, agravada_flag)
                elif id_cobertura == 7: id_franquicia, id_sublimite = OfertaManager.rc_locativa(oferta.id_oferta, suma_asegurada)
                elif id_cobertura == 8: id_franquicia, id_sublimite = OfertaManager.rc_contaminacion_accidental(oferta.id_oferta, suma_asegurada)
                elif id_cobertura == 9: id_franquicia, id_sublimite = OfertaManager.rc_subsidiaria(oferta.id_oferta)
                elif id_cobertura == 10: id_franquicia, id_sublimite = OfertaManager.rc_danos_redes_de_comunicaciones_publicas(oferta.id_oferta, suma_asegurada)
                else:
                    raise ValueError(f"Unexpected coverage id: {id_cobertura}")

                print(f"Creating OfertaCobertura: id_oferta={oferta.id_oferta}, id_cobertura={id_cobertura}, id_franquicia={id_franquicia}, id_sublimite={id_sublimite}")

                OfertaCobertura.objects.create(
                    id_oferta=oferta,
                    id_cobertura=CatalogoCoberturas.objects.get(id_cobertura=id_cobertura),
                    id_franquicia=CatalogoFranquicias.objects.get(id_franquicia=id_franquicia),
                    id_sublimite=CatalogoSublimites.objects.get(id_sublimite=id_sublimite)
                )
        except Exception as e:
            logging.error(f"Error creating coverage for oferta {oferta.id_oferta}: {e}")

    @staticmethod
    def extract_coberturas(id_cliente):
        ids_coberturas = list(ActividadCobertura.objects.filter(
            id_actividad__in=ActividadCliente.objects.filter(id_cliente=id_cliente).values_list('id_actividad')
        ).values_list('id_cobertura', flat=True).distinct())
        agravada_flag = OfertaManager.extract_agravada_flag(id_cliente)
        return ids_coberturas, agravada_flag

    @staticmethod
    def extract_agravada_flag(id_cliente):
        return CatalogoActividades.objects.filter(
            id_actividad__in=ActividadCliente.objects.filter(id_cliente=id_cliente).values_list('id_actividad'),
            agravada_flag=True
        ).exists()

    @staticmethod
    def rc_explotacion(volumen_facturacion, suma_asegurada, agravada_flag):
        if volumen_facturacion <= 600000.0: franquicia = '300 a 600'
        if volumen_facturacion > 600000 and volumen_facturacion <= 4000000.0: franquicia = '600 a 1500'
        if volumen_facturacion > 4000000 and volumen_facturacion <= 15000000.0 and not agravada_flag: franquicia = '1500 a 3000'
        if volumen_facturacion > 4000000 and volumen_facturacion <= 15000000.0 and agravada_flag: franquicia = '3000 a 6000'
        
        sublimite = str(int(suma_asegurada))
        
        id_cobertura = OfertaManager.select_id_cobertura('RC Explotacion')
        id_franquicia = OfertaManager.select_id_franquicia(id_cobertura, franquicia)
        id_sublimite = OfertaManager.select_id_sublimite(id_cobertura, sublimite)
        
        return id_franquicia, id_sublimite

    @staticmethod
    def rc_accidentes_de_trabajo(suma_asegurada, agravada_flag):
        franquicia = 'Sin franquicia'
        # Sin agravado
        if (suma_asegurada == 150000 or suma_asegurada == 300000) and not agravada_flag: sublimite = '150000'
        if suma_asegurada == 600000 and not agravada_flag: sublimite = '300000'
        if suma_asegurada >= 1000000 and suma_asegurada <= 6000000 and not agravada_flag: sublimite = '600000'
        if suma_asegurada == 8000000 and not agravada_flag: sublimite = '750000'
        # Con agravado
        if (suma_asegurada == 1000000 or suma_asegurada == 2000000) and agravada_flag: sublimite = '600000'
        if suma_asegurada >= 3000000 and suma_asegurada <= 10000000 and agravada_flag: sublimite = '750000'
        
        id_cobertura = OfertaManager.select_id_cobertura('RC Accidentes de trabajo')
        id_franquicia = OfertaManager.select_id_franquicia(id_cobertura, franquicia)
        id_sublimite = OfertaManager.select_id_sublimite(id_cobertura, sublimite)

        return id_franquicia, id_sublimite

    @staticmethod
    def rc_post_trabajos(id_oferta, suma_asegurada):
        id_cobertura = OfertaManager.select_id_cobertura('RC Post-trabajos')
        id_franquicia = OfertaManager.select_franquicia_explotacion(id_oferta)
        id_sublimite = OfertaManager.select_id_sublimite(id_cobertura, str(int(suma_asegurada)))
        return id_franquicia, id_sublimite

    @staticmethod
    def rc_derribos(suma_asegurada, volumen_facturacion, agravada_flag):
        if volumen_facturacion <= 600000.0: franquicia = '1500'
        if volumen_facturacion > 600000 and volumen_facturacion <= 4000000.0: franquicia = '10% minimo 1500 maximo 3000'
        if volumen_facturacion > 4000000 and volumen_facturacion <= 15000000.0 and not agravada_flag: franquicia = '20% minimo 1500 maximo 3000'
        if volumen_facturacion > 4000000 and volumen_facturacion <= 15000000.0 and agravada_flag: franquicia = '20% minimo 3000 maximo 6000'
        sublimite = str(int(suma_asegurada / 2))
        
        id_cobertura = OfertaManager.select_id_cobertura('RC Derribos')
        id_franquicia = OfertaManager.select_id_franquicia(id_cobertura, franquicia)
        id_sublimite = OfertaManager.select_id_sublimite(id_cobertura, sublimite)
        
        return id_franquicia, id_sublimite

    @staticmethod
    def rc_conducciones(suma_asegurada, volumen_facturacion, agravada_flag):
        if volumen_facturacion <= 600000.0: franquicia = '1500'
        if volumen_facturacion > 600000 and volumen_facturacion <= 4000000.0: franquicia = '10% minimo 1500 maximo 3000'
        if volumen_facturacion > 4000000 and volumen_facturacion <= 15000000.0 and not agravada_flag: franquicia = '20% minimo 1500 maximo 3000'
        if volumen_facturacion > 4000000 and volumen_facturacion <= 15000000.0 and agravada_flag: franquicia = '20% minimo 3000 maximo 6000'
        sublimite = str(int(suma_asegurada / 2))
        
        id_cobertura = OfertaManager.select_id_cobertura('RC Conducciones')
        id_franquicia = OfertaManager.select_id_franquicia(id_cobertura, franquicia)
        id_sublimite = OfertaManager.select_id_sublimite(id_cobertura, sublimite)
        
        return id_franquicia, id_sublimite

    @staticmethod
    def rc_trabajos_en_caliente(volumen_facturacion, suma_asegurada, agravada_flag):
        if volumen_facturacion <= 600000.0: franquicia = '1500'
        if volumen_facturacion > 600000 and volumen_facturacion <= 4000000.0: franquicia = '10% minimo 1500 maximo 3000'
        if volumen_facturacion > 4000000 and volumen_facturacion <= 15000000.0 and not agravada_flag: franquicia = '20% minimo 1500 maximo 3000'
        if volumen_facturacion > 4000000 and volumen_facturacion <= 15000000.0 and agravada_flag: franquicia = '20% minimo 3000 maximo 6000'
        # Calculo del sublimite de la cobertura
        if suma_asegurada == 150000 or suma_asegurada == 300000: sublimite = '90000'
        if suma_asegurada == 600000 or suma_asegurada == 1000000: sublimite = '150000'
        if suma_asegurada >= 1000000 and suma_asegurada <= 6000000: sublimite = '300000'
        if suma_asegurada >= 3000000 and suma_asegurada <= 6000000 and not agravada_flag: sublimite = '600000'
        if suma_asegurada == 10000000 or suma_asegurada == 8000000: sublimite = '2000000'
        if suma_asegurada == 2000000 and agravada_flag: sublimite = '600000'
        if suma_asegurada >= 3000000 and suma_asegurada <= 6000000 and agravada_flag: sublimite = '100000'
        
        id_cobertura = OfertaManager.select_id_cobertura('RC Trabajos en caliente')
        id_franquicia = OfertaManager.select_id_franquicia(id_cobertura, franquicia)
        id_sublimite = OfertaManager.select_id_sublimite(id_cobertura, sublimite)
        return id_franquicia, id_sublimite

    @staticmethod
    def rc_locativa(id_oferta, suma_asegurada):
        if suma_asegurada == 150000: sublimite = '90000'
        if suma_asegurada == 300000: sublimite = '150000'
        if suma_asegurada >= 600000 and suma_asegurada <= 3000000: sublimite = '300000'
        if suma_asegurada >= 400000 and suma_asegurada <= 7000000: sublimite = '600000'
        if suma_asegurada == 800000 and suma_asegurada == 10000000: sublimite = '1000000'
        
        id_cobertura = OfertaManager.select_id_cobertura('RC Locativa')
        id_franquicia = OfertaManager.select_franquicia_explotacion(id_oferta)
        id_sublimite = OfertaManager.select_id_sublimite(id_cobertura, sublimite)
        return id_franquicia, id_sublimite

    @staticmethod
    def rc_contaminacion_accidental(id_oferta, suma_asegurada):
        if suma_asegurada == 150000: sublimite = '90000'
        if suma_asegurada >= 300000 and suma_asegurada <= 1000000: sublimite = '150000'
        if suma_asegurada == 2000000: sublimite = '300000'
        if suma_asegurada == 3000000: sublimite = '600000'
        if suma_asegurada >= 4000000 and suma_asegurada <= 10000000: sublimite = '1000000'
        
        id_cobertura = OfertaManager.select_id_cobertura('RC Contaminación accidental')
        id_franquicia = OfertaManager.select_franquicia_explotacion(id_oferta)
        id_sublimite = OfertaManager.select_id_sublimite(id_cobertura, sublimite)
        return id_franquicia, id_sublimite

    @staticmethod
    def rc_subsidiaria(id_oferta):
        franquicia = 'Sin franquicia'
        
        id_cobertura = OfertaManager.select_id_cobertura('RC Subsidiaria')
        id_accidentes = OfertaManager.select_id_cobertura('RC Accidentes de trabajo')
        
        id_sublimite = OfertaCobertura.objects.filter(id_oferta=id_oferta, id_cobertura=id_accidentes).values_list('id_sublimite', flat=True).first()
        id_franquicia = OfertaManager.select_id_franquicia(id_cobertura, franquicia)
        
        return id_franquicia, id_sublimite

    @staticmethod
    def rc_danos_redes_de_comunicaciones_publicas(id_oferta, suma_asegurada):
        if suma_asegurada >= 150000 and suma_asegurada <= 300000: sublimite = '90000'
        if suma_asegurada == 600000: sublimite = '150000'
        if suma_asegurada >= 1000000 and suma_asegurada <= 10000000: sublimite = '300000'
        
        id_cobertura = OfertaManager.select_id_cobertura('RC Daños a las redes de comunicaciones públicas')
        id_franquicia = OfertaManager.select_franquicia_explotacion(id_oferta)
        id_sublimite = OfertaManager.select_id_sublimite(id_cobertura, sublimite)
        
        return id_franquicia, id_sublimite

    @staticmethod
    def select_franquicia_explotacion(id_oferta):
        id_cobertura = OfertaManager.select_id_cobertura('RC Explotacion')
        franquicia = OfertaCobertura.objects.filter(id_oferta=id_oferta, id_cobertura=id_cobertura).values_list('id_franquicia', flat=True).first()
        return franquicia

    @staticmethod
    def select_id_cobertura(nombre_cobertura):
        return CatalogoCoberturas.objects.get(nombre_cobertura=nombre_cobertura).id_cobertura

    @staticmethod
    def select_id_franquicia(id_cobertura, franquicia):
        return CatalogoFranquicias.objects.get(
            franquicia=franquicia,
            franquiciacobertura__id_cobertura=id_cobertura
        ).id_franquicia

    @staticmethod
    def select_id_sublimite(id_cobertura, sublimite):
        return CatalogoSublimites.objects.get(
            sublimite=sublimite,
            sublimitecobertura__id_cobertura=id_cobertura
        ).id_sublimite
