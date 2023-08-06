**********
sqlservice
**********

|version| |travis| |coveralls| |license|


The missing SQLAlchemy ORM interface.


Links
=====

- Project: https://github.com/dgilland/sqlservice
- Documentation: http://sqlservice.readthedocs.io
- PyPI: https://pypi.python.org/pypi/sqlservice/
- TravisCI: https://travis-ci.org/dgilland/sqlservice


Introduction
============

So what exactly is ``sqlservice`` and what does "the missing SQLAlchemy ORM interface" even mean? SQLAlchemy is a fantastic library and features a superb ORM layer. However, one thing SQLAlchemy lacks is a unified interface for easily interacting with your database through your ORM models. This is where ``sqlservice`` comes in. It's interface layer on top of SQLAlchemy's session manager and ORM layer that provides a single point to manage your database connection/session, create/reflect/drop your database objects, and easily persist/destroy model objects.

Features
--------

This library is meant to enhanced your usage of SQLAlchemy. SQLAlchemy is great and this library tries to build upon that by providing useful abstractions on top of it.

- Database client similar to `Flask-SQLAlchemy <http://flask-sqlalchemy.pocoo.org/>`_ and `alchy.DatabaseManager <http://alchy.readthedocs.io/en/latest/api.html#alchy.manager.Manager>`_ that helps manage an ORM scoped session.
- A model service interface that enhances model access and serialization.
- Base class for a declarative ORM Model that makes updating model columns and relationships easier and converting to a dictionary a breeze.
- A decorator based event registration for SQLAlchemy ORM events that can be used at the model class level. No need to register the event handler outside of the class definition.
- An application-side nestable transaction context-manager that helps implement pseudo-subtransactions for those that want implicit transaction demarcation, i.e. session autocommit, without using session subtransactions.
- And more!


History
-------

This library's direct predecessor is `alchy <https://github.com/dgilland/alchy>`_ which itself started as a drop-in replacement for `Flask-SQLAlchemy <http://flask-sqlalchemy.pocoo.org/>`_ combined with new functionality centering around the "fat-model" style. This library takes a different approach and encourages a "fat-service" style. As such, it is primarily a rewrite of alchy with some of its features ported over and improved, some of its features removed, and other features added. With alchy, one's primary interface with the database was through a model class. Whereas with sqlservice, one's primary interface with the database is through a service class.


Requirements
------------

- Python 2.7 or Python >= 3.4
- `SQLAlchemy <http://www.sqlalchemy.org/>`_ >= 1.0.0
- `pydash <http://pydash.readthedocs.io>`_ >= 3.4.3


Quickstart
==========

First, install using pip:


::

    pip install sqlservice


Then, define some ORM models:

.. code-block:: python

    import re

    from sqlalchemy import Column, ForeignKey, orm, types

    from sqlservice import declarative_base, event


    Model = declarative_base()

    class User(Model):
        __tablename__ = 'user'

        id = Column(types.Integer(), primary_key=True)
        name = Column(types.String(100))
        email = Column(types.String(100))
        phone = Column(types.String(10))

        roles = orm.relation('UserRole')

        @event.on_set('phone', retval=True)
        def on_set_phone(self, value, oldvalue, initator):
            # Strip non-numeric characters from phone number.
            return re.sub('[^0-9]', '', value)

    class UserRole(Model):
        __tablename__ = 'user_role'

        id = Column(types.Integer(), primary_key=True)
        user_id = Column(types.Integer(), ForeignKey('user.id'), nullable=False)
        role = Column(types.String(25), nullable=False)


Next, configure the database client:

.. code-block:: python

    from sqlservice import SQLClient

    config = {
        'SQL_DATABASE_URI': 'sqlite:///db.sql',
        'SQL_ECHO': True,
        'SQL_POOL_SIZE': 5,
        'SQL_POOL_TIMEOUT': 30,
        'SQL_POOL_RECYCLE': 3600,
        'SQL_MAX_OVERFLOW': 10,
        'SQL_AUTOCOMMIT': False,
        'SQL_AUTOFLUSH': True
    }

    db = SQLClient(config, Model=Model)


