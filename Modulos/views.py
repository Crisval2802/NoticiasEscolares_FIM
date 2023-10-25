from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
class Login(View):
    def get(self,request):
        return render(request, 'login.html')
    
class Registro(View):
    def get(self,request):
        return render(request, 'registro.html')
    

class Redirigir(View):
    def get(self, request):
        return redirect('login')