"""
implementation of the Storage interfaces with Cassandra DB
"""
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table


class KeyValue(Model):
    key = columns.UUID(primary_key=True)
    value = columns.Blob()


class ObjectStoreCassandra:

    KEY_SPACE = 'minifilebox_objects'

    def __init__(self, cluster_nodes):
        connection.setup(cluster_nodes, key_space)
        sync_table(self.KeyValue)

    def save(self, key, value):
        KeyValue.create(key=key, value=value)

    def load(self, key):
        return KeyValue.get(key=key).value

    def delete(self, key):
        KeyValue.delete(key=key)


class ContextStoreCassandra:

    KEY_SPACE = 'minifilebox_context'

    def __init__(self, cluster_nodes):
        connection.setup(cluster_nodes, self.KEY_SPACE)
        sync_table(self.KeyValue)

    def save(self, key, value):
        KeyValue.create(key=key, value=value)

    def load(self, key):
        return KeyValue.get(key=key).value

    def delete(self, key):
        KeyValue.delete(key=key)

    def list(self):
        return [ o.value for o in KeyValue.objects()]
