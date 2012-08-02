Predis: Automatic Key Prefixing Redis Client
============================================

Usage

::
    >>> from predis import Predis
    >>> conn = Predis(prefix="foo")
    >>> conn.set("bar", "baz")
    True
    >>> from redis import StrictRedis
    >>> conn = StrictRedis()
    >>> conn.get("bar")
    >>> conn.get("foo:bar", "baz")
    "baz"

