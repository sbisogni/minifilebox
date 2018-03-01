"""
Representation of a file inside Minifilebox
"""


class Minifile:

    def __init__(self, file_name, chunk_size):
        """
        Representation of a file metadata inside Minifilebox. All file metadata information to operate on the file

        :param file_name: the filename to which the metadata is associated to
        :param chunk_size: the size of the file's chunks
        """
        if not file_name:
            raise ValueError("file_name cannot be empty")

        self.file_id = None
        self.file_stream = None
        self.file_name = file_name
        self.chunk_size = chunk_size
        self.chunk_ids = []

    def add_chunk_id(self, chunk_id):
        self.chunk_ids.append(chunk_id)

    def get_chunk_ids(self):
        return self.chunk_ids

    def get_chunk_size(self):
        return self.chunk_size

    def get_file_name(self):
        return self.file_name

    def get_file_id(self):
        return self.file_id

    def set_file_id(self, id):
        self.file_id = id

    def get_file_stream(self):
        return self.file_stream

    def set_file_stream(self, stream):
        self.file_stream = stream

    def to_dict(self):
        result = dict()

        result['file_name'] = self.file_name
        result['chunk_size'] = self.chunk_size

        if self.file_id:
            result['file_id'] = self.file_id

        if self.chunk_ids:
            result['chunks'] = self.chunk_ids

        return result
