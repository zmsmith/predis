from predis.interceptor import interceptor

def foo(a,b,c):
    return (a,b,c)

def test_simple_and_shitty():
    intercepted = interceptor(foo, 1, 2, 3)
    assert intercepted['a'] == 1
    assert intercepted['b'] == 2
    assert intercepted['c'] == 3

    intercepted['c'] = 4
    assert intercepted() == (1,2,4)
