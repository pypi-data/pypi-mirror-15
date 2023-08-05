=============
Storage Stats
=============

Calculates statistics about minimum, maximum and mean average file sizes for each file extension within a directory.

|license|

Intallation
===========

::

    pip install storage_stats

Documentation
=============

Usage: ``storage_stats [-h] [-o OUTPUT] [--no-recursion] [-s] path``

Calculates file size statistics for the specified folder

positional arguments:
  path            the folder to characterise

optional arguments:
  -h, --help      show this help message and exit
  -o OUTPUT       CSV file to output statistics too
  --no-recursion  do not include sub-folders in stats
  -s, --silent    turn off command line output (useful if you just want to
                  output a CSV file

Licence
=======

Released under `Apache version 2.0 license <LICENSE>`_.

Contribute
==========

1. `Fork the GitHub project <https://help.github.com/articles/fork-a-repo>`_
2. Change the code and push into the forked project
3. `Submit a pull request <https://help.github.com/articles/using-pull-requests>`_


.. |license| image:: https://img.shields.io/badge/license-Apache%20V2-blue.svg
   :target: https://github.com/pmay/storage-stats/blob/master/LICENSE
   :alt: Apache V2
