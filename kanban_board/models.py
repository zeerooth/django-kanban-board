import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from typing import List
from model_utils.managers import InheritanceManager


class KanbanBoardState(models.Model):
    name = models.CharField(_("KanbanBoardStateName"), max_length=255)

    def __str__(self):
        return self.name


class KanbanBoard(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("KanbanBoardName"), max_length=255)
    states = models.ManyToManyField(KanbanBoardState)

    class Meta:
        app_label = 'kanban_board'
    
    def __str__(self):
        return self.name


class KanbanBoardElement(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    kanban_board_state = models.ForeignKey(KanbanBoardState, on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    kanban_board_parent = models.ForeignKey(KanbanBoard, on_delete=models.CASCADE)

    kanban_board_fields: List[str] = []

    objects = InheritanceManager()

    def kanban_board_field_tuples(self):
        return [(x.name, str(getattr(self, x.name))) for x in self._meta.fields if x.name in self.kanban_board_fields]
    
    def save(self, *args, **kwargs): 
        super(KanbanBoardElement, self).save(*args, **kwargs) 
        self.kanban_board_state = self.kanban_board_parent.states.first()

    class Meta:
        app_label = 'kanban_board'