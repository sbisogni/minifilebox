"""
Different implementation of the ContextStore to be used in different execution environment
"""


class ObjectStoreInMemory:

    def __init__(self):
        self._memory_db = {}
        self._unique_id = 0

    def save(self, obj):
        id = self._generate_unique_id()
        self._memory_db[id] = obj
        return id

    def load(self, obj_id):
        return self._memory_db[obj_id]

    def delete(self, obj_id):
        obj = self.load(obj_id)
        self._memory_db.pop(obj_id)
        return obj

    # PRIVATE IMPLEMENTATION
    def _generate_unique_id(self):
        self._unique_id += 1
        return self._unique_id

