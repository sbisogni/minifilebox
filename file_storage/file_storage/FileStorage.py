"""
FileStorage store the file splitting them in chunks
"""

import tempfile
import uuid
import logging
from file_storage.Minifile import Minifile
from file_storage.KeyValue import KeyValue
from file_storage import MemoryStorage
from file_storage import CassandraStorage


class FileStorage:
    """
    Provide operations to manipulate files inside the FileStorage
    """

    # The min chunk size supported by the system
    MIN_CHUNK_SIZE = 1
    # The max chunk size supported by the system. 100MB
    MAX_CHUNK_SIZE = 100000000

    @staticmethod
    def generate_uuid_of(value):
        """
        Generates unique random uuid
        :param value: not used
        :return: the unique id
        """
        return str(uuid.uuid4().hex)

    # Called by FileStorage to generate object id
    generate_object_id = generate_uuid_of
    # Called by FileStorage to generate file id
    generate_file_id = generate_uuid_of

    def __init__(self, context_store, object_store):
        """
        Create a new FileStorage with the given configuration. The ContextStore object specifies where to store the file
        metadata information. The ObjectStore specifies where to store the file data.
        By using dependency injection the FileStorage layout can be adapted depending on the execution environment

        :param context_store: ContextStore where to store file metadata information
        :param object_store: ObjectStore where to store file data
        """
        self._context_store = context_store
        self._object_store = object_store

    def save(self, minifile):
        """
        Store the given file in the FileStorage splitting it in chunks of the dimension as given in the Minifile
        The chunk size must be included among [MIN_CHUNK_SIZE, MAX_CHUNK_SIZE]
        :param minifile: Minifile holding the information of the file to store. Once the file is stored further
                        metadata are added to the structure
        """
        logging.info('saving file_name = %s, chunk_size = %s' % (minifile.file_name, minifile.chunk_size))
        # Generate the unique file id
        minifile.file_id = FileStorage.generate_file_id(minifile)
        self._save(minifile)

        logging.info('saving in context store minifile = %s' % minifile.to_json())
        self._context_store.save(minifile)

        logging.info('file storage save done - file_name = %s, file_id = %s' % (minifile.file_name, minifile.file_id))

    def load(self, file_id):
        """
        Load the file identified by the given id and returns it back to the user inside a Minifile
        :param file_id: the id of the file to load
        :return Minifile holding the file details
        """
        minifile = self._context_store.load(file_id)
        self._load(minifile)
        return minifile

    def delete(self, file_id):
        """
        Delete the file identified by the given id
        :param file_id: the id of the file to delete
        :return: Minifile holding the file details
        """
        minifile = self._context_store.load(file_id)
        self._delete(minifile)
        self._context_store.delete(minifile)
        return minifile

    def list(self):
        """
        Returns information about all the file store in the FileStorage
        :return: List[Minifile]
        """
        return self._context_store.list()

    # PRIVATE IMPLEMENTATION

    # Specify the max size of the temporally file before being written on the disk, otherwise is kept in memory
    MAX_TMP_FILE_SIZE = 0 # Default value

    def _save(self, minifile):
        chunk_size = minifile.chunk_size
        if chunk_size < FileStorage.MIN_CHUNK_SIZE or chunk_size > FileStorage.MAX_CHUNK_SIZE:
            raise ValueError('chunks size must be included [%s, %s]',
                             FileStorage.MIN_CHUNK_SIZE, FileStorage.MAX_CHUNK_SIZE)

        file_stream = minifile.file_stream

        while True:
            chunk = file_stream.read(chunk_size)
            if len(chunk) is not 0:
                obj_id = FileStorage.generate_object_id(chunk)
                self._object_store.save(KeyValue(key=obj_id, value=chunk))
                minifile.chunk_ids.append(obj_id)
            else:
                break

    def _load(self, minifile):
        if not minifile.chunk_ids:
            raise ValueError("No chunks in metadata, file cannot be rebuilt")

        tmp_file = None
        for id in minifile.chunk_ids:
            chunk = self._object_store.load(id)
            # We have at least one good chunk we create the tmp file
            if not tmp_file:
                tmp_file = tempfile.SpooledTemporaryFile()

            tmp_file.write(chunk.value)

        tmp_file.seek(0)
        minifile.file_stream = tmp_file

    def _delete(self, minifile):
        if not minifile.chunk_ids:
            raise ValueError("No chunks in metadata, file cannot deleted")

        for id in minifile.chunk_ids:
            self._object_store.delete(id)


def create_memory_file_storage():
    return FileStorage(MemoryStorage.ObjectStoreInMemory(),
                       MemoryStorage.ObjectStoreInMemory())


def create_cassandra_file_storage(key_space_context, key_space_obj, cluster_nodes):
    return FileStorage(CassandraStorage.ContextStoreCassandra(key_space_context, cluster_nodes),
                       CassandraStorage.ObjectStoreCassandra(key_space_obj, cluster_nodes))

