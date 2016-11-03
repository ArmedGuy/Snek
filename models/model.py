import builtins
from .column import Col
def proc():
    return builtins._snek_instance._processor

class Model(object):
    def __init__(self, values):
        for name, col in self.__class__.__dict__.items():
            if not isinstance(col, Col): continue
            if name in values:
                self.__dict__[name] = values[name] #col.read(values[name])

    def __str__(self):
        return "<Model %s>: %s" % (self.__class__.__name__, self.__dict__)
    @classmethod
    def get(cls, *args, **kwargs):
        filters = []
        for arg in args:
            filters.append(args)
        for key, value in kwargs.items():
            filters.append((key, "=", value))
        results = proc().Select(cls.__name__, '*', filters=filters)
        if(len(results)) != 1:
            raise Exception()
        else:
            return cls(results[0])

    @classmethod
    def find(cls, *args, **kwargs):
        filters = []
        for arg in args:
            filters.append(args)
        for key, value in kwargs.items():
            filters.append((key, "=", value))
        results = proc().Select(cls.__name__, '*', filters=filters)
        return [cls(res) for res in results]
