#!/usr/bin/env python

from flask import Flask, request, jsonify
from file_storage.MemoryStorage import ObjectStoreInMemory, KeyValue
from file_storage.CassandraStorage import ObjectStoreCassandra
import config


app = Flask(__name__)

object_store_factory = {
    'memory': lambda: ObjectStoreInMemory(),
    'cassandra': lambda: ObjectStoreCassandra(config.MINIFILEBOX_OBJ_STORE_CASSANDRA_KEYSPACE,
                                              config.MINIFILEBOX_OBJ_STORE_CASSANDRA_NODES)
}

object_store = object_store_factory[config.MINIFILEBOX_STORAGE_TYPE]()


@app.route(config.MINIFILEBOX_BASE_URI + '/objects', methods=['POST'])
def store_object():
    obj= KeyValue().from_dict(request.json)
    object_store.save(obj)
    return jsonify(status='OK')


@app.route(config.MINIFILEBOX_BASE_URI + '/objects/<string:obj_id>', methods=['GET'])
def load_object(obj_id):
    return jsonify(object_store.load(obj_id).to_dict())


@app.route(config.MINIFILEBOX_BASE_URI + '/objects/<string:obj_id>', methods=['DELETE'])
def delete_object(obj_id):
    object_store.delete(obj_id)
    return jsonify(status='OK')


if __name__ == '__main__':
    # Overriding default HTML exception handler
    # for ex in default_exceptions:
    #     app.register_error_handler(ex, handle_error)
    app.run(host='0.0.0.0', port=5001)