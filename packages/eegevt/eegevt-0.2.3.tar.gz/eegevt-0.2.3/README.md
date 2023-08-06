Description
===========

A set of modules used for working with EEG event file data. Can load, export and manipulate the data (ready for reuse in EEG analysis software).

Details
-------

Currently can be used for BESA and Neuroscan files
The BESA file handling assumes a specific order of columns and ignores a start marker, future versions will more fully support the specification found at: http://wiki.besa.de/index.php?title=Event\_File\_Format#Event\_Codes

## Updates

Now uses namedtuple for the list of events rather than raw str lists with name positions

### BUGFIXES & FEATURES

#### v0.2.3

* Added a suite of unittests
* Removed unreachable code and various small bugfixes

#### v0.2.2

* Code replacement not working due to immutable namedtuple use, use \_replace method for now

#### v0.2.1

* TypeError fixed, was not parsing lines correctly
