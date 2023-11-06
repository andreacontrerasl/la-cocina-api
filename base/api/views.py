from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.forms import UserCreationForm
import cloudinary.uploader
from django.contrib.auth.models import Group

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .forms import CustomUserCreationForm

from .serializers import NewsSerializer, CanchaSerializer, ReservaSerializer, ReservaDetailSerializer
from base.models import News, Cancha, Reserva

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        
        groups = user.groups.all()
        if groups:
            group_names = [group.name for group in groups]
            token['groups'] = group_names

        return token
   

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.data)
        if form.is_valid():
            user = form.save()
            
            # Asignar el grupo "client" al nuevo usuario
            group = Group.objects.get(name='client')
            user.groups.add(group)
            
            # Puedes realizar acciones adicionales aquí después de registrar al usuario
            return JsonResponse({"message": "Usuario registrado exitosamente."})
        else:
            errors = form.errors
            return JsonResponse({"error": errors}, status=400)
    else:
        return Response({"error": "Método no permitido."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)


@api_view(['GET'])
def getNews(request):
    news = News.objects.all()
    serializer = NewsSerializer(news, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getReservas(request):
    reserva = Reserva.objects.all()
    serializer = ReservaSerializer(reserva, many=True)
    return Response(serializer.data)

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def getCanchas(request):
    #user = request.user
    #canchas = user.note_set.all()
    canchas = Cancha.objects.all()
    serializer = CanchaSerializer(canchas, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def crearReserva(request):
    serializer = ReservaSerializer(data=request.data)
    if serializer.is_valid():
        cancha = serializer.validated_data['cancha']
        dia = serializer.validated_data['dia']
        hora = serializer.validated_data['hora']

        # Verificar si ya existe una reserva para la cancha, fecha y hora proporcionadas
        if Reserva.objects.filter(cancha=cancha, dia=dia, hora=hora).exists():
            return Response({"error": "Ya existe una reserva para la cancha seleccionada en esta fecha y hora."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(usuario=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createNews(request):
    serializer = NewsSerializer(data=request.data)
    if serializer.is_valid():
        image_file = serializer.validated_data.get('image') 

        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)

            image_url = upload_result['secure_url']
        else:
            image_url = None
            
        news_instance = serializer.save(user=request.user, image_url=image_url)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_news_by_id(request, news_id):
    try:
        news = News.objects.get(pk=news_id)
    except News.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = NewsSerializer(news)
    return Response(serializer.data)

@api_view(['GET'])
def get_reserva_by_id(request, reserva_id):
    try:
        reserva = Reserva.objects.get(pk=reserva_id)
    except Reserva.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ReservaSerializer(reserva)
    return Response(serializer.data)

class ReservaDetailView(RetrieveAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaDetailSerializer  # Reemplaza con el nombre real de tu serializador de detalle
    

@api_view(['GET'])
def getReservasDeUsuario(request, user_id):
    try:
        reservas = Reserva.objects.filter(usuario=user_id)
    except Reserva.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ReservaSerializer(reservas, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def editarReserva(request, reserva_id):
    try:
        reserva = Reserva.objects.get(pk=reserva_id, usuario=request.user)
    except Reserva.DoesNotExist:
        return Response({"error": "La reserva no existe o no tienes permiso para editarla."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReservaSerializer(reserva, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def editNews(request, news_id):
    try:
        news = News.objects.get(pk=news_id, user=request.user)
    except News.DoesNotExist:
        return Response({"error": "La noticia no existe o no tienes permiso para editarla."}, status=status.HTTP_404_NOT_FOUND)

    serializer = NewsSerializer(news, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
