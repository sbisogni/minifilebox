#!/usr/bin/env python

from flask import Flask, jsonify, request, abort
from file_storage import FileStorage

app = Flask(__name__)


@app.route(base_uri + '/files/upload', methods=['POST'])
def upload_file():
    """
    Upload the content from the request body in given path inside the user box
    """
    if 'file' not in request.files:
        abort(400, 'Missing parameter: file')

    file = request.files['file']



    done = False

    while not done:
        chunk = file.stream.read(CHUNK_SIZE)
        if len(chunk) != 0:
            FILE_STORAGE[chunk_key] = chunk
            chunk_key = chunk_key + 1
        else:
            done = True

    print(FILE_STORAGE)

    return "200"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'No found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
    app.file_storage = FileStorage.create_test_file_storage()
