from kanban_board.models import KanbanBoard, KanbanBoardElement
from django.db import models

DEPARTMENT_CHOICES = [
    ('management', 'Management'),
    ('sales', 'Sales'),
    ('technical', 'Technical')
]

class Person(models.Model):
    name = models.CharField("Name", max_length=255)
    department = models.CharField("Department", choices=DEPARTMENT_CHOICES, max_length=255)

    def __str__(self):
        return self.name

class Task(KanbanBoardElement):
    name = models.CharField("TaskName", max_length=65535)
    deadline = models.DateTimeField("Deadline", blank=True, null=True)
    author = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True, related_name="author")
    assignee = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True, related_name="assignee")

    kanban_board_fields = ["name", "deadline", "author", "assignee"]

