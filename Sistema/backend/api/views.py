from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .oferta_service import OfertaManager
from rest_framework import generics

class OfertaListCreateView(generics.ListCreateAPIView):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer

class OfertaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer
    lookup_field = 'id_oferta'

class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    lookup_field = 'id_cliente'

class CatalogoProvinciasListCreateView(generics.ListCreateAPIView):
    queryset = CatalogoProvincias.objects.all()
    serializer_class = CatalogoProvinciasSerializer

class CatalogoProvinciasDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CatalogoProvincias.objects.all()
    serializer_class = CatalogoProvinciasSerializer
    lookup_field = 'id_provincia'

@api_view(['POST'])
def create_oferta(request):
    try:
        id_cliente = request.data.get('id_cliente')
        cliente = Cliente.objects.get(id_cliente=id_cliente)
        provincia = request.data.get('provincia')
        
        oferta = OfertaManager.create_oferta(cliente, provincia)
        
        serializer = OfertaSerializer(oferta)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class ActividadClienteListCreateView(generics.ListCreateAPIView):
    queryset = ActividadCliente.objects.all()
    serializer_class = ActividadClienteSerializer

@api_view(['GET'])
def oferta_detalle_completo(request, id_oferta):
    try:
        oferta = Oferta.objects.get(id_oferta=id_oferta)
        coberturas = OfertaCobertura.objects.filter(id_oferta=id_oferta)
        
        cobertura_data = []
        for cobertura in coberturas:
            cobertura_data.append({
                "nombre_cobertura": cobertura.id_cobertura.nombre_cobertura,
                "franquicia": cobertura.id_franquicia.franquicia,
                "sublimite": cobertura.id_sublimite.sublimite
            })
        
        data = {
            "id_oferta": oferta.id_oferta,
            "nombre_cliente": oferta.id_cliente.nombre_cliente,
            "suma_asegurada": oferta.suma_asegurada,
            "limite_anualidad": oferta.limite_anualidad,
            "coberturas": cobertura_data
        }
        
        return Response(data, status=status.HTTP_200_OK)
    except Oferta.DoesNotExist:
        return Response({'error': 'Oferta not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def ofertas_disponibles(request):
    try:
        ofertas = Oferta.objects.all()
        data = []
        for oferta in ofertas:
            data.append({
                "id_oferta": oferta.id_oferta,
                "id_cliente": oferta.id_cliente.id_cliente,
                "nombre_cliente": oferta.id_cliente.nombre_cliente
            })
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ofertas_por_cliente(request, id_cliente):
    try:
        cliente = Cliente.objects.get(id_cliente=id_cliente)
        ofertas = Oferta.objects.filter(id_cliente=cliente)
        data = []
        for oferta in ofertas:
            numero_coberturas = OfertaCobertura.objects.filter(id_oferta=oferta).count()
            data.append({
                "id_oferta": oferta.id_oferta,
                "suma_asegurada": oferta.suma_asegurada,
                "numero_coberturas": numero_coberturas
            })
        return Response(data, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response({'error': 'Cliente not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def actividades_list(request):
    try:
        actividades = CatalogoActividades.objects.all()
        data = []
        for actividad in actividades:
            data.append({
                "nombre_actividad": actividad.nombre_actividad
            })
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def provincias_list(request):
    try:
        provincias = CatalogoProvincias.objects.all()
        data = []
        for provincia in provincias:
            data.append({
                "nombre_provincia": provincia.provincia
            })
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
