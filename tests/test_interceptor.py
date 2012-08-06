from predis.interceptor import interceptor


def simple(a, b, c=None):
    r = a + b
    if c:
        r += c
    return r


class BaseAllArgsTestCase(object):

    def test_assignment(self):
        assert self.intercepted['a'] == 1
        assert self.intercepted['b'] == 2
        assert self.intercepted['c'] == 3

    def test_unaltered_call(self):
        assert self.intercepted() == 6

    def test_altered_call(self):
        self.intercepted['c'] = 4
        assert self.intercepted() == 7


class BaseMissingArgsTestCase(object):

    def test_assignment(self):
        assert self.intercepted['a'] == 1
        assert self.intercepted['b'] == 2
        assert self.intercepted['c'] is None

    def test_unaltered_call(self):
        assert self.intercepted() == 3

    def test_altered_call(self):
        self.intercepted['c'] = 4
        assert self.intercepted() == 7


class TestPositionalCallAllArgs(BaseAllArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, 1, 2, 3)


class TestPositionalMissingArgs(BaseMissingArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, 1, 2)


class TestNamedCallAllArgs(BaseAllArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, a=1, b=2, c=3)


class TestNamedMissingArgs(BaseMissingArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, a=1, b=2)


class TesVarargsCallAllArgs(BaseAllArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, *[1, 2, 3])


class TestVarargsMissingArgs(BaseMissingArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, *[1, 2])


class TestKeywordsCallAllArgs(BaseAllArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, **{'a': 1, 'b': 2, 'c': 3})


class TestKeywordsMissingArgs(BaseMissingArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, **{'a': 1, 'b': 2})


class TestWeirdCallAllArgs(BaseAllArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, 1, c=3, *[2])


class TestWeirdMissingArgs(BaseMissingArgsTestCase):

    def setup(self):
        self.intercepted = interceptor(simple, *[1], **{'b': 2})
