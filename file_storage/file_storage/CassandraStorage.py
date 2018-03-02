"""
implementation of the Storage interfaces with Cassandra DB
"""
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table, create_keyspace_simple


class ObjectKeyValue(Model):
    key = columns.UUID(primary_key=True)
    value = columns.Blob()


class ContextKeyValue(Model):
    key = columns.UUID(primary_key=True)
    value = columns.Text()


class ObjectStoreCassandra:

    def __init__(self, key_space, cluster_nodes):
        connection.setup(cluster_nodes, key_space)
        create_keyspace_simple(key_space, 1)
        sync_table(ObjectKeyValue)

    def save(self, key, value):
        ObjectKeyValue.create(key=key, value=value)

    def load(self, key):
        return ObjectKeyValue.get(key=key).value

    def delete(self, key):
        ObjectKeyValue(key=key).delete()


class ContextStoreCassandra:

    def __init__(self, key_space, cluster_nodes):
        connection.setup(cluster_nodes, key_space)
        create_keyspace_simple(key_space, 1)
        sync_table(ContextKeyValue)

    def save(self, key, value):
        ContextKeyValue.create(key=key, value=value)

    def load(self, key):
        return ContextKeyValue.get(key=key).value

    def delete(self, key):
        ContextKeyValue(key=key).delete()

    def list(self):
        return [x.value for x in ContextKeyValue.objects().all()]
