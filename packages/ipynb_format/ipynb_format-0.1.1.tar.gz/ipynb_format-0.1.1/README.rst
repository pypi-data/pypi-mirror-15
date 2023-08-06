============
ipynb_format
============

``ipynb_format.py`` is a small script to format the python code in ipython notebooks.
The code formatter is based on yapf_.

.. _yapf: https://github.com/google/yapf.


Installation
============

To install from PyPI on Linux:

.. code-block:: shell

    $ pip install ipynb_format

or from Github:

.. code-block:: shell

    $ pip install --upgrade https://github.com/fg1/ipynb_format/archive/master.tar.gz


Usage
=====

.. code-block:: shell

    usage: ipynb_format [-h] [--style STYLE] [files [files ...]]
    
    Format ipython notebook using yapf
    
    positional arguments:
      files
    
      optional arguments:
        -h, --help     show this help message and exit
        --style STYLE  yapf style to use


The formatting style option is the same as for ``yapf``.
