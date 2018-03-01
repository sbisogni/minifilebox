"""
implementation of the Storage interfaces with Cassandra DB
"""

class ObjectStoreCassandra:

    def __init__(self):

    def save(self, key, value):
        pass

    def load(self, key):
        pass

    def delete(self, key):
        pass


class ContextStoreCassandra:

    def save(self, minifile):
        pass

    def load(self, file_id):
        pass

    def delete(self, file_id):
        pass

    def list(self):
        pass
