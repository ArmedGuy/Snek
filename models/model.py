import builtins
from .column import Col
def proc():
    return builtins._snek_instance._processor


class Model():
    def __init__(self, values):
        self._reserved = ["get", "find"]
        self._columns = {}
        self._commited = {}
        self._dirty = {}
        self._columns = {}
        for name, col in self.__class__.__dict__.items():
            if not isinstance(col, Col): continue
            col.name = name
            self._columns[name] = col
            if name in values:
                self._commited[name] = values[name] #col.read(values[name])

    def pk(self):
        primary = [(key, c) for key,c in self._columns.items() if c.args.get('primary')][0]
        primary[1].name = primary[0]
        return primary[1]

    def __str__(self):
        return "<Model %s>: %s" % (self.__class__.__name__, self.__dict__)

    def __getattribute__(self, name):
        if name.startswith("_"):
            return object.__getattribute__(self, name)
        elif name in dir(self.__class__) and callable(getattr(self.__class__,name)):
            return object.__getattribute__(self, name)

        elif name in self._reserved:
            return object.__getattribute__(self, name)
        else:
            raise AttributeError()

    def __getattr__(self, key):
        if not key.startswith("_") and key in self._columns.keys():
            if key in self._dirty.keys():
                return self._dirty[key]
            else:
                return self._commited[key]
        else:
            return self.__dict__[key]

    def __setattr__(self, key, value):
        if not key.startswith("_") and key in self._columns.keys():
            self._dirty[key] = value
        else:
            self.__dict__[key] = value

    def dirty(self):
        return len(self._dirty.keys()) != 0

    def save(self):
        if not self.dirty():
            return
        primary = self.pk()
        primary_value = getattr(self, primary.name)
        proc().Update(self.__class__.__name__, self._dirty, [(primary.name, '=', primary_value)])
        for k,v in self._dirty.items():
            self._commited[k] = v
        self._dirty = {}
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
