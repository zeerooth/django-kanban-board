from django.urls import path
from . import views

urlpatterns = [
    path('kanban-boards/<uuid:id>/', views.kanban_board),
    
]