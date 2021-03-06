"""
Representation of a file inside Minifilebox
"""
import json


class Minifile:

    def __init__(self, file_id=None, file_name=None, file_stream=None, chunk_size=0, chunk_ids=None):
        """
        Represent a file inside the minifilebox

        :param file_id: file id
        :param file_name: name of the file
        :param file_stream: file data
        :param chunk_size: size of the chunks
        :param chunk_ids: uuids of the chunks
        """
        self.file_id = file_id
        self.file_name = file_name
        self.file_stream = file_stream
        self.chunk_size = chunk_size
        self.chunk_ids = chunk_ids if chunk_ids is not None else []

    def to_dict(self):
        data = dict()

        if self.file_name:
            data['file_name'] = self.file_name

        if self.file_id:
            data['file_id'] = self.file_id

        if self.chunk_size:
            data['chunk_size'] = self.chunk_size

        if self.chunk_ids:
            data['chunk_ids'] = self.chunk_ids

        return data

    def from_dict(self, data):
        if 'file_name' in data:
            self.file_name = data['file_name']
        if 'file_id' in data:
            self.file_id = data['file_id']
        if 'chunk_size' in data:
            self.chunk_size = data['chunk_size']
        if 'chunk_ids' in data:
            self.chunk_ids = data['chunk_ids']

        return self

    def __eq__(self, other):
        return (self.file_id == other.file_id) and \
               (self.file_name == other.file_name) and \
               (self.chunk_size == other.chunk_size) and \
               (self.chunk_ids == other.chunk_ids)
