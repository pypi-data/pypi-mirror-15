Inheritance
===========

ORMithorynque supports multiple inheritance, as in the following example:

::
   
   >>> class Museum(database.Object):
   ...     name = database.SQLAttribute(str)

   >>> class Room(database.Object):
   ...     name   = database.SQLAttribute(str)
   ...     museum = database.SQLAttribute(object)

   >>> class Artwork(database.Object):
   ...     title  = database.SQLAttribute(str)
   ...     artist = database.SQLAttribute(str)

   >>> class DecoratedRoom(Room, Artwork):
   ...     architect  = database.SQLAttribute(str)

   >>> my_museum = Museum("My virtual museum")
   >>> my_decorated_room = DecoratedRoom(
   ...     museum = my_museum,
   ...     name = "Collumn gallery",
   ...     title = "Column gallery",
   ...     artist = "de Vinci",
   ...     architect = "Vitruve",
   ... )

Instances created from a class that inherits from one (or several) other classes are stored in *several*
rows, one for each table / class. Here, the my_decorated_room instance has 3 rows:

* one in the DecoratedRoom table,
* one in the Room table,
* one in the Artwork table.

All these rows share the same, global, ID.
