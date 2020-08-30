from django.urls import path
from . import views

app_name='kanban_board'

urlpatterns = [
    path('<uuid:id>/', views.kanban_board),
    path('move-element/', views.change_element_status),
    path('', views.board_panel),
]