Description
===========

A set of modules used for working with EEG event file data. Can load, export and manipulate the data (ready for reuse in EEG analysis software).

Details
-------

Currently can be used for BESA and Neuroscan files

## Updates

Now uses namedtuple for the list of events rather than raw str lists with name positions

### BUGFIXES

#### v0.2.2

* Code replacement not working due to immutable namedtuple use, use \_replace method for now

#### v0.2.1

* TypeError fixed, was not parsing lines correctly
