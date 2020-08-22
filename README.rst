
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
