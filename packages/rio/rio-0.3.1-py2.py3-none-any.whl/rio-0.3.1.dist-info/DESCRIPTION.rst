rio(WIP)
========

How to contribute?
-------------------

1. Start from scratch::

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ python setup.py develop
    (venv) $ rio db upgrade
    (venv) $ rio runworker
    (venv) $ rio runserver

2. Please use `gpg` to sign your commits.

How to Test?
--------------

Test::

    (venv) $ pip install -r tests-requirements.txt
    (venv) $ venv/bin/py.test tests


HISTORY
========


v0.3.1
------

* support multiple graph

v0.3.0
------

* support template format webhook url
* add cli command: syncproject
* add cli command: runworker
* add cli command: db
* bugfix

v0.2.4
------

* optimize webhook index

v0.2.2
------

* add Migration resources
* add cli
* add cache for sqlalchemy
* add event uuid
* support form and json payload
* support header for webhook

v0.2.0
------

* add SQLALchemy as graph backend

v0.1.0
------

* initial Release


