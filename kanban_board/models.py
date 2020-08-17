import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from typing import List
from django.contrib.contenttypes.models import ContentType
from gm2m import GM2MField

class KanbanBoard(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("KanbanBoardName"), max_length=255)
    elements = GM2MField()

    class Meta:
        app_label = 'kanban_board'

DEFAULT_KANBAN_BOARD_COLUMNS = [
    ('waiting', _('Waiting')),
    ('in_progress', _('In progress')),
    ('completed', _('Completed'))
]

class KanbanBoardElement(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)

    kanban_board_state = models.CharField(_("KanbanBoardElementState"), choices=DEFAULT_KANBAN_BOARD_COLUMNS, max_length=255)

    kanban_board_fields: List[str] = []

    def kanban_board_field_tuples(self):
        return [(x.name, str(getattr(self, x.name))) for x in self._meta.fields if x.name in self.kanban_board_fields]

    class Meta:
        abstract = True
        app_label = 'kanban_board'