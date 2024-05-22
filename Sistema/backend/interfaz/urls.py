from django.urls import path
from .views import *

urlpatterns = [
    path('clientes/', ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('clientes/<str:id_cliente>/', ClienteDetailView.as_view(), name='cliente-detail'),
    path('ofertas/', OfertaListCreateView.as_view(), name='oferta-list-create'),
    path('ofertas/<int:id_oferta>/', OfertaDetailView.as_view(), name='oferta-detail'),
    path('create_oferta/', create_oferta, name='create-oferta'),
    path('actividad_cliente/', ActividadClienteListCreateView.as_view(), name='actividad-cliente-list-create'),
    path('oferta_detalle_completo/<int:id_oferta>/', oferta_detalle_completo, name='oferta-detalle-completo'),
    path('ofertas_disponibles/', ofertas_disponibles, name='ofertas-disponibles'),
    path('cliente/<str:id_cliente>/ofertas/', ofertas_por_cliente, name='ofertas-por-cliente'),
    path('actividades/', actividades_list, name='actividades-list'),
    path('provincias/', provincias_list, name='provincias-list'),
]
