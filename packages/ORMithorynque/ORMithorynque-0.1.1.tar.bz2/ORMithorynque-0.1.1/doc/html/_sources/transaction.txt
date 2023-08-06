Transactions
============

By default, ORMithorynque works in "auto-commit" mode: any change to an object in the database is immediately
saved in the database.

However, ORMithorynque supports transactions as in the following example:

::

   database.begin_transaction()
   
   # Modify database's objects here
   
   if *something_goes_bad*:
       database.rollback()
       
   else:
       database.end_transaction()

A context / with-statement syntax is also provided:

::

   with database.transaction:
       # Modify database's objects here
       #
       # If *something goes bad*, raise an exception

In addition, when modifying objects inside a transaction, ORMithorynque tries to reduce the number of
SQL request executed. For example, in the following example, two UPDATE request are performed, one for each
modified attribute:

::

   obj = database[1] # Get an object
   obj.name       = "NewName"
   obj.first_name = "NewFirstName"
   
On the contrary, in the following example, a single update request is performed, when the transaction is ended:
   
::
   
   with database.transaction:
       obj = database[1] # Get an object
       obj.name       = "NewName"
       obj.first_name = "NewFirstName"
   
As a consequence, do **not** expect the database to be updated immediately during a transaction.
