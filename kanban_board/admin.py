from django.contrib import admin
from kanban_board.models import KanbanBoard, KanbanBoardState

admin.site.register(KanbanBoard)
admin.site.register(KanbanBoardState)
