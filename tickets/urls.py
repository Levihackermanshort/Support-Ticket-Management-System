from django.urls import path, include
from . import views
from rest_framework import routers
from .api import TicketViewSet, ReplyViewSet

router = routers.DefaultRouter()
router.register(r'api/tickets', TicketViewSet, basename='api-tickets')
router.register(r'api/replies', ReplyViewSet, basename='api-replies')

app_name = 'tickets'

urlpatterns = [
    path('', views.ticket_list, name='list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.ticket_create, name='create'),
    path('<int:pk>/', views.ticket_detail, name='detail'),
    path('<int:pk>/edit/', views.ticket_edit, name='edit'),
    path('<int:pk>/delete/', views.ticket_delete, name='delete'),
    path('<int:pk>/reply/', views.add_reply, name='reply'),
    path('', include(router.urls)),
]
