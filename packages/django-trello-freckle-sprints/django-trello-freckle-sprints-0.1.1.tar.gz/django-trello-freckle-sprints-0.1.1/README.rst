Django Trello Freckle Sprints
=============================

A reusable Django app that helps connection Freckle time entries with Trello
cards.

On Freckle, when you track time that has been spent on a certain card, just add
``cXXX`` to the entry description, where ``XXX`` is the card-ID from Trello
(you can see that in the URL when you open a card).

For more information, see chapter Usage below.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-trello-freckle-sprints

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/django-trello-freckle-sprints.git#egg=sprints

Add ``sprints`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'sprints',
    )

Add the ``sprints`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = [
        url(r'^sprints/', include('sprints.urls')),
    ]


Settings
--------

TRELLO_DEVELOPER_KEY
++++++++++++++++++++

Set this to your [Trello developer key](https://trello.com/1/appKey/generate).

TRELLO_DEVELOPER_SECRET
+++++++++++++++++++++++

Set this to your [Trello developer secret](https://trello.com/1/appKey/generate).

TRELLO_OAUTH_TOKEN
++++++++++++++++++

TODO: Describe how to get the tokens

Set this to your oauth token. To obtain your secret you can run
``ipdb``::

    from trello.util import create_oauth_token
    create_oauth_token(expiration='never', scope='read', key='yourkey', secret='yoursecret')
    # follow the instructions and note down your token and secret


TRELLO_OAUTH_TOKEN_SECRET
+++++++++++++++++++++++++

Set this to your oauth token secret.

FRECKLE_API_TOKEN
+++++++++++++++++

Set this to your Freckle API token. You can find it under ``Settings > API``.

FRECKLE_ACCOUNT_NAME
++++++++++++++++++++

Set this to your Freckle account name. This is the subdomain you use when
logging into Freckle.


Usage
-----

Sprint planning
+++++++++++++++

To get an overview over your current backlog, visit ``/sprints/backlog/``.
Enter the Trello board ID, the lists numbers that contain your backlog and your
hourly rate.

You will see a table that shows the estimated time and cost for each card in
the selected lists. The total will give you an idea about how expensive the
whole project will be in total, given the current feature scope.

In order to plan your next sprint, enable the checkboxes next to each card
until the selected total matches the budget or hours that you can spend on the
sprint.

Sprint overview
+++++++++++++++

To get an overview over a sprint, visit ``/sprints/sprint/``.

TODO: Explain more

Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-trello-freckle-sprints
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
