from django.shortcuts import render
from .models import KanbanBoard, KanbanBoardElement

def kanban_board(request, id):
    board = KanbanBoard.objects.get(id=id)
    board_elements = KanbanBoardElement.objects.get(kanban_board_parent_id=id)
    board_elements_list = []
    for board_element in board_elements:
        tmp_el = {}
        for key, value in board_element:
            tmp_el[key] = value
        board_elements_list += tmp_el
    
    return render(request, 'kanban_board', 
        context={"kanban_board": board, 
                 "kanban_board_elements": board_elements,
                })