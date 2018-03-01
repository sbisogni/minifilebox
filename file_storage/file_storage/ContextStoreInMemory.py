"""
In-memory implementation of ContextStore. Aimed for testing
"""


class ContextStoreMemory:

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


