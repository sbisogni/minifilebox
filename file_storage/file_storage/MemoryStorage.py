"""
In-memory implementation of Storage interfaces. Refer to StorageInterface for documentation
This classes are aimed for testing
"""
from file_storage.StorageInterface import ObjectStoreInterface, ContextStoreInterface
from file_storage.KeyValue import KeyValue
from file_storage.Minifile import Minifile


class ObjectStoreInMemory(ObjectStoreInterface):

    def __init__(self):
        self._memory_db = {}

    def save(self, obj):
        self._memory_db[obj.key] = obj.value

    def load(self, key):
        return KeyValue(key, self._memory_db[key])

    def delete(self, key):
        self._memory_db.pop(key)


class ContextStoreInMemory(ContextStoreInterface):

    def __init__(self):
        self._memory_db = {}

    def save(self, mini_file):
        self._memory_db[mini_file.file_id] = mini_file.to_json()

    def load(self, file_id):
        return Minifile().from_json(self._memory_db[file_id])

    def delete(self, file_id):
        self._memory_db.pop(file_id)

    def list(self):
        return [Minifile().from_json(obj) for obj in self._memory_db.values()]
