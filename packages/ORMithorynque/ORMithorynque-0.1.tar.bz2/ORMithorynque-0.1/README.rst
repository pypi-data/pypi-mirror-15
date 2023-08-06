ORMithorynque
=============

ORMithorynque is an ORM (Object Relational Mapper), that is to say an object-oriented database
built on top of a relational database (SQLite3).
ORMithorynque allows to save and reload Python object in a database, and to perform complex
and optimized request on the database.
ORMithorynque can be seen as SQLite3 with objects and (multiple) inheritance,
or Python object system with SQL queries.

The key features of ORMithorynque are:

* Very good performance thanks to prebuilt requests and agressive caching
  (faster than SQLAlchemy, SQLObject, Pony and Peewee, see :doc:`benchmark`)
* Automatic database schema update when adding new tables, new columns or new indexes
* Single and multiple inheritance support
* Transactions
* Native SQL queries
* Funny name :)

And its main drawbacks are:
  
* Support a single database backend (SQLite3)
* No specific high-level query language
* Not thread-safe

ORMithorynque is available under the GNU LGPL licence v3.
It requires Python 3.2 (or more) or Pypy 3.

  
Installation
------------

To install ORMithorynque, type the following command into the command prompt (with root permission):

::

   pip install ormithorynque


What can I do with ORMithorynque?
---------------------------------

Open an ORMithorynque database from a filename (if the database does not exist, it is automatically created):

::

   >>> import ormithorynque
   
   >>> database = ormithorynque.Database("database_filename.sqlite3")

Create two classes, with a one-to-many relation between them (tables are automatically created with the class
if they do not exist; if they exist, they are automatically updated with new column if needed):

::
   
   >>> class Person(database.Object):
   ...     name       = database.SQLAttribute(str, indexed = True)
   ...     first_name = database.SQLAttribute(str)
   ...     houses     = database.SQLOneToMany("House", "owner")
   
   >>> class House(database.Object):
   ...     address = database.SQLAttribute("Nowhere") # String attribute with a default value
   ...     owner   = database.SQLAttribute(object)

Create two instances (database is automatically updated):

::
   
   >>> someone = Person(name = "Some", first_name="One")
   
   >>> house = House(address = "Somewhere", owner = someone)

The attributes of the instances can be accessed and modified (database is automatically update):

::

   >>> someone.name
   Some
   >>> someone.name = "Some2"
   
   >>> someone.houses
   [<House id=2 address='Somewhere' owner=<Person id=1 first_name='One' name='Some2'>>]

Finally, plain SQL can be used to query the database:

::

   >>> database.select_one("select count(id) from Person")
   (1,)
   
   
Changelog
---------

0.1
***

* First release


Links
-----

ORMithorynque on BitBucket (development repository): https://bitbucket.org/jibalamy/ormithorynque

ORMithorynque on PyPI (Python Package Index, stable release): https://pypi.python.org/pypi/ormithorynque

Documentation: http://pythonhosted.org/ORMithorynque

Mail me for any comment, problem, suggestion or help !

Jiba -- Jean-Baptiste LAMY -- jibalamy @ free.fr
