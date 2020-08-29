from django.contrib import admin
from ordered_model.admin import OrderedStackedInline, OrderedInlineModelAdminMixin
from kanban_board.models import KanbanBoard, KanbanBoardState, Workflow

class KanbanBoardStateInline(OrderedStackedInline):
    model = KanbanBoardState
    fields = ('move_up_down_links', )
    readonly_fields = ('move_up_down_links', )
    extra = 1

class WorkflowAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', )
    inlines = (KanbanBoardStateInline, )

admin.site.register(KanbanBoard)
admin.site.register(KanbanBoardState)
admin.site.register(Workflow, WorkflowAdmin)
