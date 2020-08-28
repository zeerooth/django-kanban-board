from django.contrib import admin
from ordered_model.admin import OrderedStackedInline, OrderedInlineModelAdminMixin
from kanban_board.models import KanbanBoard, KanbanBoardState, Workflow

class KanbanBoardStateInline(OrderedStackedInline):
    model = KanbanBoardState
    extra = 1

class WorkflowAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'move_up_down_links')
    inlines = (KanbanBoardStateInline, )

admin.site.register(KanbanBoard)
admin.site.register(KanbanBoardState)
admin.site.register(Workflow, WorkflowAdmin)
