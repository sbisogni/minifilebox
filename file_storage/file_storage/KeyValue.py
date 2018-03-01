"""
Model a KeyValue object to be stored inside the ObjectStore
"""


class KeyValue:
    """
    Model a KeyValue object to be stored inside the ObjectStore
    """

    def __init__(self, key, value):
        if not key:
            raise ValueError('invalid key')

        if not value:
            raise ValueError('invalid value')

        self.key = key
        self.value = value

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def to_dict(self):
        return {'key': self.key, 'value': self.value}
