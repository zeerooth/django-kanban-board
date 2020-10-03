from django.shortcuts import render
from .models import KanbanBoard, KanbanBoardElement, KanbanBoardState
from django.http import JsonResponse, HttpResponse
from uuid import UUID
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.contrib.auth.decorators import permission_required
import json

@csrf_protect
@permission_required('kanban_board.kanban_board.view', login_url=settings.LOGIN_URL)
def kanban_board(request, id):
    board = KanbanBoard.objects.get(pk=id)
    elements_grouped = board.kanban_board_grouped_elements()
    
    return render(request, 'kanban_board/board.html', 
        context={
            "kanban_board": board, 
            "kanban_board_elements": elements_grouped,
        })

@permission_required('kanban_board.kanban_board.view', login_url=settings.LOGIN_URL)
def board_panel(request):
    boards = KanbanBoard.objects.all()
    return render(request, 'kanban_board/panel.html', 
        context={
            "kanban_boards": boards, 
        })

def element(request, model, id):
    pass

@csrf_protect
@permission_required('kanban_board.kanban_board_element.change', login_url=settings.LOGIN_URL)
def change_element_status(request):
    # check method
    if not request.method == "POST":
        return JsonResponse({"error": "bad_method", "details": "expected POST but got " + str(request.method)}, status=405)

    # get all required parameters
    data = request.POST
    parent_id = UUID(data.get('kb_parent_id'))
    element_id = UUID(data.get('kb_element_id'))
    new_status = int(data.get('kb_new_status'))

    # validate if all required parameters are present
    missing_params = []
    for param in [element_id, new_status, parent_id]:
        if param is None:
            missing_params.append(param)
    if len(missing_params) > 0:
        return JsonResponse({"error": "missing_parameters", "details": missing_params}, status=422)

    # actual logic
    board = KanbanBoard.objects.get(pk=parent_id)
    el = KanbanBoardElement.objects.get(pk=element_id)
    el.kanban_board_state = board.workflow.kanbanboardstate_set.get(pk=new_status)
    el.save()

    return JsonResponse({}, status=200)
    