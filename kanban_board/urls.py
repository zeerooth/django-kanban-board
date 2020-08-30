from django.urls import path
from . import views

app_name='kanban_board'

urlpatterns = [
    path('<uuid:id>/', views.kanban_board, name='board'),
    path('move-element/', views.change_element_status, name='move_element'),
    path('', views.board_panel, name='panel'),
]