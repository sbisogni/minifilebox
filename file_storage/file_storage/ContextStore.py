"""
Different implementation of the ContextStore to be used in different execution environment
"""


class ContextStoreMemory:
    """
    In-memory implementation of ContextStore. Aimed for testing
    """

    def __init__(self):
        self._memory_db = {}
        self._unique_id = 0

    def save(self, miniboxfile):
        id = self._generate_unique_id()
        miniboxfile.set_file_id(id)
        self._memory_db[id] = miniboxfile
        return id

    def load(self, file_id):
        return self._memory_db[file_id]

    def delete(self, file_id):
        miniboxfile = self.load(file_id)
        self._memory_db.pop(file_id)
        return miniboxfile

    def list(self):
        return list(self._memory_db.values())

    # PRIVATE IMPLEMENTATION
    def _generate_unique_id(self):
        self._unique_id += 1
        return self._unique_id


