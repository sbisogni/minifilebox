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
    TODO
    :return:
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

    :param file_id:
    :return:
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

    :param file_id:
    :return:
    """
    try:
        minifile = FILE_STORAGE.delete(file_id)
        return jsonify(minifile.to_dict()), 200
    except KeyError as e:
        raise NotFound(str(e))


@app.route(config.DEFAULT_BASE_URI + '/files', methods=['GET'])
def list_files():
    """

    :return:
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
    app.run(debug=True)
