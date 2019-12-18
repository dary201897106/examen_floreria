#Herramienta que nos permite transformar los datos a json o al reves
from rest_framework import serializers
from .models import Flor

class FlorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flor
        fields = ['name' ,'precio' ,'stock', 'descripcion','estado']
