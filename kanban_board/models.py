import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from typing import List
from model_utils.managers import InheritanceManager
from ordered_model.models import OrderedModel
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User, Group 


class Workflow(models.Model):
    name = models.CharField(_("WorkflowName"), max_length=255)

    def __str__(self):
        return self.name


class KanbanBoardState(OrderedModel):
    workflow = models.ForeignKey("Workflow", on_delete=models.CASCADE)
    name = models.CharField(_("KanbanBoardStateName"), max_length=255)
    order_with_respect_to = 'workflow'

    def __str__(self):
        return self.workflow.name + ": " + self.name
    
    class Meta(OrderedModel.Meta):
        ordering = ('order',)


class KanbanBoard(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("KanbanBoardName"), max_length=255)
    workflow = models.ForeignKey("Workflow", on_delete=models.PROTECT)

    allowed_users = models.ManyToManyField(User)
    allowed_groups = models.ManyToManyField(Group)

    class Meta:
        app_label = 'kanban_board'
    
    def __str__(self):
        return self.name
    
    def kanban_board_grouped_elements(self):
        states = list(KanbanBoardState.objects.filter(workflow=self.workflow))
        board_elements = list(KanbanBoardElement.objects.filter(kanban_board_parent=self).select_subclasses())
        elements_grouped = {x: [] for x in states}
        for element in board_elements:
            if element.kanban_board_state is not None:
                elements_grouped[element.kanban_board_state].append(element)
        return elements_grouped


class KanbanBoardElement(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    kanban_board_state = models.ForeignKey("KanbanBoardState", on_delete=models.SET_NULL, null=True, blank=True, editable=False)
    kanban_board_parent = models.ForeignKey("KanbanBoard", on_delete=models.CASCADE)

    kanban_board_fields: List[str] = []

    objects = InheritanceManager()

    changed_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    history = HistoricalRecords()

    def kanban_board_field_tuples(self):
        return [(x.name, str(getattr(self, x.name))) for x in self._meta.fields if x.name in self.kanban_board_fields]
    
    def save(self, *args, **kwargs):
        if self.kanban_board_state is None:
            self.kanban_board_state = self.kanban_board_parent.workflow.kanbanboardstate_set.first()
        super(KanbanBoardElement, self).save(*args, **kwargs)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


    class Meta:
        app_label = 'kanban_board'
