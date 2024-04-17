from Actividades import Actividades
from Actividad import Actividad
from Cobertura import Cobertura
import itertools
from Poliza import Poliza
from Cliente import Cliente
import json

class Reglas:        
    #Calcula la suma asegurada de la poliza. Devuelve un float con la suma asegurada.
    # Función para obtener sumaAsegurada según volumen_facturacion
    def obtener_suma_asegurada(volumen_facturacion):
        with open('agravada_mapping.json', 'r') as file:
            agravada_mapping = json.load(file)
        with open('no_agravada_mapping.json', 'r') as file:
            no_agravada_mapping = json.load(file)

        # Buscar el rango adecuado en el mapeo
        for limite, suma_asegurada in sorted(agravada_mapping.items(), key=lambda x: int(x[0])):
            if volumen_facturacion <= float(limite):
                return suma_asegurada
        
        # Si no se encuentra ningún rango, retornar el último valor (por seguridad)
        return suma_asegurada
    
    # METODO ANTIGUO
    def calcularSumaAsegurada(cliente):
        if cliente._agravada==0:
            if cliente.volumen_facturacion<=150000.0: sumaAsegurada=150000.0
            elif cliente.volumen_facturacion>150000.0 and cliente.volumen_facturacion<=300000.0: sumaAsegurada=300000.0
            elif cliente.volumen_facturacion>300000.0 and cliente.volumen_facturacion<=1000000.0: sumaAsegurada=600000.0
            elif cliente.volumen_facturacion>1000000.0 and cliente.volumen_facturacion<=2000000.0: sumaAsegurada=1000000.0
            elif cliente.volumen_facturacion>2000000.0 and cliente.volumen_facturacion<=3000000.0: sumaAsegurada=2000000.0
            elif cliente.volumen_facturacion>3000000.0 and cliente.volumen_facturacion<=4000000.0: sumaAsegurada=3000000.0
            elif cliente.volumen_facturacion>4000000.0 and cliente.volumen_facturacion<=5000000.0: sumaAsegurada=4000000.0
            elif cliente.volumen_facturacion>5000000.0 and cliente.volumen_facturacion<=10000000.0: sumaAsegurada=6000000.0
            elif cliente.volumen_facturacion>10000000.0 and cliente.volumen_facturacion<=15000000.0: sumaAsegurada=8000000.0
        else:
            if cliente.volumen_facturacion<=150000.0: sumaAsegurada=300000.0
            elif cliente.volumen_facturacion>150000.0 and cliente.volumen_facturacion<=300000.0: sumaAsegurada=600000.0
            elif cliente.volumen_facturacion>300000.0 and cliente.volumen_facturacion<=1000000.0: sumaAsegurada=1000000.0
            elif cliente.volumen_facturacion>1000000.0 and cliente.volumen_facturacion<=2000000.0: sumaAsegurada=2000000.0
            elif cliente.volumen_facturacion>2000000.0 and cliente.volumen_facturacion<=3000000.0:sumaAsegurada=3000000.0
            elif cliente.volumen_facturacion>3000000.0 and cliente.volumen_facturacion<=4000000.0:sumaAsegurada=4000000.0
            elif cliente.volumen_facturacion>4000000.0 and cliente.volumen_facturacion<=5000000.0:sumaAsegurada=6000000.0
            elif cliente.volumen_facturacion>5000000.0 and cliente.volumen_facturacion<=10000000.0:sumaAsegurada=8000000.0
            elif cliente.volumen_facturacion>10000000.0 and cliente.volumen_facturacion<=15000000.0:sumaAsegurada=10000000.0

        return sumaAsegurada
    
    def rc_explotacion(poliza, actividad):
        if actividad in Actividades.listaActividades # and 'RC Explotación' not in listCobert:     
            #Calculo de la franquicia de la cobertura
            if poliza.volumen_facturacion<=600000.0: franquicia='300 o 600'
            if poliza.volumen_facturacion>600000 and poliza.volumen_facturacion<=4000000.0: franquicia='600 o 1500'
            if poliza.volumen_facturacion>4000000 and poliza.volumen_facturacion<=15000000.0 and actividad._agravada==0: franquicia='1500 o 3000'
            if poliza.volumen_facturacion>4000000 and poliza.volumen_facturacion<=15000000.0 and actividad._agravada==1: franquicia='3000 o 6000'
            #calculo del sublimite de la cobertura
            sublimite = poliza.suma_asegurada

            # listCobert.append(Cobertura(nombre,sublimite,franquicia))
            franquicia_explotacion = franquicia

        return Cobertura('RC Explotación', sublimite, franquicia)
        
    def rc_accidentes_de_trabajo(poliza, actividad):
        if actividad in Actividades.listaActividades # and 'RC Accidentes de trabajo' not in listCobert:
            nombre='RC Accidentes de trabajo'
            #Calculo de la franquicia de la cobertura
            franquicia='Sin franquicia'
            #calculo del sublimite de la cobertura
            #Sin agravado
            if poliza.suma_asegurada==150000 or poliza.suma_asegurada==300000 and actividad._agravada==0: sublimite=150000
            if poliza.suma_asegurada==600000 and actividad._agravada==0: sublimite=300000
            if poliza.suma_asegurada>=1000000 and poliza.suma_asegurada<=6000000 and actividad._agravada==0: sublimite=600000
            if poliza.suma_asegurada==8000000 and actividad._agravada==0: sublimite=750000
            #Con agravado
            if poliza.suma_asegurada==1000000 or poliza.suma_asegurada==2000000 and actividad._agravada==1: sublimite=600000
            if poliza.suma_asegurada>=3000000 and poliza.suma_asegurada<=10000000 and actividad._agravada==1: sublimite=750000
             
            sublimite_acctidentes=sublimite
                
        return Cobertura('RC Accidentes de trabajo', sublimite, franquicia)

    def rc_post_trabajos(poliza, actividad):
        if actividad in Actividades.listaActividades # and 'RC Post-trabajos' not in listCobert:
            return Cobertura('RC Post-trabajos', poliza.suma_asegurada, franquicia_explotacion)) # hacer consuta para enocntrar la cobertura de explotacion para obtener valor de la franquicia
    
    def rc_derribos(poliza, actividad):
        if actividad in Actividades.listaDerribos # and 'RC Derribos' not in listCobert:
            #Calculo de la franquicia de la cobertura
            if poliza.volumen_facturacion<=600000.0: franquicia='1500'
            if poliza.volumen_facturacion>600000 and poliza.volumen_facturacion<=4000000.0: franquicia='10% minimo 1500 maximo 3000'
            if poliza.volumen_facturacion>4000000 and poliza.volumen_facturacion<=15000000.0 and actividad._agravada==0: franquicia='20% minimo 1500 maximo 3000'
            if poliza.volumen_facturacion>4000000 and poliza.volumen_facturacion<=15000000.0 and actividad._agravada==1: franquicia='20% minimo 3000 maximo 6000'
            #calculo del sublimite de la cobertura
            sublimite = poliza.suma_asegurada/2

        return Cobertura('RC Derribos', sublimite, franquicia)
    
    def rc_conducciones(poliza, actividad):
        if actividad in Actividades.listaConducciones # and 'RC Conducciones' not in listCobert:
            #Calculo de la franquicia de la cobertura
            if poliza.volumen_facturacion<=600000.0: franquicia='1500'
            if poliza.volumen_facturacion>600000 and poliza.volumen_facturacion<=4000000.0: franquicia='10% minimo 1500 maximo 3000'
            if poliza.volumen_facturacion>4000000 and poliza.volumen_facturacion<=15000000.0 and actividad._agravada==0: franquicia='20% minimo 1500 maximo 3000'
            if poliza.volumen_facturacion>4000000 and poliza.volumen_facturacion<=15000000.0 and actividad._agravada==1: franquicia='20% minimo 3000 maximo 6000'
            #calculo del sublimite de la cobertura
            sublimite = poliza.suma_asegurada/2

        return Cobertura('RC Conducciones', sublimite, franquicia)
    
    def rc_trabajos_en_caliente(poliza, actividad):
        if actividad in Actividades.listaTrabajosCaliente # and 'RC Trabajos en caliente' not in listCobert:
            #Calculo de la franquicia de la cobertura
            if poliza.volumen_facturacion<=600000.0: franquicia='1500'
            if poliza.volumen_facturacion>600000 and poliza.volumen_facturacion<=4000000.0: franquicia='10% minimo 1500 maximo 3000'
            if poliza.volumen_facturacion>4000000 and poliza.volumen_facturacion<=15000000.0 and actividad._agravada==0: franquicia='20% minimo 1500 maximo 3000'
            if poliza.volumen_facturacion>4000000 and poliza.volumen_facturacion<=15000000.0 and actividad._agravada==1: franquicia='20% minimo 3000 maximo 6000'
            #calculo del sublimite de la cobertura
            if poliza.suma_asegurada==150000 or poliza.suma_asegurada==300000: sublimite=90000
            if poliza.suma_asegurada==600000 or poliza.suma_asegurada==1000000: sublimite=150000
            if poliza.suma_asegurada>=1000000 and poliza.suma_asegurada<=6000000: sublimite=300000
            if poliza.suma_asegurada>=3000000 and poliza.suma_asegurada<=6000000 and actividad._agravada==0: sublimite=600000
            if poliza.suma_asegurada==10000000 or poliza.suma_asegurada==8000000: sublimite=2000000
            if poliza.suma_asegurada==2000000 and actividad._agravada==1: sublimite=600000
            if poliza.suma_asegurada>=3000000 and poliza.suma_asegurada<=6000000 and actividad._agravada==1: sublimite=100000

        return Cobertura('RC Trabajos en caliente', sublimite, franquicia)
    
    def rc_locativa(poliza, actividad):
        if actividad in Actividades.listaLocativa # and 'RC Locativa' not in listCobert:
            #Calculo de la franquicia de la cobertura
            franquicia = franquicia_explotacion
            #calculo del sublimite de la cobertura
            if poliza.suma_asegurada==150000: sublimite=90000
            if poliza.suma_asegurada==300000: sublimite=150000
            if poliza.suma_asegurada>=600000 and poliza.suma_asegurada<=3000000: sublimite=300000
            if poliza.suma_asegurada>=400000 and poliza.suma_asegurada<=7000000: sublimite=600000
            if poliza.suma_asegurada==800000 and poliza.suma_asegurada==10000000: sublimite=1000000

        return Cobertura('RC Locativa', sublimite, franquicia)
    
    def rc_contaminacion_accidental(poliza, actividad):
        if actividad in Actividades.listaContaminacion # and 'RC Contaminación accidental' not in listCobert:
            #Calculo de la franquicia de la cobertura
            franquicia = franquicia_explotacion
            #calculo del sublimite de la cobertura
            if poliza.suma_asegurada==150000: sublimite=90000
            if poliza.suma_asegurada>=300000 and poliza.suma_asegurada<=1000000: sublimite=150000
            if poliza.suma_asegurada==2000000: sublimite=300000
            if poliza.suma_asegurada==3000000: sublimite=600000
            if poliza.suma_asegurada>=4000000 and poliza.suma_asegurada<=10000000: sublimite=1000000

        return Cobertura('RC Contaminación accidental', sublimite, franquicia)
    
    def rc_subsidiaria(poliza, actividad):
        if actividad in Actividades.listaSubsidiaria # and 'RC Subsidiaria' not in listCobert:
            sublimite=sublimite_acctidentes

        return Cobertura('RC Subsidiaria', sublimite, 'Sin limite')
    
    def rc_danios_a_las_redes_publicas(poliza, actividad):
        if actividad in Actividades.listaRedes # and 'RC Daños a las redes de comunicaciones públicas' not in listCobert:
            #Calculo de la franquicia de la cobertura
            franquicia=franquicia_explotacion
            #calculo del sublimite de la cobertura
            if poliza.suma_asegurada>=150000 and poliza.suma_asegurada<=300000: sublimite=90000
            if poliza.suma_asegurada==600000: sublimite=150000
            if poliza.suma_asegurada>=1000000 and poliza.suma_asegurada<=10000000: sublimite=300000

        return Cobertura('RC Daños a las redes de comunicaciones públicas', sublimite, franquicia)
    
    # METODO ANTIGUO
    #Metodo que evalua las actividades para ver que coberturas son necesarias y calcula la franquicia y el sublimite de cada una. Devuelve una lista de objeto cobertura.
    def coberturas(cliente, sumaAsegurada):
        listCobert=[]
        for act in cliente._actividades:
            if act in Actividades.listaActividades and 'RC Explotación' not in listCobert:
                nombre='RC Explotación'
                #Calculo de la franquicia de la cobertura
                if cliente.volumen_facturacion<=600000.0: franquicia='300 o 600'
                if cliente.volumen_facturacion>600000 and cliente.volumen_facturacion<=4000000.0: franquicia='600 o 1500'
                if cliente.volumen_facturacion>4000000 and cliente.volumen_facturacion<=15000000.0 and cliente._agravada==0: franquicia='1500 o 3000'
                if cliente.volumen_facturacion>4000000 and cliente.volumen_facturacion<=15000000.0 and cliente._agravada==1: franquicia='3000 o 6000'
                #calculo del sublimite de la cobertura
                sublimite=sumaAsegurada

                listCobert.append(Cobertura(nombre,sublimite,franquicia))
                franquiciaExplotacion=franquicia
            
            if act in Actividades.listaActividades and 'RC Accidentes de trabajo' not in listCobert:
                nombre='RC Accidentes de trabajo'
                #Calculo de la franquicia de la cobertura
                franquicia='Sin franquicia'
                #calculo del sublimite de la cobertura
                #Sin agravado
                if sumaAsegurada==150000 or sumaAsegurada==300000 and cliente._agravada==0: sublimite=150000
                if sumaAsegurada==600000 and cliente._agravada==0: sublimite=300000
                if sumaAsegurada>=1000000 and sumaAsegurada<=6000000 and cliente._agravada==0: sublimite=600000
                if sumaAsegurada==8000000 and cliente._agravada==0: sublimite=750000
                #Con agravado
                if sumaAsegurada==1000000 or sumaAsegurada==2000000 and cliente._agravada==1: sublimite=600000
                if sumaAsegurada>=3000000 and sumaAsegurada<=10000000 and cliente._agravada==1: sublimite=750000
             
                listCobert.append(Cobertura(nombre,sublimite,franquicia))
                sublimiteAcctidentes=sublimite

            if act in Actividades.listaActividades and 'RC Post-trabajos' not in listCobert:
                nombre='RC Post-trabajos'
                listCobert.append(Cobertura(nombre,sumaAsegurada,franquiciaExplotacion))

            if act in Actividades.listaDerribos and 'RC Derribos' not in listCobert:
                nombre='RC Derribos'
                #Calculo de la franquicia de la cobertura
                if cliente.volumen_facturacion<=600000.0: franquicia='1500'
                if cliente.volumen_facturacion>600000 and cliente.volumen_facturacion<=4000000.0: franquicia='10% minimo 1500 maximo 3000'
                if cliente.volumen_facturacion>4000000 and cliente.volumen_facturacion<=15000000.0 and cliente._agravada==0: franquicia='20% minimo 1500 maximo 3000'
                if cliente.volumen_facturacion>4000000 and cliente.volumen_facturacion<=15000000.0 and cliente._agravada==1: franquicia='20% minimo 3000 maximo 6000'
                #calculo del sublimite de la cobertura
                sublimite=sumaAsegurada/2

                listCobert.append(Cobertura(nombre,sublimite,franquicia))

            if act in Actividades.listaConducciones and 'RC Conducciones' not in listCobert:
                nombre='RC Conducciones'
                #Calculo de la franquicia de la cobertura
                if cliente.volumen_facturacion<=600000.0: franquicia='1500'
                if cliente.volumen_facturacion>600000 and cliente.volumen_facturacion<=4000000.0: franquicia='10% minimo 1500 maximo 3000'
                if cliente.volumen_facturacion>4000000 and cliente.volumen_facturacion<=15000000.0 and cliente._agravada==0: franquicia='20% minimo 1500 maximo 3000'
                if cliente.volumen_facturacion>4000000 and cliente.volumen_facturacion<=15000000.0 and cliente._agravada==1: franquicia='20% minimo 3000 maximo 6000'
                #calculo del sublimite de la cobertura
                sublimite=sumaAsegurada/2

                listCobert.append(Cobertura(nombre,sublimite,franquicia))
    
            if act in Actividades.listaTrabajosCaliente and 'RC Trabajos en caliente' not in listCobert:
                nombre='RC Trabajos en caliente'
                #Calculo de la franquicia de la cobertura
                if cliente.volumen_facturacion<=600000.0: franquicia='1500'
                if cliente.volumen_facturacion>600000 and cliente.volumen_facturacion<=4000000.0: franquicia='10% minimo 1500 maximo 3000'
                if cliente.volumen_facturacion>4000000 and cliente.volumen_facturacion<=15000000.0 and cliente._agravada==0: franquicia='20% minimo 1500 maximo 3000'
                if cliente.volumen_facturacion>4000000 and cliente.volumen_facturacion<=15000000.0 and cliente._agravada==1: franquicia='20% minimo 3000 maximo 6000'
                #calculo del sublimite de la cobertura
                if sumaAsegurada==150000 or sumaAsegurada==300000: sublimite=90000
                if sumaAsegurada==600000 or sumaAsegurada==1000000: sublimite=150000
                if sumaAsegurada>=1000000 and sumaAsegurada<=6000000: sublimite=300000
                if sumaAsegurada>=3000000 and sumaAsegurada<=6000000 and cliente._agravada==0: sublimite=600000
                if sumaAsegurada==10000000 or sumaAsegurada==8000000: sublimite=2000000
                if sumaAsegurada==2000000 and cliente._agravada==1: sublimite=600000
                if sumaAsegurada>=3000000 and sumaAsegurada<=6000000 and cliente._agravada==1: sublimite=100000

                listCobert.append(Cobertura(nombre,sublimite,franquicia))

            if act in Actividades.listaLocativa and 'RC Locativa' not in listCobert:
                nombre='RC Locativa'
                #Calculo de la franquicia de la cobertura
                franquicia=franquiciaExplotacion
                #calculo del sublimite de la cobertura
                if sumaAsegurada==150000: sublimite=90000
                if sumaAsegurada==300000: sublimite=150000
                if sumaAsegurada>=600000 and sumaAsegurada<=3000000: sublimite=300000
                if sumaAsegurada>=400000 and sumaAsegurada<=7000000: sublimite=600000
                if sumaAsegurada==800000 and sumaAsegurada==10000000: sublimite=1000000

                listCobert.append(Cobertura(nombre,sublimite,franquicia))

            if act in Actividades.listaContaminacion and 'RC Contaminación accidental' not in listCobert:
                nombre='RC Contaminación accidental'
                #Calculo de la franquicia de la cobertura
                franquicia=franquiciaExplotacion
                #calculo del sublimite de la cobertura
                if sumaAsegurada==150000: sublimite=90000
                if sumaAsegurada>=300000 and sumaAsegurada<=1000000: sublimite=150000
                if sumaAsegurada==2000000: sublimite=300000
                if sumaAsegurada==3000000: sublimite=600000
                if sumaAsegurada>=4000000 and sumaAsegurada<=10000000: sublimite=1000000

                listCobert.append(Cobertura(nombre,sublimite,franquicia))

            if act in Actividades.listaRedes and 'RC Daños a las redes de comunicaciones públicas' not in listCobert:
                nombre='RC Daños a las redes de comunicaciones públicas'
                #Calculo de la franquicia de la cobertura
                franquicia=franquiciaExplotacion
                #calculo del sublimite de la cobertura
                if sumaAsegurada>=150000 and sumaAsegurada<=300000: sublimite=90000
                if sumaAsegurada==600000: sublimite=150000
                if sumaAsegurada>=1000000 and sumaAsegurada<=10000000: sublimite=300000

                listCobert.append(Cobertura(nombre,sublimite,franquicia))

            if act in Actividades.listaSubsidiaria and 'RC Subsidiaria' not in listCobert:
                nombre='RC Subsidiaria'
                franquicia='Sin limite'
                sublimite=sublimiteAcctidentes
                listCobert.append(Cobertura(nombre,sublimite,franquicia))

        return listCobert