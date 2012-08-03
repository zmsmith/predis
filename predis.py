import inspect

from redis import StrictRedis


class PredisMeta(type):

    @staticmethod
    def fucking_awesome_factory(name):
        def f(self, *_args, **_kwargs):
            # get underlying method from StrictRedis
            orig = getattr(StrictRedis, name)

            # `parsed_args` is a dictionary of (parameter name, value) pairs of
            # of how `orig` would interpret `*args` and `**kwargs`.
            parsed_args = inspect.getcallargs(orig, self, *_args, **_kwargs)

            # Loop through the parsed arguments and transform the arguments we
            # know represent redis keys
            for key, value in parsed_args.iteritems():
                trans = getattr(self, "_{}__transform__{}".format(self.__class__.__name__, key), None)
                if trans:
                    parsed_args[key] = trans(value)
            # get the argument names so we can reconstruct out parameters
            args_spec, varargs_spec, keywords = inspect.getargs(orig.func_code)
            # put requried positional arguments in the correct positions
            args = [parsed_args.get(a) for a in args_spec]
            # extend with varargs variable so it can be passed in with * syntnax
            args.extend(parsed_args.get(varargs_spec, []))
            # get the dictionary to be passed in with **syntax
            kwargs = parsed_args.get(keywords, {})
            # call the motherfucker
            return orig(*args, **kwargs)
        f.__name__ = name
        return f

    commands_to_overwrite = (
        "append",
        "getrange",
        "decr",
        "exists",
        "expire",
        "expireat",
        "get",
        "getbit",
        "getset",
        "incr",
        "keys",
        "mget",
        "mset",
        "msetnx",
        "move",
        "persist",
        "randomkey",
        "rename",
        "renamenx",
        "set",
        "setbit",
        "setex",
        "setnx",
        "setrange",
        "strlen",
        "substr",
        "ttl",
        "type",
        "watch",
        "unwatch",
        "blpop",
        "brpop",
        "brpoplpush",
        "lindex",
        "linsert",
        "llen",
        "lpop",
        "lpush",
        "lpushx",
        "lrange",
        "lrem",
        "lset",
        "ltrim",
        "rpop",
        "rpoplpush",
        "rpush",
        "rpushx",
        "sort",
        "sadd",
        "scard",
        "sdiff",
        "sdiffstore",
        "sinter",
        "sinterstore",
        "sismember",
        "smembers",
        "smove",
        "spop",
        "srandmember",
        "srem",
        "sunion",
        "sunionstore",
        "zadd",
        "zcard",
        "zcount",
        "zincrby",
        "zinterstore",
        "zrange",
        "zrangebyscore",
        "zrank",
        "zrem",
        "zremrangebyrank",
        "zremrangebyscore",
        "zrevrange",
        "zrevrangebyscore",
        "zrevrank",
        "zscore",
        "zunionstore",
        "_zaggregate",
        "hdel",
        "hexists",
        "hget",
        "hgetall",
        "hincrby",
        "hkeys",
        "hlen",
        "hset",
        "hsetnx",
        "hmset",
        "hmget",
        "hvals"
    )

    def __new__(cls, _name, bases, attrs):
        for name in cls.commands_to_overwrite:
            attrs[name] = cls.fucking_awesome_factory(name)

        return super(PredisMeta, cls).__new__(cls, _name, bases, attrs)


class Predis(StrictRedis):

    __metaclass__ = PredisMeta

    def __init__(self, prefix, *args, **kwargs):
        self.prefix = prefix
        super(Predis, self).__init__(*args, **kwargs)

    def __add_prefix(self, value):
        if self.prefix:
            value = "{0}:{1}".format(self.prefix, value)
        return value

    def __transform__name(self, value):
        return self.__add_prefix(value)

    def __transform__keys(self, keys):
        return [self.__add_prefix(key) for key in keys]

    def __transform__args(self, keys):
        return [self.__add_prefix(key) for key in keys]

    def __transform__dest(self, value):
        return self.__add_prefix(value)

    def __transform__src(self, value):
        return self.__add_prefix(value)
