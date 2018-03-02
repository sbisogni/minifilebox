"""
Model a KeyValue object to be stored inside the ObjectStore
"""
import json
import uuid


class KeyValue:

    def __init__(self, key=None, value=None):
        """
        Generate a new Key Value pair
        :param key: object uuid
        :param value: value to store
        """
        self.key = key
        self.value = value

    def to_json(self):
        data = dict()

        if self.key:
            data['key'] = self.key.hex

        if self.value:
            data['value'] = self.value

        return json.dumps(data, sort_keys=True)

    def from_json(self, s):
        data = json.loads(s)
        if 'key' in data:
            self.key = uuid.UUID(data['key'])
        if 'value' in data:
            self.value = data['value']

        return self

    def __eq__(self, other):
        return self.to_json() == other.to_json()