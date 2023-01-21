class Choices:
    def __init__(self, *values):
        for v in values:
            setattr(self, v, v)

    def __getattr__(self, item):
        return getattr(self._choices, item)

    def __str__(self):
        return
