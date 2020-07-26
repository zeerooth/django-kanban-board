import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from typing import List

class KanbanBoard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("KanbanBoardName"), max_length=255)

    class Meta:
        abstract = True

DEFAULT_KANBAN_BOARD_COLUMNS = [
    ('waiting', _('Waiting')),
    ('in_progress', _('In progress')),
    ('completed', _('Completed'))
]

class KanbanBoardElement(models.Model):
    kanban_board_parent_id = models.ForeignKey(KanbanBoard, on_delete=models.CASCADE, blank=True, null=True)
    kanban_board_state = models.CharField(_("KanbanBoardElementState"), choices=DEFAULT_KANBAN_BOARD_COLUMNS, max_length=255)

    def kanban_board_field_tuples(self):
        return [(str(x), x.model.getattr(x)) for x in self._meta.get_fields()]

    class Meta:
        abstract = True
        kanban_board_fields: List[str] = []