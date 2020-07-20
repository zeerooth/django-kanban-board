from django.shortcuts import render
from .models import KanbanBoard, KanbanBoardElement

def kanban_board(request, id):
    board = KanbanBoard.objects.get(id=id)
    board_elements = KanbanBoardElement.objects.get(kanban_board_parent_id=id)
    
    return render(request, 'kanban_board', context={"kanban_board": board, "kanban_board_elements": board_elements})