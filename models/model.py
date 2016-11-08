import builtins
from .column import Col
def proc():
    return builtins._snek_instance._processor


class Model():
    def __init__(self, **values):
        if '__exists' in values:
            self._exists = True
            del values['__exists']
        else:
            self._exists = False
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
                if self._exists:
                    self._commited[name] = values[name] #col.read(values[name])
                else:
                    self._dirty[name] = values[name]


    # internal function overrides
    def __str__(self):
        return "<Model %s>: %s" % (self.__class__.__name__, self.__dict__)

    def __getattribute__(self, name):
        if name.startswith("_"):
            return object.__getattribute__(self, name)
        cls = self.__class__
        clsdir = dir(cls)
        if name in clsdir and (callable(getattr(cls,name)) or isinstance(getattr(cls,name), property)):
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
    # properties
    def _get_dirty(self):
        return len(self._dirty.keys()) != 0
    dirty = property(_get_dirty)

    def _get_primary(self):
        primary = [(key, c) for key,c in self._columns.items() if c.args.get('primary')][0]
        primary[1].name = primary[0]
        return primary[1]
    primary_key = property(_get_primary)

    def _get_table_name(self):
        return self.__class__.__name__
    table_name = property(_get_table_name)

    # save
    def save(self):
        if not self.dirty:
            return
        if self._exists: # remote object exists, update
            primary = self.primary_key
            primary_value = getattr(self, primary.name)
            proc().Update(self.table_name, self._dirty, [(primary.name, '=', primary_value)])
            for k,v in self._dirty.items():
                self._commited[k] = v
            self._dirty = {}
        else: # no remote object, insert
            pk = self.primary_key
            primary = proc().Insert(self.table_name, self._dirty, pk.name)
            setattr(self, pk.name, primary)
            self._exists = True
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
            values = results[0]
            values['__exists'] = True
            return cls(**values)

    @classmethod
    def find(cls, *args, **kwargs):
        filters = []
        for arg in args:
            filters.append(args)
        for key, value in kwargs.items():
            filters.append((key, "=", value))
        results = proc().Select(cls.__name__, '*', filters=filters)
        found = []
        for res in results:
            res['__exists'] = True
            found.append(cls(**res))
        return found
