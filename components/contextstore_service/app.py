#!/usr/bin/env python

from flask import Flask, request, jsonify
from file_storage.MemoryStorage import ContextStoreInMemory, Minifile
from file_storage.CassandraStorage import ContextStoreCassandra
import config

app = Flask(__name__)


context_store_factory = {
    'memory': lambda: ContextStoreInMemory(),
    'cassandra': lambda: ContextStoreCassandra(config.MINIFILEBOX_CTX_STORE_CASSANDRA_KEYSPACE,
                                               config.MINIFILEBOX_CTX_STORE_CASSANDRA_NODES)
}

context_store = context_store_factory[config.MINIFILEBOX_STORAGE_TYPE]()


@app.route(config.MINIFILEBOX_BASE_URI + '/context', methods=['POST'])
def store_context():
    file = Minifile().from_dict(request.json)
    context_store.save(file)
    return jsonify(status='OK')


@app.route(config.MINIFILEBOX_BASE_URI + '/context/<string:file_id>', methods=['GET'])
def load_context(file_id):
    return jsonify(context_store.load(file_id).to_dict())


@app.route(config.MINIFILEBOX_BASE_URI + '/context/<string:file_id>', methods=['DELETE'])
def delete_context(file_id):
    context_store.delete(file_id)
    return jsonify(status='OK')


@app.route(config.MINIFILEBOX_BASE_URI + '/context', methods=['GET'])
def list_context():
    return jsonify([c.to_dict() for c in context_store.list()])


if __name__ == '__main__':
    # Overriding default HTML exception handler
    # for ex in default_exceptions:
    #     app.register_error_handler(ex, handle_error)
    app.run(host='0.0.0.0', port=5002)