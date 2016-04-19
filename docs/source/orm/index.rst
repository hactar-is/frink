ORM
===

The ORM part of Frink gives you very basic querying abilities. For anything a little more complex you should probably just drop down to :ref:`ReQL` anyway.


Unique Fields
-------------

You can specify that fields need to be unique by adding them to your model's ``_uniques``. Every field included in ``_uniques`` is, by definition, also required.

::

    class MyModel(BaseModel):

        __metaclass__ = ORMMeta
        _uniques = ['username', 'email']

    username = StringType(required=True)
    email = StringType()


Querying
--------

Get a single instance by id.

::

    User.query.get('9353b884-591b-404f-a4e2-30334d5ad335')

Get all instances.

::

    User.query.all()

Get all instances, ordered and limited.

::

    User.query.all(order_by='firstname', limit=10)

Filtering
~~~~~~~~~

Get a single instance, that is the first to match the filter.

::

    User.query.first(firstname='Jeff')

Get a list of results matching kwargs filters.

::

    User.query.filter(active=True, firstname='Jeff')

Order the results by firstname ascending.

::

    User.query.filter(active=True, firstname='Jeff', order_by='<name')

Order the results by firstname descending.

::

    User.query.filter(active=True, firstname='Jeff', order_by='>name')

Limit the results.

::

    User.query.filter(active=True, firstname='Jeff', order_by='>name', limit=10)


Find all instances that match one column / value.

::

    User.query.find_by(column='firstname', value='Jeff')

Ordered and limited.

::

    User.query.find_by(column='firstname', value='Jeff', order_by='lastname', limit=1)

Get a single instance matched on column / value.

::

    User.query.get_by(column='firstname', value='Jeff')

.. TODO ::

    Add an ``offset`` parameter to all methods that have a ``limit`` argument for use with pagination.


.. _ReQL:

ReQL
----

The models all contain references to the database and the table that they're stored in, just in case you ever need to dynamically create a ReQL query. It's also fairly useful even if you're writing them by hand.

::

    r.db(User._db).table(User._table).filter({"firstname": "Jeff"}).run(conn)
