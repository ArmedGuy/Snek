SUPPORTED_PROCESSORS = ["postgres"]
import sys, inspect
import psycopg2
from .processors import *
from .models import *
import builtins

class Snek():
    def __init__(self, processor, host="localhost", port=None, user="root", password="", database="snek"):
        self._models = {}
        builtins._snek_instance = self
        self._processor = None
        if processor not in SUPPORTED_PROCESSORS:
            raise Exception()
        if processor == "postgres":
            dbstring = "host='%s' dbname='%s' user='%s' password='%s'" % (host, database, user, password)
            conn = psycopg2.connect(dbstring)
            self._processor = PostgresProcessor(conn)
        else:
            raise Exception()

    def create_all(self):
        for name, obj in inspect.getmembers(sys.modules["__main__"]):
            if inspect.isclass(obj) and issubclass(obj, Model) and Model != obj:
                m = obj.__name__
                cols = []
                for name, col in obj.__dict__.items():
                    if not isinstance(col, Col): continue
                    col.name = name
                    cols.append(col)
                self._processor.CreateTable(m, cols)
    def drop_all(self):
        for name, obj in inspect.getmembers(sys.modules["__main__"]):
            if inspect.isclass(obj) and issubclass(obj, Model) and Model != obj:
                m = obj.__name__
                self._processor.DropTable(m)

    def registerModel(self, cls):
        self._models[cls.__name__] = cls

