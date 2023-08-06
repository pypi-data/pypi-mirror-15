===============
 pygments-dmdl
===============

DMDL lexer and highlighter for Pygments

Installation
============

from PyPI
---------

.. code-block:: bash

   pip install pygments-dmdl

from source code
----------------

.. code-block:: bash

   git clone <repo_url>
   cd .../pygments-dmdl
   python setup.py install

How to use
==========

You do not need any configuration in conf.py.

.. code-block:: rst

   .. code-block:: dmdl

      "desc"
      @attribute
      sample = {
          id : INT;
          name : TEXT;
      };


