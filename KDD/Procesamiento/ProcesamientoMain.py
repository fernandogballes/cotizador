import ProcesamientoATR as ATR
import ProcesamientoPoblacion as Poblacion
import ProcesamientoTrafico as Trafico
import ProcesamientoGold as Gold

if __name__ == '__main__':
    print('Procesando Accidentes de Trabajo...')
    ATR.create_atr_2001_2022()
    print('Procesando datos poblacionales...')
    Poblacion.create_poblacion_ocupada_activa_2002_2023()
    print('Procesando Accidentes de Tráfico...')
    Trafico.create_accidentes_trafico()
    print('Creando capa GOLD...')
    Gold.create_gold()