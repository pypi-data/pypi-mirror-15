.. image:: https://travis-ci.org/MacHu-GWU/uszipcode-project.svg?branch=master

.. image:: https://img.shields.io/pypi/v/uszipcode.svg

.. image:: https://img.shields.io/pypi/l/uszipcode.svg

.. image:: https://img.shields.io/pypi/pyversions/uszipcode.svg


Welcome to uszipcode Documentation
==================================
``uszipcode`` is the most powerful and easy to use zipcode information searchengine in Python. Besides geometry data (also boundary info), several useful census data points are also served: `population`, `population density`, `total wage`, `average annual wage`, `house of units`, `land area`, `water area`. The geometry and geocoding data I am using is from google map API on Oct 2015. To know more about the data, `click here <http://pythonhosted.org/uszipcode/uszipcode/data/__init__.html#module-uszipcode.data>`_. `Another pupolar zipcode Python extension <https://pypi.python.org/pypi/zipcode>`_ has lat, lng accuracy issue, which doesn't give me reliable results of searching by coordinate and radius.

**Highlight**:

1. `Rich methods <http://pythonhosted.org/uszipcode/index.html#list-of-the-way-you-can-search>`_ are provided for getting zipcode anyway you want. 
2. `Fuzzy city name and state name <http://pythonhosted.org/uszipcode/index.html#search-by-city-and-state>`_ allows you to search **WITHOUT using exactly accurate input**. **This is very helpful if you need to build a web app with it**.
3. You can easily `sort your results <http://pythonhosted.org/uszipcode/index.html#sortby-descending-and-returns-keyword>`_ by `population`, `area`, `wealthy` and etc...


**Quick Links**
-------------------------------------------------------------------------------
- `GitHub Homepage <https://github.com/MacHu-GWU/uszipcode-project>`_
- `Online Documentation <http://pythonhosted.org/uszipcode>`_
- `PyPI download <https://pypi.python.org/pypi/uszipcode>`_
- `Install <install_>`_
- `Issue submit and feature request <https://github.com/MacHu-GWU/uszipcode-project/issues>`_
- `API reference and source code <http://pythonhosted.org/uszipcode/uszipcode/searchengine.html#uszipcode.searchengine.ZipcodeSearchEngine>`_


.. _install:

Install
-------------------------------------------------------------------------------

``uszipcode`` is released on PyPI, so all you need is:

.. code-block:: console

	$ pip install uszipcode

To upgrade to latest version:

.. code-block:: console

	$ pip install --upgrade uszipcode