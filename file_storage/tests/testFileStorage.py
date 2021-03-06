import unittest
from unittest.mock import Mock, call
import io

from file_storage.FileStorage import FileStorage
from file_storage.Minifile import Minifile
from file_storage.KeyValue import KeyValue


class FileStorageTestCase(unittest.TestCase):

    def setUp(self):
        self.object_store_mock = Mock()
        self.context_store_mock = Mock()
        self.storage = FileStorage(self.context_store_mock, self.object_store_mock)

    def testSaveCallsContextStoreToSaveFileMetadata(self):
        # We disable the internal _save function as we are not interested for this test
        def disable_internal_save(any):
            pass

        self.storage._save = disable_internal_save
        file = Minifile()

        self.storage.save(file)

        self.context_store_mock.save.assert_has_calls([call(file)])

    def testLoadCallsContextStoreToLoadFileMetadata(self):
        # We disable the internal _load function as we are not interested for this test
        def disable_internal_load(any):
            pass

        self.storage._load = disable_internal_load
        exp_file = Minifile(file_id="id")

        self.context_store_mock.load.return_value = exp_file
        self.storage.load(exp_file.file_id)

        self.context_store_mock.load.assert_has_calls([call(exp_file.file_id)])

    def testLoadReturnsMinifile(self):
        # We disable the internal _load function as we are not interested for this test
        def disable_internal_load(any):
            pass

        self.storage._load = disable_internal_load
        exp_file = Minifile(file_id="id", file_name="file")

        self.context_store_mock.load.return_value = exp_file
        act_file = self.storage.load(exp_file.file_id)

        self.assertEqual(exp_file, act_file)

    def testDeleteCallsContextStoreToLoadFileMetadata(self):
        # We disable the internal _load function as we are not interested for this test
        def disable_internal_delete(any):
            pass

        self.storage._delete = disable_internal_delete
        exp_file = Minifile(file_id="id")
        self.context_store_mock.load.return_value = exp_file
        self.storage.delete(exp_file.file_id)

        self.context_store_mock.load.assert_has_calls([call(exp_file.file_id)])

    def testDeleteCallsContextStoreToDeleteFileMetadata(self):
        # We disable the internal _load function as we are not interested for this test
        def disable_internal_delete(any):
            pass

        self.storage._delete = disable_internal_delete
        exp_file = Minifile(file_id="id")
        self.context_store_mock.load.return_value = exp_file

        self.storage.delete(exp_file.file_id)

        self.context_store_mock.delete.assert_has_calls([call(exp_file.file_id)])

    def testDeleteReturnsMinifileOfDeletedFile(self):
        # We disable the internal _delete function as we are not interested for this test
        def disable_internal_delete(any):
            pass

        self.storage._delete = disable_internal_delete
        exp_file = Minifile(file_id="id")
        self.context_store_mock.load.return_value = exp_file

        act_file = self.storage.delete(exp_file.file_id)

        self.assertEqual(exp_file, act_file)

    def testListCallsContextStoreToListFiles(self):
        exp_list = [Minifile(file_id="1"),
                    Minifile(file_id="2")]
        self.context_store_mock.list.return_value = exp_list

        self.storage.list()

        self.context_store_mock.list.assert_called()

    def testListReturnsListOfFiles(self):
        exp_list = [Minifile(file_id="1"),
                    Minifile(file_id="2")]
        self.context_store_mock.list.return_value = exp_list

        act_list = self.storage.list()

        self.assertEqual(exp_list, act_list)

    # VALIDATION INTERNAL SAVE METHOD
    def testSaveThrowValueErrorIfChunkSizeLessThanMinChunkSize(self):
        self.assertRaises(ValueError, self.storage._save, Minifile(chunk_size=FileStorage.MIN_CHUNK_SIZE - 1))

    def testSaveThrowValueErrorIfChunkSizeGreaterThanMaxChunkSize(self):
        self.assertRaises(ValueError, self.storage._save, Minifile(chunk_size=FileStorage.MAX_CHUNK_SIZE + 1))

    def testSaveGeneratesNoChunksIfStreamIsEmpty(self):
        file = Minifile(file_stream=io.BytesIO(), chunk_size=1)

        self.storage._save(file)

        self.assertTrue(len(file.chunk_ids) == 0)

    def testSavesSplitsStreamInFiveChunks(self):
        file = Minifile(file_stream=io.BytesIO('1234567890'.encode()), chunk_size=2)

        self.storage._save(file)

        self.assertEqual(len(file.chunk_ids), 5)

    def testSavesSplitsStreamInTenChunks(self):
        file = Minifile(file_stream=io.BytesIO('1234567890'.encode()), chunk_size=1)

        self.storage._save(file)

        self.assertEqual(len(file.chunk_ids), 10)

    def testSaveCallsObjectStoreForEachChunk(self):

        FileStorage.generate_object_id = lambda x: 'id'

        stream = io.BytesIO('12345'.encode())
        mbf = Minifile(file_stream=stream, chunk_size=1)

        self.storage._save(mbf)

        self.object_store_mock.save.assert_has_calls([call(KeyValue('id', b'1')),
                                                      call(KeyValue('id', b'2')),
                                                      call(KeyValue('id', b'3')),
                                                      call(KeyValue('id', b'4')),
                                                      call(KeyValue('id', b'5'))])

    def testSaveNoCallsObjectStoreIfStreamIsEmpty(self):
        mbf = Minifile(file_stream=io.BytesIO(), chunk_size=1)

        self.storage._save(mbf)

        self.object_store_mock.assert_not_called()

    # # VALIDATION INTERNAL LOAD METHOD
    def testLoadThrowsValueErrorIsFileMetadataHasNoChunks(self):
        mbf = Minifile()
        self.assertRaises(ValueError, self.storage._load, mbf)

    def testLoadCallsObjectStoreForEachChunk(self):
        mbf = Minifile(chunk_ids=[1, 2, 3, 4, 5])

        self.object_store_mock.load.return_value = KeyValue('id', b'12345')

        self.storage._load(mbf)
        self.object_store_mock.load.assert_has_calls([call(1), call(2), call(3), call(4), call(5)])

    def testLoadReturnsStream(self):
        exp_stream = io.BytesIO('12345'.encode())
        chunk_size = 1

        mbf = Minifile(chunk_size=chunk_size,
                       file_stream=exp_stream,
                       chunk_ids=[1, 2, 3, 4, 5])

        # Work around as I cannot manage to make it working with Mock library
        def load_return_exp_stream(id):
            return KeyValue(id, exp_stream.read(chunk_size))

        self.storage._object_store.load = load_return_exp_stream
        self.storage._load(mbf)

        act_stream = mbf.file_stream
        exp_stream.seek(0)
        self.assertEqual(act_stream.read(), exp_stream.read())

    # VALIDATION INTERNAL DELETE METHOD

    def testDeleteThrowsValueErrorIfFileMetadataHasNoChunks(self):
        mbf = Minifile()
        self.assertRaises(ValueError, self.storage._delete, mbf)

    def testDeleteCallsObjectStoreDeleteForEachChunkId(self):
        mbf = Minifile(chunk_ids=[1, 2, 3])

        calls = [call(1), call(2), call(3)]
        self.storage._delete(mbf)
        self.object_store_mock.delete.assert_has_calls(calls)

    def testDeleteThrowsKeyErrorIfChunkNotFound(self):
        metadata = Minifile(chunk_ids=[1])

        def delete_raise_io_error(id):
            raise KeyError("ObjectStore: Chunk not found id = %s" % id)
        self.storage._object_store.delete = delete_raise_io_error

        self.assertRaises(KeyError, self.storage._delete, metadata)

    def testIsUniqueIdGenerated(self):
        self.assertTrue(FileStorage.generate_uuid_of("any"))

    def testAreIdsUnique(self):
        ids = []
        for x in range(10000):
            ids.append(FileStorage.generate_uuid_of("any"))

        seen = set()
        unique = [x for x in ids if x not in seen and not seen.add(x)]
        self.assertEqual(len(ids), len(unique))
