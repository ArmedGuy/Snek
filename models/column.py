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
