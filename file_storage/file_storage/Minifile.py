"""
Representation of a file inside Minifilebox
"""
import json
import uuid


class Minifile:

    def __init__(self, file_id=None, file_name=None, file_stream=None, chunk_size=0, chunk_ids=None):
        """
        Represent a file inside the minifilebox

        :param file_id: file uuid
        :param file_name: name of the file
        :param file_stream: file data
        :param chunk_size: size of the chunks
        :param chunk_ids: ids of the chunks
        """
        self.file_id = file_id
        self.file_name = file_name
        self.file_stream = file_stream
        self.chunk_size = chunk_size
        self.chunk_ids = chunk_ids if chunk_ids is not None else []

    def to_json(self):
        data = dict()

        if self.file_name:
            data['file_name'] = self.file_name

        if self.file_id:
            data['file_id'] = self.file_id.hex

        if self.chunk_size:
            data['chunk_size'] = self.chunk_size

        if self.chunk_ids:
            data['chunk_ids'] = self.chunk_ids

        return json.dumps(data, sort_keys=True)

    def from_json(self, s):
        data = json.loads(s)
        if 'file_name' in data:
            self.file_name = data['file_name']
        if 'file_id' in data:
            self.file_id = uuid.UUID(data['file_id'])
        if 'chunk_size' in data:
            self.chunk_size = data['chunk_size']
        if 'chunk_ids' in data:
            self.chunk_ids = data['chunk_ids']

        return self

    def __eq__(self, other):
        return self.to_json() == other.to_json()