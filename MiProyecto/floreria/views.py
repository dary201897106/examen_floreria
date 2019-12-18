from django.shortcuts import render
from .models import Estado,Flor
from django.contrib.auth.models import User #para trabajar con usuarios
from django.contrib.auth import authenticate,logout,login as login_autent #libreria de autentificacion
from django.contrib.auth.decorators import login_required #decorator para impedir ingresar sin estar logeado

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
import json

from fcm_django.models import FCMDevice


from rest_framework import viewsets #rest_framework 
from .serializers import FlorSerializer 


# Create your views here.
@csrf_exempt
@require_http_methods(['POST'])
def guardar_token(request):
    body = request.body.decode('utf-8')
    bodyDict = json.loads(body)

    token = bodyDict['token']

    existe = FCMDevice.objects.filter(registration_id = token, active=True)

    if len(existe) > 0:
        return HttpResponseBadRequest(json.dumps({'mensaje':'El token ya existe'}))

    dispositivo = FCMDevice()
    dispositivo.registration_id = token
    dispositivo.active = True

    #solo si el usuario esta logeado
    if request.user.is_authenticated:
        dispositivo.user = request.user

    try:
        dispositivo.save()
        return HttpResponse(json.dumps({'mensaje':'Token guardado'}))
    except:
        return HttpResponseBadRequest(json.dumps({'mensaje':'No se pudo guardar el token'}))


@login_required(login_url='/login/')
def home(request):
    return render(request,'core/index.html')
#Vista para la administracion de flores
@login_required(login_url='/login/')
def adm(request):
    fl=Flor.objects.all()
    return render(request,'core/adm_flores.html', {'flores':fl})
@login_required(login_url='/login/')
def eliminar_flor(request,id):
    flo=Flor.objects.get(name=id)
    mensaje=''
    try:
        flo.delete()
        mensaje='Flor Eliminada' 
    except:
          mensaje='Problema al Eliminar' 
    fl=Flor.objects.all()
    return render(request,'core/adm_flores.html', {'flores':fl, 'msg':mensaje})
@login_required(login_url='/login/')
def galeria(request):
    fl=Flor.objects.all()
    return render(request,'core/galeria.html', {'flores':fl})

@login_required(login_url='/login/')
def formulario(request):
    est=Estado.objects.all()#select * from Estado
    if request.POST:
        nombre=request.POST.get("txtNombre")
        precio=request.POST.get("txtPrecio")
        stock=request.POST.get("txtStock")
        descripcion=request.POST.get("txtDescripcion")
        estado=request.POST.get("cboEstado")
        obj_estado=Estado.objects.get(name=estado)
        imagen=request.FILES.get("imagen")
        flor=Flor(
           name=nombre,precio=precio,stock=stock,descripcion=descripcion,estado=obj_estado,imagen=imagen
        )
        flor.save()#se graba flor

        dispositivos = FCMDevice.objects.filter(active=True)
        #dispositivos.send_message(
            #title="Flor Agregada",
            #icon="/static/img/logo.png"
        #)

        return render(request,'core/formulario.html', {'estados':est, 'msg':'Grabo'})
    return render(request,'core/formulario.html', {'estados':est})#nombre del arreglo con todos los estados

@login_required(login_url='/login/')
def quienes(request):
    return render(request,'core/quienes_somos.html')

@login_required(login_url='/login/')
def ubicacion(request):
    return render(request,'core/ubicacion.html')

#Creacion de vista login
def login(request):
    if request.POST:
        usuario=request.POST.get("txtUsuario")
        password=request.POST.get("txtPass")
        us=authenticate(request,username=usuario,password=password)
        msg=''
        if us is not None and us.is_active:
            login_autent(request,us)
            return render(request,'core/index.html')
        else:
            return render(request,'core/login.html')
    return render(request,'core/login.html')

def login_acceso(request):
    if request.POST:
        usuario=request.POST.get("txtUsuario")
        password=request.POST.get("txtPass")
        us=authenticate(request,username=usuario,password=password)
        msg=''
        if us is not None and us.is_active:
            login_autent(request,us)
            return render(request,'core/index.html')
        else:
            return render(request,'core/login.html')

#CERRAR SESION
def cerrar_sesion(request):
    logout(request)
    return render(request,'core/login.html')


#CARRITO DE COMPRAS
#@login_required(login_url='/login/')
#def carrito_compra(request,id):
#    lista=request.session.get('carrito','')
#    lista=lista+str(id)+","
#    fl=Flor.objects.all()
#    request.session["carrito"]=lista
#    arr=lista.split(',')
#    return render(request,'core/galeria.html',{'flores':fl,'lista':lista})

#Representa los datos que va a guardar y los devolverá como json 
class FlorViewSet(viewsets.ModelViewSet): 
    queryset = Flor.objects.all()
    serializer_class = FlorSerializer