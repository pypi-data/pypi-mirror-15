Getting started
===============

Installation
------------

To install ORMithorynque, type the following command into the command prompt (with root permission):

::

   pip install ormithorynque


Opening / creating a database
-----------------------------

To open an ORMithorynque database, simply import the "ormithorynque" Python module and create an instance
of the Database class with the filename of the database. If the database does not exist, it is automatically
created.

::

   >>> import ormithorynque
   
   >>> database = ormithorynque.Database("database_filename.sqlite3")

A database can also be created in memory:

::

   >>> database = ormithorynque.Database(":memory:")
   
Finally, you can turn on the "debug mode" to see any SQL request performed by ORMithorynque:

::

   >>> database = ormithorynque.Database(":memory:", debug_sql = True)


Creating a class
----------------

Classes in the database are created by inheriting from the :class:`database.Object` class.
The attributes that are stored in the database must be listed as in the following example:

::

   >>> class Person(database.Object):
   ...     name       = database.SQLAttribute(str, indexed = True)
   ...     first_name = database.SQLAttribute(str)
   ...     age        = database.SQLAttribute(int)

A table is automatically created in the SQLite3 database, with the same name than the class (here, "Person")
and one column per attribute (with the same names too). If the table already exists, it is automatically updated
with any new attribute / column.

Here, the following SQL table and index are automatically created:

::
   
   create table Person (
       id integer primary key autoincrement,
       first_name text,
       name text,
       age integer
   );
   create index Person_name_index on Person(name);


The following datatypes are supported by ORMithorynque:

* :class:`str` : Python Unicode string (TEXT in SQL)
* :class:`bytes` : binary data (BLOB)
* :class:`int` : integer number (INTEGER)
* :class:`float` : real number (REAL)
* :class:`datetime.date` : date (DATA)
* :class:`datetime.datetime` : date and time (TIMESTAMP)
* :class:`object` : a Python object, of any class inheriting from :class:`database.Object` (in SQL, an INTEGER ID field)

Notice that ORMithorynque does not statically type objects: an attribute of the type :class:`object` can
received *any* object.
  
In addition, a default value can be provided instead of the attribute type. In this case, the type is guessed
from the default value.

If the :attr:`indexed` optional parameters to :func:`database.SQLAttribute()` is True, an index is created for this
attribute.

.. note::

   ORMithorynque automatically adds an :attr:`id` INTEGER attribute; :attr:`id` is a reserved attribute name
   so please don't add your own ID !

   Notice that ORMithorynque's ID are global ID, and not per-table ID as usual in relational databases.


Creating an instance
--------------------

To create an instance of the class, simply call the class and pass any attribute values as named-parameter:

::

   >>> jiba = Person(name = "Lamy", first_name="Jean-Baptiste", age = 36)
   >>> jiba
   <Person id=1 first_name='Jean-Baptiste' name='Lamy' age=36>

Any missing attribute takes a default value (the one specified to :func:`database.SQLAttribute()`,
or "" for string, 0 for int, None for object,...).

The object is automatically created and stored in the database.
Here, the object received the ID 1 in the database.


Updating instances
------------------

Instances can be updated as any Python object:

::

   jiba.age = 37 # Yay, it's my bithday!

The database is automatically updated.

