from django.urls import path
from . import views
from .views import MyTokenObtainPairView, crearReserva, createNews


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),
    path('news/', views.getNews),
    path('news/create', createNews, name='news-create'),
    path('news/<int:news_id>/', views.get_news_by_id, name='get-news-by-id'),
    path('canchas/', views.getCanchas),
    path('reservas/', views.getReservas),
    path('reservas/create', crearReserva, name='reserva-create'),
    path('reservas/<int:pk>/', views.ReservaDetailView.as_view(), name='reserva-detail'),
    path('reservas/<int:user_id>/', views.getReservasDeUsuario, name='reservas-de-usuario'),
    path('reservas/edit/<int:reserva_id>/', views.editarReserva, name='reserva-edit'),
    path('news/<int:news_id>/edit/', views.editNews, name='edit-news'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register, name='register'),
]
