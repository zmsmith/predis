from redis import StrictRedis
from predis import Predis


class TestPredis(object):

    def setUp(self):
        self.redis = StrictRedis(db=9)
        self.predis = Predis(prefix="test", db=9)

    def tearDown(self):
        self.redis.flushdb()

    def test_set(self):
        self.predis.set("foo", "bar")
        assert self.redis.get("test:foo") == "bar"

    def test_get(self):
        self.redis.set("test:foo", "bar")
        assert self.predis.get("foo") == "bar"

    def test_sunionstore(self):
        self.redis.sadd("test:foo", "bar")
        self.redis.sadd("test:boo", "bat")
        self.redis.sadd("test:goo", "bak")
        self.predis.sunionstore("blah", ["foo", "boo"], "goo")
        assert self.redis.smembers("test:blah") == set(["bar", "bat", "bak"])
