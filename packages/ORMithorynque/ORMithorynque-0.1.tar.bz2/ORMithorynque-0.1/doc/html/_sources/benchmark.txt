Benchmark
=========

The following table shows the result of a small benchmark comparing several Python ORM
for importing the 10000+ terms of the ICD10 medical classifications (writing), and then
for traversing all terms (reading).

All ORM used SQLite3. In addition, plain SQL is also shown for comparison.

Results:

=================  =============  ============  ===============  =============  =======================
Module                Writing       Reading      Database size   Lines of code  Inheritance
=================  =============  ============  ===============  =============  =======================
SQLAlchemy 1.0.13  23.91 seconds  8.07 seconds    962 560 bytes    42 lines     single (?)
SQLObjet 3.0.0      8.32 seconds  2.43 seconds    966 656 bytes    35 lines     single
Peewee 2.8.1        5.72 seconds  2.31 seconds    962 560 bytes    35 lines     single (?)
Pony 0.6.5          5.84 seconds  0.67 seconds    958 464 bytes    35 lines     multiple (partial)
ORMithorynque 0.1   1.81 seconds  0.60 seconds  1 110 016 bytes    31 lines     multiple (full support)
SQL (non-object)    1.30 seconds  0.27 seconds    966 656 bytes    45 lines     none
=================  =============  ============  ===============  =============  =======================

(for numbers, the lower is always the better)

ORMithorynque beats all other ORM for speed. It also require fewer lines of code (mostly thanks to the
automatic schema creation and update).

ORMithorynque databases are slighly bigger than with other ORM however; this result was expected because
ORMithorynque requires an extra table for storing classname, due to multiple inheritance support.
