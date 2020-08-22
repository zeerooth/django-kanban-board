from django.test import TestCase, Client
from django.http import HttpRequest
from .test_project.models import GeneralBoard, Task, Person
import datetime

class BackendTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.board = GeneralBoard.objects.create(name="TeamworkBoard")
        natalie = Person.objects.create(name="Natalie Example", department="management")
        kyosti = Person.objects.create(name="Kyösti Haapalainen", department="sales")
        grzegorz = Person.objects.create(name="Grzegorz Brzęczyszczykiewicz", department="technical")
        self.task1 = Task.objects.create(name="Conduct a task number 1", kanban_board_state='waiting', deadline=datetime.datetime(year=2020, month=6, day=1), author=natalie, assignee=grzegorz)
        self.task2 = Task.objects.create(name="Conduct a task number 2", kanban_board_state='under_review', deadline=None, author=kyosti, assignee=None)
        self.board.elements = [self.task1, self.task2]

    def test_field_tuples(self):
        sampleElement = Task.objects.get(name="Conduct a task number 1")
        self.assertEqual(sampleElement.kanban_board_field_tuples(), [("name", "Conduct a task number 1"), ("deadline", '2020-06-01 00:00:00+00:00'), ("author", "Natalie Example"), ("assignee", "Grzegorz Brzęczyszczykiewicz")])
    
    def test_board_view(self):
        response = self.client.get('/kanban-board/' + str(self.board.id) + "/")
        self.assertEqual(response.status_code, 200)
    
    def test_change_status_view(self):
        http_req = HttpRequest()
        http_req.method = "POST"
        http_req.POST = {"kb_parent_id": str(self.board.id), "kb_element_id": str(self.task1.id), "kb_new_status": "completed"}
        response = self.client.post('/kanban-board/move-element/', data=http_req.POST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.get(pk=self.task1.id).kanban_board_state, "completed")