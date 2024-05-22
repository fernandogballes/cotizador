from rest_framework import serializers
from .models import *

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class CatalogoActividadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoActividades
        fields = '__all__'

class CatalogoCoberturasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoCoberturas
        fields = '__all__'

class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = '__all__'

class CatalogoFranquiciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoFranquicias
        fields = '__all__'

class CatalogoSublimitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoSublimites
        fields = '__all__'

class ActividadClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadCliente
        fields = ['id_cliente', 'id_actividad']

class ActividadCoberturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadCobertura
        fields = ['id_cobertura', 'id_actividad']

class OfertaCoberturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfertaCobertura
        fields = ['id_cobertura', 'id_oferta']

class FranquiciaCoberturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranquiciaCobertura
        fields = ['id_cobertura', 'id_franquicia']

class SublimiteCoberturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SublimiteCobertura
        fields = ['id_cobertura', 'id_sublimite']

class CatalogoProvinciasSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogoProvincias
        fields = '__all__'

class OfertaDisponibleSerializer(serializers.ModelSerializer):
    nombre_cliente = serializers.CharField(source='id_cliente.nombre_cliente')

    class Meta:
        model = Oferta
        fields = ['id_oferta', 'id_cliente', 'nombre_cliente']

class OfertaPorClienteSerializer(serializers.ModelSerializer):
    numero_coberturas = serializers.SerializerMethodField()

    class Meta:
        model = Oferta
        fields = ['id_oferta', 'suma_asegurada', 'numero_coberturas']

    def get_numero_coberturas(self, obj):
        return OfertaCobertura.objects.filter(id_oferta=obj).count()
