# Django Kanban Board

description: TODO

## Installation

1. Add `kanban_board` and `ordered_model` to INSTALLED_APPS in settings.py:

```python
INSTALLED_APPS = [
    ...
    'ordered_model',
    'kanban_board',
]
```

2. Add the following code to urlpatterns in urls.py:

```python
from django.urls import path
import kanban_board
...
urlpatterns = [
    ...
    path('kanban-board/', include('kanban_board.urls')),
]
```

3. Django Kanban Board uses tailwind for rendering its component, so either install it by yourself (https://tailwindcss.com/docs/installation) or simply add it to your template via the files provided in this package:

```html
{% load static %}
...
<link href="{% static 'kanban_board/css/tailwind.min.css' %}" rel="stylesheet">
```

4. In your projects' models.py create a new model that inherits from kanban_board.models.KanbanBoardElement:

```python
class Task(KanbanBoardElement):
    name = models.CharField("TaskName", max_length=65535)
    deadline = models.DateTimeField("Deadline", blank=True, null=True)
    # add other fields

    kanban_board_fields = ["name", "deadline"] # here assign which of them will be displayed on your kanban boards
```

#### The beauty here lies in the fact that you can create elements for kanban boards using your existing models!

## Development

### Poetry

1. Download and install poetry (https://github.com/K900/poetry#installation)
2. Run poetry install and poetry shell to access the environment
3. source (yourenv file).sh to activate environment variables
4. Done!

### Packaging and publishing

1. poetry build
2. Make sure you have correct credentials set up (https://python-poetry.org/docs/repositories/#adding-credentials)
3. poetry publish

### Generating setup.py from pyproject.toml

1. dephell deps convert
