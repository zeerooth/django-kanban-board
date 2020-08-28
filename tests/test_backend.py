from django.test import TestCase, Client
from django.http import HttpRequest
from .test_project.models import Task, Person
from kanban_board.models import KanbanBoard, KanbanBoardState, Workflow
import datetime

class BackendTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        workflow = Workflow.objects.create(name="Sample workflow")
        states = [KanbanBoardState.objects.create(name="Waiting", workflow=workflow), KanbanBoardState.objects.create(name="In Progress", workflow=workflow), KanbanBoardState.objects.create(name="Done", workflow=workflow)]
        self.board = KanbanBoard.objects.create(name="TeamworkBoard", workflow=workflow)
        natalie = Person.objects.create(name="Natalie Example", department="management")
        kyosti = Person.objects.create(name="Kyösti Haapalainen", department="sales")
        grzegorz = Person.objects.create(name="Grzegorz Brzęczyszczykiewicz", department="technical")
        self.tasks = [Task.objects.create(name="Conduct a task number 1", kanban_board_state=states[0], kanban_board_parent=self.board, deadline=datetime.datetime(year=2020, month=6, day=1), author=natalie, assignee=grzegorz), 
                      Task.objects.create(name="Conduct a task number 2", kanban_board_state=states[1], kanban_board_parent=self.board, deadline=None, author=kyosti, assignee=None)]
    
    def test_default_element_value(self):
        self.assertEqual(Task.objects.first().kanban_board_state, self.board.states.first())

    def test_field_tuples(self):
        sampleElement = Task.objects.get(name="Conduct a task number 1")
        self.assertEqual(sampleElement.kanban_board_field_tuples(), [("name", "Conduct a task number 1"), ("deadline", '2020-06-01 00:00:00+00:00'), ("author", "Natalie Example"), ("assignee", "Grzegorz Brzęczyszczykiewicz")])
    
    def test_board_view(self):
        response = self.client.get('/kanban-board/' + str(self.board.id) + "/")
        self.assertEqual(response.status_code, 200)
    
    def test_panel_view(self):
        response = self.client.get('/kanban-board/')
        self.assertEqual(response.status_code, 200)
    
    def test_change_status_view(self):
        http_req = HttpRequest()
        http_req.method = "POST"
        http_req.POST = {"kb_parent_id": str(self.board.id), "kb_element_id": str(self.tasks[0].id), "kb_new_status": self.board.states.last().id}
        response = self.client.post('/kanban-board/move-element/', data=http_req.POST)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.get(pk=self.tasks[0].id).kanban_board_state.name, "Done")