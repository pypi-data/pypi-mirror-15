Welcome to ORMithorynque's documentation!
*****************************************

ORMithorynque is an ORM (Object Relational Mapper), that is to say an object-oriented database
built on top of a relational database (SQLite3).
ORMithorynque allows to save and reload Python object in a database, and to perform complex
and optimized request on the database.
ORMithorynque can be seen as SQLite3 with objects and (multiple) inheritance,
or Python object system with SQL queries.

ORMithorynque was initially written as a challenge to write a little ORM for Python with multiple inheritance
(a feature very few existing ORM support). But it soon appeared that the multiple inheritance support
lead to a very neat and efficient inner structure, and impressive performances.


The key features of ORMithorynque are:

* Very good performance thanks to prebuilt requests and agressive caching
  (faster than SQLAlchemy, SQLObject, Pony and Peewee, see :doc:`benchmark`)
* Automatic database schema update when adding new tables, new columns or new indexes
* Single and multiple inheritance support
* Transactions
* Native SQL queries
* Funny name [#f1]_ :)

And its main drawbacks are:
  
* Support a single database backend (SQLite3)
* No specific high-level query language
* Not thread-safe


ORMithorynque is available under the GNU LGPL licence v3.
It requires Python 3.2 (or more) or Pypy 3.


Table of content
----------------

.. toctree::
   tuto.rst
   relation.rst
   querying.rst
   inheritance.rst
   transaction.rst
   benchmark.rst

.. [#f1] an ornithorynque (or platypus) is a strange animal,
         somehow a mix of a duck and a mammal -- similarly ORMithorynque
         is a mix of the object and the relational paradigm.

