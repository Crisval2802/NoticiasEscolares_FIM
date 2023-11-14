from django.urls import path

from .views import Evento, Inicio, Inicio_Escritor, Inicio_Lector, Login, Logout, Publicar, Redirigir, Registro
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns=[  
   path('login/', Login.as_view(), name='login'),
   path('logout/', Logout.as_view(), name='logout'),
   path('', Redirigir.as_view(), name='redirigir'),
   path('inicio/', Inicio.as_view(), name='inicio'),
   path('registro/', Registro.as_view(), name='registro'),
   path('inicio_lector/', Inicio_Lector.as_view(), name='inicio_lector'),
   path('inicio_escritor/', Inicio_Escritor.as_view(), name='inicio_escritor'),
   path('publicar/', Publicar.as_view(), name='publicar'),
   path('evento/', Evento.as_view(), name='publicar_evento'),
]