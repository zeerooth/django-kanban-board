# Django Kanban Board

description: TODO

## Installation

1. Add `kanban_board` to INSTALLED_APPS in settings.py:
INSTALLED_APPS = [
    ...
    'kanban_board',
]
2. Add the following code to urlpatterns in urls.py:
from django.urls import path
import kanban_board
...
urlpatterns = [
    ...
    path('kanban-board/', kanban_board.urls),
]

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
