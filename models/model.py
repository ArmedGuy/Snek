import builtins
def proc():
    return builtings._snek_instance._processor
class Model(object):
    def __init__(self, object):
        pass
    @classmethod
    def get(cls, **kwargs):
        filters = []
        for key, value in kwargs.items():
            filters.append((key, "=", value))
        results = proc().Select(cls.__name__, '*', filters=filters)
        if(len(results) != 1:
            raise Exception()
        else:
            return results[0]
