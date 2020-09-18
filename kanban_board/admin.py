from django.contrib import admin
from ordered_model.admin import OrderedStackedInline, OrderedInlineModelAdminMixin
from kanban_board.models import KanbanBoard, KanbanBoardState, Workflow, KanbanBoardElement

class KanbanBoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'workflow', 'element_count')
    filter_horizontal = ('allowed_users', 'allowed_groups')

    def element_count(self, obj):
        return KanbanBoardElement.objects.filter(kanban_board_parent=obj).select_subclasses().count()


class KanbanBoardStateInline(OrderedStackedInline):
    model = KanbanBoardState
    fields = ('workflow', 'name', 'move_up_down_links', )
    readonly_fields = ('workflow', 'move_up_down_links', )
    extra = 0
    ordering = ('order',)


class WorkflowAdmin(OrderedInlineModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'workflow_sequence')
    inlines = (KanbanBoardStateInline, )

    def workflow_sequence(self, obj):
        return "->".join([str(x.name) for x in list(obj.kanbanboardstate_set.all())])

admin.site.register(KanbanBoard, KanbanBoardAdmin)
admin.site.register(KanbanBoardState)
admin.site.register(Workflow, WorkflowAdmin)
