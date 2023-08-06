Avenue: Highway routing.
=============================================

.. teaser-begin

``Avenue`` is an `MIT <http://choosealicense.com/licenses/mit/>`_-licensed Python package with a very extensible,
but light weight, routing system.

A quick example:

.. code-block:: python

    from avenue import Avenue
    
    router = Avenue()

    @router.attach(path='/', method='GET')
    def hello_world():
        return 'Hallo world!'
    
    route = {
      'path': '/',
      'method': 'GET,
    }

    assert router.solve(**route) == 'Hallo world!'

