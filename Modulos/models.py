from django.utils import timezone
from django.db import models


class usuario(models.Model):
    nombre=models.CharField(max_length=100)
    apellido=models.CharField(max_length=100)
    correo=models.CharField(max_length=100, default='')
    tipo=models.CharField(max_length=1, default='L')
    

class categoria(models.Model):
    nombre=models.CharField(max_length=80)

class publicacion(models.Model):
    titulo= models.CharField(max_length=150)
    id_categoria = models.ForeignKey(categoria, null=False, on_delete=models.DO_NOTHING)
    descripcion = models.CharField(max_length=1000)
    fecha = models.DateField()
    imagen = models.ImageField(upload_to='imagenes_publicacion')
    id_usuario = models.ForeignKey(usuario, null=False, on_delete=models.DO_NOTHING)

class eventos(models.Model):
    titulo= models.CharField(max_length=150)
    id_categoria = models.ForeignKey(categoria, null=False, on_delete=models.DO_NOTHING)
    descripcion = models.CharField(max_length=1000)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_final = models.DateField()
    id_usuario = models.ForeignKey(usuario, null=False, on_delete=models.DO_NOTHING)

