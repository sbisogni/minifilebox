"""
In-memory implementation of Storage interfaces
"""

import logging


class ContextStoreMemory:
    """
    In-memory implementation of ContextStore. Aimed for testing
    """

    def __init__(self):
        self._memory_db = {}
        self._unique_id = 0

    def save(self, minifile):
        id = self._generate_unique_id()
        minifile.set_file_id(id)
        self._memory_db[id] = minifile
        return id

    def load(self, file_id):
        return self._memory_db[file_id]

    def delete(self, file_id):
        minifile = self.load(file_id)
        self._memory_db.pop(file_id)
        return minifile

    def list(self):
        return list(self._memory_db.values())

    # PRIVATE IMPLEMENTATION
    def _generate_unique_id(self):
        self._unique_id += 1
        return self._unique_id


class ObjectStoreInMemory:
    """
    In-Memory implementation of the ObjectStore. Aimed for testing
    """

    def __init__(self):
        self._memory_db = {}
        self._unique_id = 0

    def save(self, key, obj):
        logging.info("storing object with id = %s" % key)
        self._memory_db[key] = obj

    def load(self, key):
        logging.info("loading object with id = %s" % key)
        return self._memory_db[key]

    def delete(self, key):
        logging.info("deleting object with id = %s" % key)
        obj = self.load(key)
        self._memory_db.pop(key)
        return obj
