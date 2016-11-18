class GeneralProcessor(object):
    def __init__(self):
        pass

    def Select(self, table, columns, filters=[], relations=[]):
        pass
    def Insert(self, table, values):
        pass
    def Update(self, table, values, filters=[], relations=[]):
        pass
    def Delete(self, table, filters, relations=[]):
        pass

    def CreateTable(self, table, values):
        pass
    def DropTable(self, table):
        pass
