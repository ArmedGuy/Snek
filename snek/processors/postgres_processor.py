from .general_processor import GeneralProcessor
import psycopg2
import psycopg2.extras
class PostgresProcessor(GeneralProcessor):
    def __init__(self, conn):
        self._connection = conn

    def Select(self, table, columns, filters=[], relations=[]):
        query = ["SELECT"]
        query.append(",".join([self._escapeName(c) for c in columns]))
        query.append("FROM")
        query.append(self._escapeName(table))
        query.append(self._compileFilters(filters))
        cur = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(" ".join(query))
        return cur.fetchall()

    def Insert(self, table, values, returns):
        columns = values.keys()
        values = values.values()
        query = ["INSERT", "INTO"]
        query.append(self._escapeName(table))
        query.append("(%s)" % (",".join([self._escapeName(c) for c in columns])))
        query.append("VALUES")
        query.append("(%s)" % (",".join([self._escapeValue(v) for v in values])))
        query.append("RETURNING %s" % self._escapeName(returns))
        cur = self._connection.cursor()
        cur.execute(" ".join(query))
        self._connection.commit()
        return cur.fetchone()[0]

    def Update(self, table, values, filters=[], relations=[]):
        query = ["UPDATE"]
        query.append(self._escapeName(table))
        query.append("SET")
        query.append(",".join(["%s = %s" % (self._escapeName(k),self._escapeValue(v)) for k,v in values.items()]))
        query.append(self._compileFilters(filters))

        self._executeNoResult(" ".join(query))

    def Delete(self, table, filters, relations=[]):
        query = ["DELETE", "FROM"]
        query.append(self._escapeName(table))
        query.append(self._compileFilters(filters))

        self._executeNoResult(" ".join(query))

    def CreateTable(self, table, columns):
        query = ["CREATE", "TABLE"]
        query.append(self._escapeName(table))
        query.append("(%s)" % ",".join([self._compileColumn(c) for c in columns]))

        self._executeNoResult(" ".join(query))

    def DropTable(self, table):
        query = ["DROP", "TABLE"]
        query.append(self._escapeName(table))

        self._executeNoResult(" ".join(query))

    def _executeNoResult(self, query):
        cur = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(query)
        self._connection.commit()

    def _compileFilters(self, filters):
        if(len(filters) == 0):
            return ""
        ret = ["WHERE"]
        for f in filters:
            if isinstance(f, str):
                ret.append("(%s)" % f)
                ret.append("AND")
            else:
                ret.append("%s %s %s" % (self._escapeName(f[0]),f[1],self._escapeValue(f[2])))
                ret.append("AND")
        return " ".join(ret[0:-1])

    def _escapeName(self, name):
        if name == "*":
            return name
        ret = []
        if "." in name:
            parts = name.split('.')
            for part in parts:
                ret.append("\"%s\"" % part)
        else:
            ret.append("\"%s\"" % name)
        return ".".join(ret)

    def _escapeValue(self, value):
        if isinstance(value, str):
            return "'%s'" % value
        else:
            return str(value)

    def _compileColumn(self, col):
        ret = [self._escapeName(col.name)]
        ret.append(col.args['type'])
        if 'primary' in col.args and col.args['primary']:
            ret.append("PRIMARY KEY")
        if 'foreign' in col.args:
            ret.append("REFERENCES")
            ret.append("%s(id)" % self._escapeName(col.args['foreign']))
        if 'default' in col.args:
            ret.append("DEFAULT")
            ret.append(self._escapeValue(col.args['default']))
        if 'unique' in col.args and col.args['unique']:
            ret.append("UNIQUE")
        if 'null' in col.args and col.args['null']:
            ret.append("NULL")
        elif 'null' not in col.args or not col.args['null']:
            ret.append("NOT NULL")
        return " ".join(ret)

