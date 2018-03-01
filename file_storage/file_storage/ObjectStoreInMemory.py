"""
In-Memory implementation of the ObjectStore. Aimed for testing
"""
import logging


class ObjectStoreInMemory:

    def __init__(self):
        self._memory_db = {}
        self._unique_id = 0

    def save(self, obj):
        id = self._generate_unique_id()
        logging.info("storing object with id = %s" % id)
        self._memory_db[id] = obj
        return id

    def load(self, obj_id):
        logging.info("loading object with id = %s" % obj_id)
        return self._memory_db[obj_id]

    def delete(self, obj_id):
        logging.info("deleting object with id = %s" % obj_id)
        obj = self.load(obj_id)
        self._memory_db.pop(obj_id)
        return obj

    # PRIVATE IMPLEMENTATION
    def _generate_unique_id(self):
        self._unique_id += 1
        return self._unique_id

