Relations
=========

One-to-many relations
---------------------

ORMithorynque supports one-to-one, one-to-many and many-to-many relations.
In order to create relations, we need to create more classes in our example, so we are adding a House class
and updating the Person class -- ORMithorynque will automatically create the new House table and update
the Person one!

Here, we have an example of a one-to-many relation
(a House has one owner Person, a Person can own many House):

::

   >>> class House(database.Object):
   ...     address = database.SQLAttribute("Nowhere") # String attribute with a default value
   ...     owner   = database.SQLAttribute(object)
   
   >>> class Person(database.Object):
   ...     name       = database.SQLAttribute(str, indexed = True)
   ...     first_name = database.SQLAttribute(str)
   ...     age        = database.SQLAttribute(int)
   ...     houses     = database.SQLOneToMany("House", "owner")

   >>> someone = Person(name = "Some", first_name="One")
   
   >>> house1 = House(address = "Somewhere", owner = someone)
   >>> house2 = House(address = "Somewhere else")

   >>> someone.houses
   [<House id=3 address='Somewhere' owner=<Person id=2 first_name='One' name='Some' age=0>>]

:func:`database.SQLOneToMany` expects two parameters: the name of the other table / class, and the name of the
corresponding attribute / column in the other table.

ORMithorynque automatically adds index for attributes involved in relations.
   
To update the relation, simply modify the value at its "one" side:

::

   >>> house2.owner = someone
   >>> someone.houses
   [<House id=3 address='Somewhere' owner=<Person id=2 first_name='One' name='Some' age=0>>, <House id=8 address='Somewhere else' owner=<Person id=2 first_name='One' name='Some' age=0>>]

.. warning::

   On the contrary, **do not** modify the list returned by the one-to-many relation:

   ::
      
      someone.houses.append(house2) # Don't do that!

      
Many-to-many relations
----------------------

In the following example, we have an example of a many-to-many relation
(a House can have many inhabitant Person, a Person can live in many House --
not at the same time but for example in a house during the week and another one for the week-end):

::
   
   >>> class House(database.Object):
   ...     address     = database.SQLAttribute("Nowhere") # String attribute with a default value
   ...     owner       = database.SQLAttribute(object)
   ...     inhabitants = database.SQLManyToMany("inhabitant", "lives_in")
   
   >>> class Person(database.Object):
   ...     name        = database.SQLAttribute(str, indexed = True)
   ...     first_name  = database.SQLAttribute(str)
   ...     age         = database.SQLAttribute(int)
   ...     houses      = database.SQLOneToMany("House", "owner")
   ...     lives_in    = database.SQLManyToMany("lives_in", "inhabitant")
   
   >>> someone1 = Person(name = "Some", first_name="One")
   >>> someone2 = Person(name = "Some", first_name="Two")
   
   >>> house1 = House(address = "Somewhere")
   >>> house2 = House(address = "Somewhere else")
   
   >>> someone1.add_lives_in(house1)
   >>> house1.add_inhabitant(someone2)
   >>> house1.inhabitants
   [<Person id=5 first_name='One' name='Some' age=0>, <Person id=6 first_name='Two' name='Some' age=0>]
   
   >>> house1.remove_inhabitant(someone2)
   >>> house1.inhabitants
   [<Person id=5 first_name='One' name='Some' age=0>]

:func:`database.SQLManyToMany` expects two parameters: the name of the attribute in this table,
and the name of the attribute in the other table. The two names are expected to be singular
(e.g. "inhabitant" and not "inhabitant **s**").

ORMithorynque automatically creates a table for the relation
(named "relation_attribute1_attribute2", here "relation_inhabitant_lives_in") and an index for this table.

In addition, the :meth:`House.add_inhabitant()`, :meth:`House.remove_inhabitant()`,
:meth:`Person.add_lives_in()` and :meth:`Person.remove_lives_in()` methods are automatically created.

.. warning::

   To modify the data, the add/remove methods must be used, **do not** modify the list returned by
   the many-to-many relation:

   ::
      
      someone1.lives_in.append(house1) # Don't do that!
      house1.inhabitants.append(someone1) # Don't do that!


One-to-one relations
--------------------

One-to-one relations are created with :func:`database.SQLOneToOne`, which is very similar to
:func:`database.SQLOneToMany`, excepted that the relation return a single object instead of a list.


Self-referencing relations
--------------------------

ORMithorynque supports self-referencing relations, as in the following example:

::
   
   >>> class Node(database.Object):
   ...     data     = database.SQLAttribute(bytes)
   ...     parent   = database.SQLAttribute(object)
   ...     children = database.SQLOneToMany("Node", "parent")

