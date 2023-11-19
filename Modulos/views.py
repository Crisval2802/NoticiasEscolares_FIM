import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.views import View
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.core.paginator import Paginator
from django.core.files.base import ContentFile


from .models import eventos, usuario, publicacion



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
                return redirect('/inicio_lector/General')  
            else:
                return redirect('/inicio_escritor/General')  
            
            
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
            return redirect('/inicio_escritor/General')  
        else:
            return redirect('/inicio_lector/General')  
        

class Inicio_Escritor(View):
    @method_decorator(login_required, name='dispatch')
    def get(self,request, categoria=""):
        # Validacion de tipo de usuario
        aux_usuario = usuario.objects.get(correo=request.user.email)
        if aux_usuario.tipo=='E':

            
            if categoria =="Software":

                publicaciones = publicacion.objects.filter(id_categoria_id=2).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_escritor.html', {'entity': publicaciones, 'paginator':paginator, 'categoria': "Software"})
            
            if categoria =="Civil":

                publicaciones = publicacion.objects.filter(id_categoria_id=3).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_escritor.html', {'entity': publicaciones, 'paginator':paginator, 'categoria': "Civil"})
            if categoria =="Geodesia":
                publicaciones = publicacion.objects.filter(id_categoria_id=4).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_escritor.html', {'entity': publicaciones, 'paginator':paginator, 'categoria': "Geodesia"})
            if categoria =="Procesos":
                publicaciones = publicacion.objects.filter(id_categoria_id=5).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_escritor.html', {'entity': publicaciones, 'paginator':paginator, 'categoria': "Procesos Industriales"})
            if categoria =="Becas":
                publicaciones = publicacion.objects.filter(id_categoria_id=6).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_escritor.html', {'entity': publicaciones, 'paginator':paginator, 'categoria': "Becas"})
            else:
                
                publicaciones = publicacion.objects.all().order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_escritor.html', {'entity': publicaciones, 'paginator':paginator, 'categoria': "General"})
            
            
           
        else:
            return redirect('/inicio_lector/General')
    
class Inicio_Lector(View):
    @method_decorator(login_required, name='dispatch')
    def get(self,request, categoria=""):
        # Validacion de tipo de usuario
        aux_usuario = usuario.objects.get(correo=request.user.email)
        if aux_usuario.tipo=='L':

            

            if categoria =="Software":

                publicaciones = publicacion.objects.filter(id_categoria_id=2).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_lector.html', {'entity': publicaciones, 'paginator':paginator})
            
            if categoria =="Civil":

                publicaciones = publicacion.objects.filter(id_categoria_id=3).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_lector.html', {'entity': publicaciones, 'paginator':paginator})
            if categoria =="Geodesia":
                publicaciones = publicacion.objects.filter(id_categoria_id=4).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_lector.html', {'entity': publicaciones, 'paginator':paginator})
            if categoria =="Procesos":
                publicaciones = publicacion.objects.filter(id_categoria_id=5).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_lector.html', {'entity': publicaciones, 'paginator':paginator})
            if categoria =="Becas":
                publicaciones = publicacion.objects.filter(id_categoria_id=6).order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_lector.html', {'entity': publicaciones, 'paginator':paginator})
            else:
                
                publicaciones = publicacion.objects.all().order_by("-id")

                page = request.GET.get('page', 1)
                try:
                    paginator = Paginator(publicaciones, 5)
                    publicaciones = paginator.page(page)
                except:
                    raise   Http404

                return render(request, 'inicio_lector.html', {'entity': publicaciones, 'paginator':paginator})


        else:
            return redirect('/inicio_escritor/General')

class Publicar(View):
    @method_decorator(login_required)
    def get(self, request):
        # Validacion de tipo de usuario
        aux_usuario = usuario.objects.get(correo=request.user.email)
        if aux_usuario.tipo=='E':
            return render(request, 'publicar.html') 
        else:
            return redirect('/inicio_lector/General')  
        
        
    
    def post(self, request):

        id_usuario = usuario.objects.get(correo=request.user.email)
        publicacion.objects.create(
            titulo=request.POST.get('titulo'),
            descripcion=request.POST.get('descripcion'),
            fecha=request.POST.get('fecha'),
            id_categoria_id=request.POST.get('id_categoria_id'),
            id_usuario=id_usuario  
        )


        imagen = request.FILES.get('imagen', None)
        if imagen:
            image = request.FILES['imagen'].read()

            ultima_publicacion = publicacion.objects.latest('id')

            ultima_publicacion.imagen.save('imagen_publicacion_'+ str(ultima_publicacion.id) + '.jpg',  ContentFile(image), save=False) # se guarda la nueva foto
            ultima_publicacion.save()

        datos = {'message': "Success"}
        return JsonResponse(datos)
class Evento(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'evento.html')
    def post(self, request):
        jd = json.loads(request.body)
        id_usuario = usuario.objects.get(correo=request.user.email)
        eventos.objects.create(
            titulo=jd['titulo'],
            id_categoria_id=jd['id_categoria_id'],
            descripcion=jd['descripcion'],
            fecha_inicio=jd['fecha_inicio'],
            fecha_final=jd['fecha_final'],
            imagen=jd['imagen'],
            id_usuario=id_usuario 
        )
        datos = {'message': "Success"}
        return JsonResponse(datos)
    
class Calendar_View(View):    
    def get(self, request):
        return render(request, 'calendar.html')

