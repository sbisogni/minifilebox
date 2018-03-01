"""
implementation of the Storage interfaces with Cassandra DB
"""


class ObjectStoreCassandra:

    def __init__(self):

    def save(self, obj):
        pass

    def load(self, obj_id):
        pass

    def delete(self, obj_id):
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
