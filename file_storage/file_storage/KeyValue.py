"""
Model a KeyValue object to be stored inside the ObjectStore
"""
import base64


class KeyValue:

    def __init__(self, key=None, value=None):
        """
        Generate a new Key Value pair
        :param key: object key
        :param value: value to store
        """
        self.key = key
        self.value = value

    def to_dict(self):
        """
        Converts the KeyValue into an Dict
        :return: Dict
        """
        data = dict()

        if self.key:
            data['key'] = self.key

        if self.value:
            data['value'] = base64.encodebytes(self.value).decode()

        return data

    def from_dict(self, data):
        """
        Initialize the KeyValue with given data Dict
        :param data: Initialization dictionary
        :return: self
        """
        if 'key' in data:
            self.key = data['key']
        if 'value' in data:
            self.value = base64.decodebytes(data['value'].encode())

        return self

    def __eq__(self, other):
        return (self.key == other.key) and \
               (self.value == other.value)

    def __str__(self):
        return str(self.to_dict())
