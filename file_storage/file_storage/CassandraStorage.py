"""
implementation of the Storage interfaces with Cassandra DB
"""
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.management import sync_table, create_keyspace_simple
from file_storage.KeyValue import KeyValue
from file_storage.Minifile import Minifile
import json


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

    def save(self, obj):
        ObjectKeyValue.create(key=obj.key, value=obj.value)

    def load(self, key):
        return KeyValue(key, ObjectKeyValue.get(key=key).value)

    def delete(self, key):
        ObjectKeyValue(key=key).delete()


class ContextStoreCassandra:

    def __init__(self, key_space, cluster_nodes):
        connection.setup(cluster_nodes, key_space)
        create_keyspace_simple(key_space, 1)
        sync_table(ContextKeyValue)

    def save(self, mini_file:Minifile):
        ContextKeyValue.create(kmini_file.file_id, json.dumps(mini_file.to_dict(), sort_keys=True))

    def load(self, file_id):
        return Minifile().from_dict(json.loads(ContextKeyValue.get(file_id).value))

    def delete(self, file_id):
        ContextKeyValue(key=file_id).delete()

    def list(self):
        return [Minifile().from_dict(json.loads(obj.value)) for obj in ContextKeyValue.objects().all()]
