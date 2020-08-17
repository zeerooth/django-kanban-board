from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:id>/', views.kanban_board),
    path('move-element/', views.change_element_status),
]