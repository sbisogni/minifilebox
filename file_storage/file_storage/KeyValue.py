"""
Model a KeyValue object to be stored inside the ObjectStore
"""
import json
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

    def to_json(self):
        data = dict()

        if self.key:
            data['key'] = self.key

        if self.value:
            data['value'] = base64.encodebytes(self.value).decode()

        return json.dumps(data, sort_keys=True)

    def from_json(self, s):
        data = json.loads(s)
        if 'key' in data:
            self.key = data['key']
        if 'value' in data:
            self.value = base64.decodebytes(data['value'].encode())

        return self

    def __eq__(self, other):
        return self.to_json() == other.to_json()