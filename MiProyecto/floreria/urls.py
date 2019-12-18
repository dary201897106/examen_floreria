from django.contrib import admin
from django.urls import path,include
from .views import home,galeria,formulario,quienes,adm,eliminar_flor,login,ubicacion,cerrar_sesion,guardar_token,FlorViewSet
from rest_framework import routers

router = routers.DefaultRouter()

#Define la ruta para hacer el get y el post
router.register('flores', FlorViewSet)

#,carrito_compra
urlpatterns = [
    path('',home,name='HOME'),
    path('galeria/',galeria,name='GALE'),
    path('formulario/',formulario,name='FORM'),
    path('quienes_somos/',quienes,name='QUIENES'),
    path('adm_flores/',adm,name='ADM'),
    path('eliminar_flor/<id>/',eliminar_flor,name='ELIMINAR'),
    path('login/',login,name='LOGIN'),
    #path('carrito_compra/<id>/',carrito_compra,name='AGREGAR_CARRO'),
    path('ubicacion/',ubicacion,name='UBI'),
    path('cerrar_sesion/',cerrar_sesion,name='LOGOUT'),
    path('guardar_token/',guardar_token,name='guardar_token'),
   
    path('api/', include(router.urls)),
]