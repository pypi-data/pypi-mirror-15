Instrospective Factory pattern library
======================================

.. image:: https://travis-ci.org/engine-cl/ng-factory.svg
    :target: https://travis-ci.org/engine-cl/ng-factory

.. image:: https://codecov.io/github/engine-cl/ng-factory/coverage.svg?branch=master
    :target: https://codecov.io/github/engine-cl/ng-factory?branch=master

.. image:: https://www.quantifiedcode.com/api/v1/project/f57003898f714494b2a6f2bb66516a18/badge.svg
    :target: https://www.quantifiedcode.com/app/project/f57003898f714494b2a6f2bb66516a18

Overview
--------

Python 3 object factory pattern implementation.
The principal idea is keep it simple and readable, the main function provide a mechanism to factorize any object
with introspection and don't make the horrible code conditions commonly showed in factory_ examples:

.. _factory: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html

.. code-block:: python

  def factory(type):
      if type == 'MyClass': 
          return MyClass()
      if type == 'MyOtherClass': 
          return MyOtherClass()


So, this module factorize any class from any module and works only in python 3
for python 2 don't make any sense wasted time adapting differences between both version
also is important know which this module only factorize classes or functions from modules
so if can't __import__ them, raises an exception, and if you want factorize class or function
who is in the same module you need make it reachable to the __import__ statement


Installation
------------

.. code-block:: bash

  git clone https://github.com/engine-cl/ng_factory.git
  cd ng-factory
  python3 setup.py install
  pip install ng_factory


Testing
-------

.. code-block:: shell

  python test/factory.py


Example
-------

Create any module with your atomic class encapsulation with GOPS and then factorize object to inject the dependencies 
into the business logic like persistence layer or any another layer.

.. code-block:: python

  from ng_factory import factorize
  class persistence(object):
      """ assumes all code needed to connect db and commit data transaction """
      def __init__(self, data):
          import database
          self._dbcon = database.get_connection()
          self.data = data
      def save(self):
          self._dbcon.commit(this.data.persist())
  
  class DataObjectTypeOne(object):
      """ assumes all serializable function to format the data output """
      @staticmethod
      def persist():
          return self.get_save_format()

  try:
      db = persistence(factorize(module=Example, object_type=DataObjectTypeOne))
  except(ArgumentError, NonExistentTypeError, NonExistentModuleError) as e:
      print("factory error {}".format(e))
      raise
  
  db.save()


