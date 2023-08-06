Querying
========

ORMithorynque does not provide a specific query language but uses SQL.

You can either use the :attr:`database.cursor` plain SQLite3 database cursor, or use the more convenient
:meth:`database.select_one()`, :meth:`database.select_all()`, :meth:`database.select_object_one()` and
:meth:`database.select_object_all()` methods described here.

:meth:`database.select_one()` execute an SQL SELECT query and return one row as a tuple; it is equivalent to an
:func:`execute()` followed by a :func:`fetchone()` call. For example:

::

   >>> database.select_one("select max(age) from Person")
   (37,)
   >>> database.select_one("select count(id) from Person")
   (4,)


:meth:`database.select_all()` execute an SQL SELECT query and return all rows (as tuples); it is equivalent to an
:func:`execute()` followed by a :func:`fetchall()` call. For example:

::

   >>> database.select_all("select age from Person where name = 'Some'") # The age of all Person named 'Some'
   [(0,), (0,), (0,)]
   
:meth:`database.select_one_object()` execute an SQL SELECT query on a single ID and return the
corresponding object. For example:

::

   >>> database.select_object_one("select id from Person where name='Lamy'")
   <Person id=1 first_name='Jean-Baptiste' name='Lamy' age=37>

   
:meth:`database.select_all_object()` execute an SQL SELECT query on ID and return the list of
corresponding objects. For example:

::

   >>> database.select_object_all("select id from Person where name='Some'")
   [<Person id=2 first_name='One' name='Some' age=0>, <Person id=5 first_name='One' name='Some' age=0>, <Person id=6 first_name='Two' name='Some' age=0>]


Finally, the database can be indiced with ID to obtain the object of the corresponding ID:

::

   >>> database[1]
   >>> database.get(1) # Return None if no object exists for this ID


The ID can be used to join the various tables. Remember that ID are global in ORMithorynque (not per-table).
