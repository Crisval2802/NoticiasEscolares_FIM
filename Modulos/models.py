from django.db import models


class usuario(models.Model):
    nombre=models.CharField(max_length=100)
    apellido=models.CharField(max_length=100)
    num_cuenta=models.CharField(max_length=8)

class categoria(models.Model):
    nombre=models.CharField(max_length=80)

class publicacion(models.Model):
    titulo= models.CharField(max_length=150)
    id_categoria = models.ForeignKey(categoria, null=False, on_delete=models.DO_NOTHING)
    descripcion = models.CharField(max_length=1000)
    fecha = models.DateField()
    imagen = models.CharField(max_length=80)
    id_usuario = models.ForeignKey(usuario, null=False, on_delete=models.DO_NOTHING)

class eventos(models.Model):
    titulo= models.CharField(max_length=150)
    id_categoria = models.ForeignKey(categoria, null=False, on_delete=models.DO_NOTHING)
    descripcion = models.CharField(max_length=1000)
    fecha = models.DateField()
    imagen = models.CharField(max_length=80)
    id_usuario = models.ForeignKey(usuario, null=False, on_delete=models.DO_NOTHING)

