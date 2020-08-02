from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:id>/', views.kanban_board),
]