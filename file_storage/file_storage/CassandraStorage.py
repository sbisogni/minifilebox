"""
implementation of the Storage interfaces with Cassandra DB
"""
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table, create_keyspace_simple


class KeyValue(Model):
    key = columns.UUID(primary_key=True)
    value = columns.Blob()


class ObjectStoreCassandra:

    KEY_SPACE = 'minifilebox_objects'

    def __init__(self, cluster_nodes):
        connection.setup(cluster_nodes, self.KEY_SPACE)
        create_keyspace_simple(self.KEY_SPACE, 1)
        sync_table(KeyValue)

    def save(self, key, value):
        KeyValue.create(key=key, value=value)

    def load(self, key):
        return KeyValue.get(key=key).value

    def delete(self, key):
        KeyValue(key=key).delete()


class ContextStoreCassandra:

    KEY_SPACE = 'minifilebox_context'

    def __init__(self, cluster_nodes):
        connection.setup(cluster_nodes, self.KEY_SPACE)
        create_keyspace_simple(self.KEY_SPACE, 1)
        sync_table(KeyValue)

    def save(self, key, value):
        KeyValue.create(key=key, value=value)

    def load(self, key):
        return KeyValue.get(key=key).value

    def delete(self, key):
        KeyValue(key=key).delete()

    def list(self):
        return [o.value for o in KeyValue.objects()]
