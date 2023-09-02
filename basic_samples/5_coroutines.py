from inspect import getgeneratorstate


def coroutine(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


def subgen():
    x = "Ready to accept message"
    message = yield x
    print("subget recived:", message)


class BlaBlaException(Exception):
    pass


@coroutine
def avarage():
    count = 0
    sum = 0
    avarage = None

    while True:
        try:
            x = yield avarage
        except StopIteration:
            print("Done")
            break
        except BlaBlaException:
            print("bla bla bla")
            break
        else:
            count = count + 1
            sum += x
            avarage = round(sum / count, 2)
    return avarage


g = avarage()
print(getgeneratorstate(g))

print(g.send(4))
print(g.send(10))
try:
    print(g.throw(StopIteration))
except StopIteration as e:
    print("Avarage", e.value)
