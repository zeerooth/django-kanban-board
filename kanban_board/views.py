from django.shortcuts import render
from .models import KanbanBoard, KanbanBoardElement, KanbanBoardState
from django.http import JsonResponse, HttpResponse
from uuid import UUID
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def kanban_board(request, id):
    board = KanbanBoard.objects.get(pk=id)
    states = list(KanbanBoardState.objects.filter(workflow=board.workflow))
    board_elements = list(KanbanBoardElement.objects.filter(kanban_board_parent=board).select_subclasses())
    elements_grouped = {x: [] for x in states}
    for element in board_elements:
        if element.kanban_board_state is not None:
            elements_grouped[element.kanban_board_state].append(element)
    return render(request, 'kanban_board/board.html', 
        context={
            "kanban_board": board, 
            "kanban_board_elements": elements_grouped,
        })

def board_panel(request):
    boards = KanbanBoard.objects.all()
    return render(request, 'kanban_board/panel.html', 
        context={
            "kanban_boards": boards, 
        })

def element(request, model, id):
    pass

@csrf_protect
def change_element_status(request):
    # check method
    if not request.method == "POST":
        return JsonResponse({"error": "bad_method", "details": "expected POST but got " + str(request.method)}, status=405)

    # get all required parameters
    parent_id = UUID(request.POST.get('kb_parent_id'))
    element_id = UUID(request.POST.get('kb_element_id'))
    new_status = int(request.POST.get('kb_new_status'))

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
    