Prepare the database by creating all tables:

.. code-block:: python

    db.create_all()


Finally (whew!), start interacting with the database:

.. code-block:: python

    # Insert a new record in the database.
    data = {'name': 'Jenny', 'email': 'jenny@example.com', 'phone': '555-867-5309'}
    user = db.User.save(data)


    # Fetch records.
    assert user is db.User.get(data.id)
    assert user is db.User.find_one(id=user.id)
    assert user is db.User.find(User.id == user.id)[0]

    # Serialize to a dict.
    assert user.to_dict() == {'id': 1,
                              'name': 'Jenny',
                              'email': 'jenny@example.com',
                              'phone': '5558675309'}

    assert dict(user) == user.to_dict()

    # Update the record and save.
    user.phone = '222-867-5309'
    db.User.save(user)

    # Upsert on primary key automatically.
    assert user is db.User({'id': 1,
                            'name': 'Jenny',
                            'email': 'jenny@example.com',
                            'phone': '5558675309'})

    # Delete the model.
    db.User.delete(user)
    # OR db.User.delete([user])
    # OR db.User.delete(user.id)
    # OR db.User.delete(dict(user))


For more details, please see the full documentation at http://sqlservice.readthedocs.io.



.. |version| image:: http://img.shields.io/pypi/v/sqlservice.svg?style=flat-square
    :target: https://pypi.python.org/pypi/sqlservice/

.. |travis| image:: http://img.shields.io/travis/dgilland/sqlservice/master.svg?style=flat-square
    :target: https://travis-ci.org/dgilland/sqlservice

.. |coveralls| image:: http://img.shields.io/coveralls/dgilland/sqlservice/master.svg?style=flat-square
    :target: https://coveralls.io/r/dgilland/sqlservice

.. |license| image:: http://img.shields.io/pypi/l/sqlservice.svg?style=flat-square
    :target: https://pypi.python.org/pypi/sqlservice/


Changelog
=========


v0.2.0 (2016-06-15)
-------------------

- Add Python 2.7 compatibility.
- Add concept of ``model_registry`` and ``service_registry`` to ``SQLClient`` class:

  - ``SQLClient.model_registry`` returns mapping of ORM model names to ORM model classes bound to ``SQLClient.Model``.
  - ``SQLService`` instances are created with each model class bound to declarative base, ``SQLClient.Model`` and stored in ``SQLClient.service_registry``.
  - Access to each model class ``SQLService`` instance is available via attribute access to ``SQLClient``. The attribute name corresponds to the model class name (e.g. given a ``User`` ORM model, it would be accessible at ``sqlclient.User``.

- Add new methods to ``SQLClient`` class:

  - ``save``: Generic saving of model class instances similar to ``SQLService.save`` but works for any model class instance.
  - ``destroy``: Generic deletion of model class instances or ``dict`` containing primary keys where model class is explicitly passed in. Similar to ``SQLService.destroy``.

- Rename ``SQLService.delete`` to ``destroy``. (**breaking change**)
- Change ``SQLService`` initialization signature to ``SQLService(db, model_class)`` and remove class attribute ``model_class`` in favor of instance attribute. (**breaking change**)
- Add properties to ``SQLClient`` class:

  - ``service_registry``
  - ``model_registry``

- Add properties to ``Query`` class:

  - ``model_classes``: Returns list of model classes used to during ``Query`` creation.
  - ``joined_model_classes``: Returns list of joined model classes of ``Query``.
  - ``all_model_classes``: Returns ``Query.model_classes`` + ``Query.joined_model_classes``.

- Remove methods from ``SQLService`` class: (**breaking change**)

  - ``query_one``
  - ``query_many``
  - ``default_order_by`` (default order by determination moved to ``Query.search``)

- Remove ``sqlservice.service.transaction`` decorator in favor of using transaction context manager within methods. (**breaking change**)
- Fix incorrect passing of ``SQL_DATABASE_URI`` value to ``SQLClient.create_engine`` in ``SQLClient.__init__``.


v0.1.0 (2016-05-24)
-------------------

- First release.


