#!/usr/bin/env python

from flask import Flask, request, send_file, jsonify
from werkzeug.exceptions import BadRequest, NotFound, HTTPException, default_exceptions
from file_storage.FileStorage import FileStorage, Minifile
from file_storage.MemoryStorage import ObjectStoreInMemory, ContextStoreInMemory
from file_storage.CassandraStorage import ObjectStoreCassandra, ContextStoreCassandra
from file_storage.HTTPProxyStorage import ObjectStoreHTTPProxy, ContextStoreHTTPProxy
import config


app = Flask(__name__)

# FACTORY METHODS


def create_local_memory_file_storage():
    return FileStorage(ContextStoreInMemory(), ObjectStoreInMemory())


def create_local_cassandra_file_storage():
    return FileStorage(ContextStoreCassandra(key_space=config.MINIFILEBOX_CASSANDRA_CONTEXT_KEY_SPACE,
                                             cluster_nodes=config.MINIFILEBOX_CASSANDRA_CLUSTER),
                       ObjectStoreCassandra(key_space=config.MINIFILEBOX_CASSANDRA_OBJECT_KEY_SPACE,
                                            cluster_nodes=config.MINIFILEBOX_CASSANDRA_CLUSTER))


def create_remote_file_storate():
    contextstore_url = 'http://%s:%s%s/context' % (config.MINIFILEBOX_CONTEXTSTORE_HOST,
                                                    config.MINIFILEBOX_CONTEXTSTORE_PORT,
                                                    config.MINIFILEBOX_BASE_URI)
    objectstore_url = 'http://%s:%s%s/objects' % (config.MINIFILEBOX_OBJECTSTORE_HOST,
                                                   config.MINIFILEBOX_OBJECTSTORE_PORT,
                                                   config.MINIFILEBOX_BASE_URI)

    print("ContextStore URI %s" % contextstore_url)
    print("ObjectStore URI %s" % objectstore_url)

    return FileStorage(ContextStoreHTTPProxy(contextstore_url), ObjectStoreHTTPProxy(objectstore_url))


file_storage_factory = {
    'cassandra': create_local_cassandra_file_storage,
    'memory': create_local_memory_file_storage,
    'remote': create_remote_file_storate
}


file_storage = file_storage_factory[config.MINIFILEBOX_STORAGE_TYPE]()


@app.route(config.MINIFILEBOX_BASE_URI + '/files/upload', methods=['POST'])
def upload_file():
    """
    Upload a file inside the Minifilebox FileStorage.

        curl -X POST http://<host:port>/minifilebox/api/v1/files/upload \
            -H 'cache-control: no-cache' \
            -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
            -F file=@<your_file>

    :return: The file metadata
        {
            "chunk_size": <chunk_size>,
            "chunks": [
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24
            ],
            "file_id": <file_unique_id>,
            "file_name": <file_name>
        }

    """
    if 'file' not in request.files:
        raise BadRequest('missing file parameter')

    file = request.files['file']

    chunk_size = config.MINIFILEBOX_CHUNK_SIZE

    minifile = Minifile(file_stream=file.stream, file_name=file.filename, chunk_size=chunk_size)
    file_storage.save(minifile)

    return jsonify(minifile.to_dict()), 200


@app.route(config.MINIFILEBOX_BASE_URI + '/files/download/<string:file_id>', methods=['GET'])
def download_file(file_id):
    """
    Download the file with given id
        curl -X GET http://<host:port>/minifilebox/api/v1/files/download/<file_id> \
            -H 'cache-control: no-cache'

    :param file_id:
    :return: The file in mimetype='application/octet-stream'
    """
    try:
        minifile = file_storage.load(file_id)
        return send_file(minifile.file_stream,
                         attachment_filename=minifile.file_name,
                         as_attachment=True,
                         mimetype='application/octet-stream'), 200
    except KeyError as e:
        raise NotFound(str(e))


@app.route(config.MINIFILEBOX_BASE_URI + '/files/delete/<string:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """
    Delete the file with given id
        curl -X DELETE http://<host:port>/minifilebox/api/v1/files/delete/<file_id> \
            -H 'cache-control: no-cache' \

    :param file_id: The file unique id
    :return: The file metadata of deleted file
         {
            "chunk_size": <chunk_size>,
            "chunk_ids": [
                17,
                18,
                19,
                20,
                21,
                22,
                23,
                24
            ],
            "file_id": <file_unique_id>,
            "file_name": <file_name>
        }
    """
    try:
        minifile = file_storage.delete(file_id)
        return jsonify(minifile.to_dict()), 200

    except KeyError as e:
        raise NotFound(str(e))


@app.route(config.MINIFILEBOX_BASE_URI + '/files', methods=['GET'])
def list_files():
    """
    List all the files inside the Minifilebox
        curl -X GET http://<host:port>/minifilebox/api/v1/files
            -H 'cache-control: no-cache'

    :return: The list of files metadata
        [
            {
                "chunk_size": 50000000,
                "chunk_ids": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8
                ],
                "file_id": 1,
                "file_name": "ideaIC-2017.3.4-no-jdk.tar.gz"
            },
            {
                "chunk_size": 50000000,
                "chunk_ids": [
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    24
                ],
                "file_id": 3,
                "file_name": "ideaIC-2017.3.4-no-jdk.tar.gz"
            }
        ]
    """
    minifile_list = file_storage.list()
    return jsonify([m.to_dict() for m in minifile_list]), 200


# @app.errorhandler(Exception)
# def handle_error(e):
#     code = 500
#     if isinstance(e, HTTPException):
#         code = e.code
#     return jsonify(error=str(e)), code


if __name__ == '__main__':
    # Overriding default HTML exception handler
    # for ex in default_exceptions:
    #     app.register_error_handler(ex, handle_error)
    app.run(host='0.0.0.0')
