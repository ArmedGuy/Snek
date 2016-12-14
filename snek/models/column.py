class Col:
    def __init__(self, type, kwargs):
        self.args = kwargs
        self.args['type'] = type

    @staticmethod
    def Id(**kwargs):
        return Col("serial", kwargs)

    @staticmethod
    def Int(**kwargs):
        return Col("integer", kwargs)

    @staticmethod
    def Text(**kwargs):
        return Col("text", kwargs)

    @staticmethod
    def DateTime(**kwargs):
        return Col("timestamp", kwargs)

    @staticmethod
    def Float(**kwargs):
        return Col("real", kwargs)

    @staticmethod
    def ForeignKey(primary_key_class, **kwargs):
        primary_key = None
        for c in dir(primary_key_class):
            col = getattr(primary_key_class, c)
            if not isinstance(col, Col): continue
            col.name = c
            if col.args.get("primary"):
                primary_key = col
        if not primary_key:
            raise Exception()
        type = primary_key.args.get("type")
        if type == "serial":
            type = "integer"
        kwargs['null'] = True
        kwargs['_foreignKey'] = True
        kwargs['_foreignClass'] = primary_key_class
        kwargs['foreign'] = primary_key_class.__name__
        kwargs['_foreignClassPrimaryKey'] = primary_key.name
        return Col(type, kwargs)

