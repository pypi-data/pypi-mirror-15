========================================= 
Chi-Squared Automatic Inference Detection
=========================================

This package provides a python implementation of the Chi-Squared Automatic Inference Detection (CHAID) decision tree. More details can be found here_.


Installation
------------

CHAID is distributed via pypi_ and can be installed like:

.. code-block:: bash
	
	pip install CHAID


Creating a Tree
---------------

.. code-block:: python
	
	import CHAID from CHAID

	pandas_data_frame = ...
	independent_variable_columns = ['a', 'b', 'c']
	dep_variable = ['d']
	CHAID.from_pandas_df(df, independent_variable_columns, dep_variable)

Running from the Command Line
-----------------------------

You can play around with the repo by cloning and running this from the command line:

.. code-block:: bash

	python3 -m CHAID CHAID/data/titanic.csv survived sex embarked --max-depth 4 --min-samples 2 --alpha-merge 0.05

It calls the `print_tree()` method, which prints the tree to terminal:

.. code-block:: bash

	([], {'1': 500.0, '0': 809.0}, embarked, 1.0, 0.31731050786291404)
	├── (['C', 'Q'], {'1': 194.0, '0': 199.0}, None, None, 1)
	└── (['S', '<missing>'], {'1': 306.0, '0': 610.0}, None, None, 1)

To get a LibTree object, call to_tree() on the CHAID instance

.. _here: http://www.python.org/
.. _pypi: https://en.wikipedia.org/wiki/CHAID