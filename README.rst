
Django Kanban Board
===================

description: TODO

Installation
------------


#. Add ``kanban_board`` to INSTALLED_APPS in settings.py:

.. code-block:: python

   INSTALLED_APPS = [
       ...
       'kanban_board',
   ]


#. Add the following code to urlpatterns in urls.py:

.. code-block:: python

   from django.urls import path
   import kanban_board
   ...
   urlpatterns = [
       ...
       path('kanban-board/', include('kanban_board.urls')),
   ]


#. Django Kanban Board uses tailwind for rendering its component, so either install it by yourself (https://tailwindcss.com/docs/installation) or simply add it to your template via the files provided in this package:

.. code-block:: html

   {% load static %}
   ...
   <link href="{% static 'kanban_board/css/tailwind.min.css' %}" rel="stylesheet">


#. In your projects' models.py create a new model that inherits from kanban_board.models.KanbanBoardElement:

.. code-block:: python

   class Task(KanbanBoardElement):
       name = models.CharField("TaskName", max_length=65535)
       deadline = models.DateTimeField("Deadline", blank=True, null=True)
       # add other fields

       kanban_board_fields = ["name", "deadline"] # here assign which of them will be displayed on your kanban boards

The beauty here lies in the fact that you can create elements for kanban boards using your existing models!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Development
-----------

Poetry
^^^^^^


#. Download and install poetry (https://github.com/K900/poetry#installation)
#. Run poetry install and poetry shell to access the environment
#. source (yourenv file).sh to activate environment variables
#. Done!

Packaging and publishing
^^^^^^^^^^^^^^^^^^^^^^^^


#. poetry build
#. Make sure you have correct credentials set up (https://python-poetry.org/docs/repositories/#adding-credentials)
#. poetry publish

Generating setup.py from pyproject.toml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


#. dephell deps convert
