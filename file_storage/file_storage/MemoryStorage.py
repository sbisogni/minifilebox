"""
In-memory implementation of Storage interfaces
"""


class ObjectStoreInMemory:
    """
    In-Memory implementation of the ObjectStore. Aimed for testing
    """

    def __init__(self):
        self._memory_db = {}
        self._unique_id = 0

    def save(self, key, obj):
        self._memory_db[key] = obj

    def load(self, key):
        return self._memory_db[key]

    def delete(self, key):
        obj = self.load(key)
        self._memory_db.pop(key)
        return obj

    def list(self):
        return list(self._memory_db.values())
