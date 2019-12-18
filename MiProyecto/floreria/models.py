from django.db import models

# Create your models here.
class Estado(models.Model):
    name=models.CharField(max_length=15,primary_key=True)
    estado=models.IntegerField()

    def __str__(self):
        return self.name


class Flor(models.Model):
    name=models.CharField(max_length=30,primary_key=True)
    precio=models.IntegerField()
    stock=models.IntegerField()
    descripcion=models.TextField()
    estado=models.ForeignKey(Estado,on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to="flores",null=True)

    def __str__(self):
        return self.name 