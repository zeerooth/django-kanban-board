from django.test import TestCase, Client
from django.http import HttpRequest
from django.contrib.auth.models import User
from .test_project.models import Task, Person
from kanban_board.models import KanbanBoard, KanbanBoardState, Workflow
import datetime

class BackendTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.privileged_user = User.objects.create_superuser(username='priv_user')
        self.guest_user = User.objects.create(username='guest_user')
        for user in [self.privileged_user, self.guest_user]:
            user.set_password('passwd')
            user.save()
        self.client.login(username='priv_user', password='passwd')
        workflow = Workflow.objects.create(name="Sample workflow")
        states = [KanbanBoardState.objects.create(name="Waiting", workflow=workflow), KanbanBoardState.objects.create(name="In Progress", workflow=workflow), KanbanBoardState.objects.create(name="Done", workflow=workflow)]
        self.board = KanbanBoard.objects.create(name="TeamworkBoard", workflow=workflow)
        natalie = Person.objects.create(name="Natalie Example", department="management")
        kyosti = Person.objects.create(name="Kyösti Haapalainen", department="sales")
        grzegorz = Person.objects.create(name="Grzegorz Brzęczyszczykiewicz", department="technical")
        self.tasks = [Task.objects.create(name="Task number 1", kanban_board_parent=self.board, deadline=datetime.datetime(year=2020, month=6, day=1), author=natalie, assignee=grzegorz), 
                      Task.objects.create(name="Task number 2", kanban_board_state=states[1], kanban_board_parent=self.board, deadline=None, author=kyosti, assignee=None)]
    
    def test_default_element_value(self):
        self.assertEqual(Task.objects.get(name="Task number 1").kanban_board_state, self.board.workflow.kanbanboardstate_set.first())

    def test_field_tuples(self):
        sampleElement = Task.objects.get(name="Task number 1")
        self.assertEqual(sampleElement.kanban_board_field_tuples(), [("name", "Task number 1"), ("deadline", '2020-06-01 00:00:00+00:00'), ("author", "Natalie Example"), ("assignee", "Grzegorz Brzęczyszczykiewicz")])
    
    def test_board_view(self):
        response = self.client.get('/kanban-board/' + str(self.board.id) + "/")
        print(response)
        self.assertEqual(response.status_code, 200)
    
    def test_panel_view(self):
        response = self.client.get('/kanban-board/')
        self.assertEqual(response.status_code, 200)
    
    def test_change_status_view(self):
        data = {"kb_parent_id": str(self.board.id), "kb_element_id": str(self.tasks[1].id), "kb_new_status": self.board.workflow.kanbanboardstate_set.last().id}
        response = self.client.post('/kanban-board/move-element/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.get(pk=self.tasks[1].id).kanban_board_state.name, "Done")