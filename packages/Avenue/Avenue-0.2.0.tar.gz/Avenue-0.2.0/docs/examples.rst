.. _examples:

Examples
========

Processors & Arguments
----------------------

Avenue is build to be very extensible, not only path routing can be
achieved using Avenue. But, because routing is mostly used in
web-application, we have some processors specific for this end.

The quick start example, with the default processors:

.. code-block:: python

    from avenue import Avenue
    from avenue import MethodProcessor
    from avenue import PathProcessor

    router = Avenue([
        PathProcessor('path'),
        MethodProcessor('method', optional=True),
    ])

    @router.attach(path='/', method='GET')
    def hello_world():
        return 'Hallo world!'

    route = {'path': '/', 'method': 'GET}
    assert router.solve(**route) == 'Hallo world!'

This matches the *quick start* example, but we defined the processors
explicitly. When the `solve` method is ran, the names of the processors
are used to match the arguments against.

MethodProcessor is marked as `optional`, this means you can attach
a route without an `method='...'` parameter. It allows you to create
more generic patterns, where some routes match the path and *any* method.

You can pass any argument into the `solve` method, as long as the
processor-names are there. Omitting the *path*, for example, will simply
use the `None` value for path.


Custom processor
----------------

You can define your own processors, this allows you to match on domain,
role, user rights, cookies, post values, anything you can think of! Normally
we would write a decorate for this and wrap our route in it. The processor
pattern allows your code to be much cleaner and easier to maintain.

A custom RoleProcessor:

.. code-block:: python

    from avenue import Avenue
    from avenue import MethodProcessor
    from avenue import PathProcessor
    from avenue import Processor

    class RoleProcessor(Processor):
        def __call__(self, value, route):
            # prepare takes care of the `optional` part automaticly
            argument, value = self.prepare(value, route)

            # argument is the parameter with which the route was defined
            # value is the parameter which `solve` was called with

            if not argument:
                # processor is optional
                return 0
            elif value in argument:
                # value is one of the allowed roles
                return 1
            else:
                # you could also raise some other error and return
                # a 403 to your users, this simply marks the route
                # as not runnable if the role does not match
                error = 'Role does not match, `{:s}` not in `{:s}`'.format(
                    value, ', '.join(argument))
                raise MatchError(error)

    # create a router with the RoleProcessor
    router = Avenue([
        PathProcessor('path'),
        MethodProcessor('method', optional=True),
        RoleProcessor('role', optional=True),
    ])

    # define a route and use the role parameter
    @router.attach(path='/', method='GET', role=['user', 'administrator'])
    def hello_world():
        return 'Hallo world!'

    # solve with a role
    route = {'path': '/', 'method': 'GET', 'role': 'user'}
    assert router.solve(**route) == 'Hallo world!'

    # solve without a role
    route = {'path': '/', 'method': 'GET'}
    try:
        router.solve(**route)
    except NotFound:
        # no role, so it can't match `hello_world`
        pass
