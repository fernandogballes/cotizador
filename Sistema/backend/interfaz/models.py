from django.db import models

# Create your models here.
from django.db import models
from viewflow.fields import CompositeKey

class CatalogoProvincias(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    provincia = models.CharField(max_length=50)

    class Meta:
        db_table = 'catalogo_provincias'
        managed = False

    def __str__(self):
        return self.provincia

class Cliente(models.Model):
    id_cliente = models.CharField(max_length=9, primary_key=True)
    nombre_cliente = models.CharField(max_length=250, unique=True, default='None')
    volumen_facturacion = models.FloatField()
    id_provincia = models.ForeignKey(CatalogoProvincias, on_delete=models.CASCADE, db_column='id_provincia', default=0)

    class Meta:
        db_table = 'clientes'
        managed = False

    def __str__(self):
        return self.nombre_cliente

class CatalogoActividades(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    nombre_actividad = models.CharField(max_length=100, unique=True)
    agravada_flag = models.BooleanField()

    class Meta:
        db_table = 'catalogo_actividades'
        managed = False

    def __str__(self):
        return self.nombre_actividad

class CatalogoCoberturas(models.Model):
    id_cobertura = models.AutoField(primary_key=True)
    nombre_cobertura = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'catalogo_coberturas'
        managed = False

    def __str__(self):
        return self.nombre_cobertura

class Oferta(models.Model):
    id_oferta = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    suma_asegurada = models.FloatField(null=True, blank=True, default=0.0)
    limite_anualidad = models.FloatField(null=True, blank=True, default=0.0)
    semaforo = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'ofertas'
        managed = False

    def __str__(self):
        return f'Oferta {self.id_oferta} - Cliente {self.id_cliente}'

class CatalogoFranquicias(models.Model):
    id_franquicia = models.AutoField(primary_key=True)
    franquicia = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalogo_franquicias'
        managed = False

    def __str__(self):
        return self.franquicia

class CatalogoSublimites(models.Model):
    id_sublimite = models.AutoField(primary_key=True)
    sublimite = models.CharField(max_length=100)

    class Meta:
        db_table = 'catalogo_sublimites'
        managed = False

    def __str__(self):
        return self.sublimite

class ActividadCliente(models.Model):
    id = CompositeKey(columns=['id_cliente', 'id_actividad', 'id_oferta'])
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    id_actividad = models.ForeignKey(CatalogoActividades, on_delete=models.CASCADE, db_column='id_actividad')
    id_oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, db_column='id_oferta')

    class Meta:
        unique_together = (('id_cliente', 'id_actividad', 'id_oferta'),)
        managed = False
        db_table = 'actividad_cliente'

class ActividadCobertura(models.Model):
    id = CompositeKey(columns=['id_cobertura', 'id_actividad'])
    id_actividad = models.ForeignKey(CatalogoActividades, on_delete=models.CASCADE, db_column='id_actividad')
    id_cobertura = models.ForeignKey(CatalogoCoberturas, on_delete=models.CASCADE, db_column='id_cobertura')

    class Meta:
        unique_together = (('id_actividad', 'id_cobertura'),)
        managed = False
        db_table = 'actividad_cobertura'

class OfertaCobertura(models.Model):
    id = CompositeKey(columns=['id_oferta', 'id_cobertura'])
    id_oferta = models.ForeignKey(Oferta, on_delete=models.CASCADE, db_column='id_oferta')
    id_cobertura = models.ForeignKey(CatalogoCoberturas, on_delete=models.CASCADE, db_column='id_cobertura')
    id_franquicia = models.ForeignKey(CatalogoFranquicias, on_delete=models.CASCADE, db_column='id_franquicia')
    id_sublimite = models.ForeignKey(CatalogoSublimites, on_delete=models.CASCADE, db_column='id_sublimite')

    class Meta:
        managed = False
        db_table = 'oferta_cobertura'
        unique_together = (('id_oferta', 'id_cobertura'),)

class FranquiciaCobertura(models.Model):
    id = CompositeKey(columns=['id_franquicia', 'id_cobertura'])
    id_franquicia = models.ForeignKey(CatalogoFranquicias, on_delete=models.CASCADE, db_column='id_franquicia')
    id_cobertura = models.ForeignKey(CatalogoCoberturas, on_delete=models.CASCADE, db_column='id_cobertura')

    class Meta:
        db_table = 'franquicia_cobertura'
        managed = False
        unique_together = (('id_franquicia', 'id_cobertura'),)

class SublimiteCobertura(models.Model):
    id = CompositeKey(columns=['id_sublimite', 'id_cobertura'])
    id_sublimite = models.ForeignKey(CatalogoSublimites, on_delete=models.CASCADE, db_column='id_sublimite')
    id_cobertura = models.ForeignKey(CatalogoCoberturas, on_delete=models.CASCADE, db_column='id_cobertura')

    class Meta:
        db_table = 'sublimite_cobertura'
        managed = False
        unique_together = (('id_sublimite', 'id_cobertura'),)
