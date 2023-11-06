from rest_framework.serializers import ModelSerializer, CharField
from base.models import News, Cancha, Reserva
from django.contrib.auth import get_user_model

User = get_user_model()

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        
class CanchaSerializer(ModelSerializer):
    class Meta:
        model = Cancha
        fields = '__all__'

class ReservaSerializer(ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

class ReservaDetailSerializer(ModelSerializer):
    cancha_nombre = CharField(source='cancha.nombre', read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'
        extra_fields = ['cancha_nombre']