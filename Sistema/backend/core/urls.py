from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('test_interfaz.urls')),  # Asegúrate de reemplazar <nombre_de_tu_aplicacion>
]
