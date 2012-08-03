import inspect


class Interceptor(object):
    """
    >>> def add(x, y):
    ...   return x + y
    ...
    >>> intercepted = Interceptor(func, 1, 2)
    >>> intercepted['x']
    1
    >>> intercepted['y']
    2
    >>> intercepted['y'] = 3
    >>> intercepted()
    4
    """

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self._args = args
        self._kwargs = kwargs
        self.callargs = inspect.getcallargs(self.func, *self._args, **self._kwargs)

    def params(self):
        return self.callargs.iteritems()

    def __getitem__(self, key):
        return self.callargs.get(key)

    def __setitem__(self, key, value):
        self.callargs[key] = value

    def __call__(self):
        args_spec, varargs_spec, keywords = inspect.getargs(self.func.func_code)
        args = [self.callargs[arg] for arg in args_spec]
        args.extend(self.callargs.get(varargs_spec, []))
        kwargs = self.callargs.get(keywords, {})
        return self.func(*args, **kwargs)

interceptor = Interceptor
