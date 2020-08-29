from django.contrib import admin
from ordered_model.admin import OrderedStackedInline, OrderedInlineModelAdminMixin
from kanban_board.models import KanbanBoard, KanbanBoardState, Workflow

class KanbanBoardStateInline(OrderedStackedInline):
    model = KanbanBoardState
    fields = ('workflow', 'name', 'move_up_down_links', )
    readonly_fields = ('workflow', 'move_up_down_links', )
    extra = 0
    ordering = ('order',)

class WorkflowAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', )
    inlines = (KanbanBoardStateInline, )

admin.site.register(KanbanBoard)
admin.site.register(KanbanBoardState)
admin.site.register(Workflow, WorkflowAdmin)
