#!/usr/bin/env python

from flask import Flask, request, jsonify, send_file
from file_storage import FileStorage, Minifile
from werkzeug.exceptions import BadRequest, NotFound, HTTPException, default_exceptions
import config


app = Flask(__name__)
FILE_STORAGE = FileStorage.create_test_file_storage()


@app.route(config.DEFAULT_BASE_URI + '/files/upload', methods=['POST'])
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

    chunk_size = config.DEFAULT_CHUNK_SIZE

    minifile = Minifile.Minifile(file.filename, chunk_size)
    minifile.set_file_stream(file.stream)
    FILE_STORAGE.save(minifile)

    return jsonify(minifile.to_dict()), 200


@app.route(config.DEFAULT_BASE_URI + '/files/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    """
    Download the file with given id
        curl -X GET http://<host:port>/minifilebox/api/v1/files/download/<file_id> \
            -H 'cache-control: no-cache'

    :param file_id:
    :return: The file in mimetype='application/octet-stream'
    """
    try:
        minifile = FILE_STORAGE.load(file_id)
        return send_file(minifile.get_file_stream(),
                         attachment_filename=minifile.get_file_name(),
                         as_attachment=True,
                         mimetype='application/octet-stream'), 200
    except KeyError as e:
        raise NotFound(str(e))


@app.route(config.DEFAULT_BASE_URI + '/files/delete/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """
    Delete the file with given id
        curl -X DELETE http://<host:port>/minifilebox/api/v1/files/delete/<file_id> \
            -H 'cache-control: no-cache' \

    :param file_id: The file unique id
    :return: The file metadata of deleted file
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
    try:
        minifile = FILE_STORAGE.delete(file_id)
        return jsonify(minifile.to_dict()), 200
    except KeyError as e:
        raise NotFound(str(e))


@app.route(config.DEFAULT_BASE_URI + '/files', methods=['GET'])
def list_files():
    """
    List all the files inside the Minifilebox
        curl -X GET http://<host:port>/minifilebox/api/v1/files
            -H 'cache-control: no-cache' 

    :return: The list of files metadata
        [
            {
                "chunk_size": 50000000,
                "chunks": [
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
                "file_id": 3,
                "file_name": "ideaIC-2017.3.4-no-jdk.tar.gz"
            }
        ]
    """
    minifile_list = FILE_STORAGE.list()
    return jsonify([m.to_dict() for m in minifile_list]), 200


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


if __name__ == '__main__':
    # Overriding default HTML exception handler
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_error)
    app.run(host='0.0.0.0')
