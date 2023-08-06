Celery-Tryton
=============

Celery integration with Tryton.
It defines an abstract base Task class that runs inside a Tryton transaction.
If the task is called from within a Tryton transaction, the context of this one
will be automatically restored when the worker will execute it.

Getting Started
---------------

Here is a simple application::

    from celery import Celery
    from celery_tryton import TrytonTask, celery_app
    from trytond.pool import Pool

    celery_app.conf.TRYTON_DATABASE = 'test'

    @celery.task(base=TrytonTask)
    def hello(user_id):
        User = Pool().get('res.user')
        user = User(user_id)
        return 'hello world, %s' % user.name

Configuration
-------------

All standard celery configuration options will work but in addition
`TRYTON_DATABASE` must be set to the default Tryton database name and
optionally `TRYTON_CONFIG` to load a specific configuration file.

The `celery_app` will load the configuration from the `config` value from the
section `[celery]` defined in the trytond configuration when used from a Tryton
module.

Example
-------

Start a worker::

    $ celery worker --app=examples.purchase_requests

Call `generate_all` task::

    $ celery call examples.purchase_requests.generate_all

To report issues please visit the `celery_tryton bugtracker`_.

.. _celery_tryton bugtracker: http://celery-tryton.b2ck.com/


