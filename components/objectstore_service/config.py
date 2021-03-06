import os

# CONFIGURATION VARIABLE
MINIFILEBOX_BASE_URI = '/minifilebox/api/v1'
MINIFILEBOX_STORAGE_TYPE = 'cassandra'
# CASSANDRA
MINIFILEBOX_OBJ_STORE_CASSANDRA_NODES = os.getenv('MINIFILEBOX_CASSANDRA_NODES', '127.0.0.1').split(',')
MINIFILEBOX_OBJ_STORE_CASSANDRA_KEYSPACE = 'object_store'
