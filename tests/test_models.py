from django.test import TestCase, Client
from .test_project.models import GeneralBoard, Task, Person
import datetime

class BoardTestCase(TestCase):
    def setUp(self):
        self.board = GeneralBoard.objects.create(name="TeamworkBoard")
        natalie = Person.objects.create(name="Natalie Example", department="management")
        kyosti = Person.objects.create(name="Kyösti Haapalainen", department="sales")
        grzegorz = Person.objects.create(name="Grzegorz Brzęczyszczykiewicz", department="technical")
        Task.objects.create(name="Conduct a task number 1", kanban_board_parent=self.board, kanban_board_state='waiting', deadline=datetime.datetime(year=2020, month=6, day=1), author=natalie, assignee=grzegorz)
        Task.objects.create(name="Conduct a task number 2", kanban_board_parent=self.board, kanban_board_state='under_review', deadline=None, author=kyosti, assignee=None)


    def test_field_tuples(self):
        sampleElement = Task.objects.get(name="Conduct a task number 1")
        self.assertEqual(sampleElement.kanban_board_field_tuples(), [("name", "Conduct a task number 1"), ("deadline", '2020-06-01 00:00:00+00:00'), ("author", "Natalie Example"), ("assignee", "Grzegorz Brzęczyszczykiewicz")])
    
    def test_views(self):
        c = Client()
        response = c.get('/kanban-board/' + str(self.board.id))
        self.assertRedirects(response, '/kanban-board/' + str(self.board.id) + "/", status_code=301)