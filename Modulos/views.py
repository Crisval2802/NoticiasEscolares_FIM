import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views import View
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout


from .models import usuario, publicacion



# Create your views here.
class Login(View):
    def get(self,request):
        return render(request, 'login.html')
    
    def post(self,request):
        correo = request.POST.get('correo')
        password = request.POST.get('contra')
        user = authenticate(request, username=correo, password=password)
        if user is not None:
            login(request, user)
            aux=usuario.objects.get(correo=correo)

            if (aux.tipo=="L"):
                return redirect('inicio_lector')
            else:
                return redirect('inicio_escritor')
            
            
        else:
            datos={'message': "Credenciales incorrectas"}
            return render(request, 'login.html' , {"datos":datos})
        
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
class Registro(View):
    def get(self,request):
        return render(request, 'registro.html')
    
    def post(self,request):
        
        contra = request.POST.get('contra')
        confirmar_contra = request.POST.get('confirmar_contra')

        if contra != confirmar_contra:
            datos={'message': "Las contraseñas no coinciden"}
            return render(request, 'registro.html' , {"datos":datos})
        else:
            
            correo = request.POST.get('correo')

            usuarios=list(User.objects.filter(email=correo).values())
            if len(usuarios)>0:
                datos={'message': "Error, ya existe un registro con ese correo"}
                return render(request, 'registro.html' , {"datos":datos})
            else:
                tipo_usuario = request.POST.get('tipo_usuario')
                nombre = request.POST.get('nombre')
                apellido = request.POST.get('apellido')

                usuario.objects.create(nombre=nombre, apellido=apellido, correo=correo, tipo=tipo_usuario)

                
                user= User.objects.create_user(correo, correo, contra)
                user.save()
                datos={'message': "Registro Exitoso"}
                return render(request, 'registro.html' , {"registro":datos})

    

class Redirigir(View):
    def get(self, request):
        return redirect('inicio')    
    
class Inicio(View):

    @method_decorator(login_required, name='dispatch')
    def get(self, request):
        # Validacion de tipo de usuario
        aux_usuario = usuario.objects.get(correo=request.user.email)
        if aux_usuario.tipo=='E':
            return redirect('inicio_escritor')  
        else:
            return redirect('inicio_lector')  
        

class Inicio_Escritor(View):
    @method_decorator(login_required, name='dispatch')
    def get(self,request, categoria=""):
        # Validacion de tipo de usuario
        aux_usuario = usuario.objects.get(correo=request.user.email)
        if aux_usuario.tipo=='E':
            publicaciones = list(publicacion.objects.values().order_by("-fecha"))

            datos={'publicaciones': publicaciones}



            return render(request, 'inicio_escritor.html', {"datos":datos})
        else:
            datos={'message': "Error, no tienes acceso a esta ventana"}
            return JsonResponse(datos)
    
class Inicio_Lector(View):
    @method_decorator(login_required, name='dispatch')
    def get(self,request, categoria=""):
        # Validacion de tipo de usuario
        aux_usuario = usuario.objects.get(correo=request.user.email)
        if aux_usuario.tipo=='L':

            if categoria=="" or categoria=="General":
                
                publicaciones = list(publicacion.objects.values().order_by("-fecha"))

            elif categoria =="Software":

                publicaciones = list(publicacion.objects.filter(id_categoria_id=2).values().order_by("-fecha"))

            datos={'publicaciones': publicaciones}



            return render(request, 'inicio_lector.html', {"datos":datos})
        else:
            datos={'message': "Error, no tienes acceso a esta ventana"}
            return JsonResponse(datos)

class Publicar(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'publicar.html')
    
    def post(self, request):
        jd = json.loads(request.body)
        id_usuario = usuario.objects.get(correo=request.user.email)
        publicacion.objects.create(
            titulo=jd['titulo'],
            descripcion=jd['descripcion'],
            fecha=jd['fecha'],
            imagen=jd['imagen'],
            id_categoria_id=jd['id_categoria_id'],
            id_usuario=id_usuario  
        )
        datos = {'message': "Success"}
        return JsonResponse(datos)
