import unittest
from unittest.mock import Mock, call
from io import BytesIO

from file_storage.FileStorage import FileStorage
from file_storage.MiniboxFile import MiniboxFile


class FileStorageTestCase(unittest.TestCase):

    def setUp(self):
        self.object_store_mock = Mock()
        self.context_store_mock = Mock()
        self.storage = FileStorage(self.context_store_mock, self.object_store_mock)

    def testSaveThrowsRuntimeErrorIfNoIdGenerated(self):
        # We disable the internal _save function as we are not interested for this test
        def disable_internal_save(any):
            pass

        self.storage._save = disable_internal_save
        mbf = MiniboxFile("file", 1)

        self.assertRaises(RuntimeError, self.storage.save, mbf)

    def testSaveCallsContextStoreToSaveFileMetadata(self):
        # We disable the internal _save function as we are not interested for this test
        def disable_internal_save(any):
            pass

        self.storage._save = disable_internal_save
        mbf = MiniboxFile("file", 1)
        self.context_store_mock.save.side_effect = mbf.set_file_id("id")

        self.storage.save(mbf)

        self.context_store_mock.save.assert_has_calls([call(mbf)])

    def testLoadCallsContextStoreToLoadFileMetadata(self):
        # We disable the internal _load function as we are not interested for this test
        def disable_internal_load(any):
            pass

        exp_id = "id"
        self.storage._load = disable_internal_load

        self.storage.load(exp_id)

        self.context_store_mock.load.assert_has_calls([call(exp_id)])

    def testLoadReturnsMiniboxFileOfLoadedFile(self):
        # We disable the internal _load function as we are not interested for this test
        def disable_internal_load(any):
            pass

        exp_id = "id"
        self.storage._load = disable_internal_load
        exp_mbf = MiniboxFile("file", 1)
        self.context_store_mock.load.return_value = exp_mbf

        act_mbf = self.storage.load(exp_id)

        self.assertEqual(exp_mbf, act_mbf)

    def testDeleteCallsContextStoreToLoadFileMetadata(self):
        # We disable the internal _delete function as we are not interested for this test
        def disable_internal_delete(any):
            pass

        exp_id = "id"
        self.storage._delete = disable_internal_delete

        self.storage.delete(exp_id)

        self.context_store_mock.load.assert_has_calls([call(exp_id)])

    def testDeleteCallsContextStoreToDeleteFileMetadata(self):
        # We disable the internal _delete function as we are not interested for this test
        def disable_internal_delete(any):
            pass

        exp_id = "id"
        self.storage._delete = disable_internal_delete

        self.storage.delete(exp_id)

        self.context_store_mock.delete.assert_has_calls([call(exp_id)])

    def testDeleteReturnsMiniboxFileOfDeletedFile(self):
        # We disable the internal _delete function as we are not interested for this test
        def disable_internal_delete(any):
            pass

        exp_id = "id"
        self.storage._delete = disable_internal_delete
        exp_mbf = MiniboxFile("file", 1)
        self.context_store_mock.delete.return_value = exp_mbf

        act_mbf = self.storage.delete(exp_id)

        self.assertEqual(exp_mbf, act_mbf)

    def testListCallsContextStoreToListFiles(self):
        self.storage.list()
        self.context_store_mock.list.assert_called()

    def testListReturnsListOfFiles(self):
        exp_result = [MiniboxFile("file", 1), MiniboxFile("file", 1)]
        self.context_store_mock.list.return_value = exp_result

        act_result = self.storage.list()

        self.assertEqual(exp_result, act_result)

    # VALIDATION INTERNAL SAVE METHOD
    def testSaveThrowValueErrorIfChunkSizeLessThanMinChunkSize(self):
        self.assertRaises(ValueError, self.storage._save, MiniboxFile("file.txt", FileStorage.MIN_CHUNK_SIZE - 1))

    def testSaveThrowValueErrorIfChunkSizeGreaterThanMaxChunkSize(self):
        self.assertRaises(ValueError, self.storage._save, MiniboxFile("file.txt", FileStorage.MAX_CHUNK_SIZE + 1))

    def testSaveGeneratesNoChunksIfStreamIsEmpty(self):
        mbf = MiniboxFile("file.txt", 1)
        mbf.set_file_stream(BytesIO())

        self.storage._save(mbf)

        self.assertTrue(len(mbf.get_chunk_ids()) == 0)

    def testSavesSplitsStreamInTenChunks(self):
        mbf = MiniboxFile("file.txt",1)
        mbf.set_file_stream(BytesIO('1234567890'.encode()))

        self.storage._save(mbf)

        self.assertTrue(len(mbf.get_chunk_ids()) == 10)

    def testSavesSplitsStreamInFiveChunks(self):
        mbf = MiniboxFile("file.txt", 2)
        mbf.set_file_stream(BytesIO('1234567890'.encode()))

        self.storage._save(mbf)

        self.assertTrue(len(mbf.get_chunk_ids()) == 5)

    def testSaveCallesObjectStoreForEachChunk(self):
        mbf = MiniboxFile("file.txt", 1)
        mbf.set_file_stream(BytesIO('12345'.encode()))

        self.storage._save(mbf)

        self.object_store_mock.save.assert_has_calls([call(b'1'), call(b'2'), call(b'3'), call(b'4'), call(b'5')])

    def testSaveNoCallsObjectStoreIfStreamIsEmpty(self):
        mbf = MiniboxFile("file.txt", 1)
        mbf.set_file_stream(BytesIO())

        self.storage._save(mbf)

        self.object_store_mock.assert_not_called()

    # VALIDATION INTERNAL LOAD METHOD

    def testLoadThrowsValueErrorIsFileMetadataHasNoChunks(self):
        mbf = MiniboxFile("file.txt", 0)
        self.assertRaises(ValueError, self.storage._load, mbf)

    def testLoadCallsObjectStoreForEachChunk(self):
        mbf = MiniboxFile("file.txt", 1)
        mbf.add_chunk_id(1)
        mbf.add_chunk_id(2)
        mbf.add_chunk_id(3)
        mbf.add_chunk_id(4)
        mbf.add_chunk_id(5)

        self.object_store_mock.load.return_value = b'12345'

        self.storage._load(mbf)
        self.object_store_mock.load.assert_has_calls([call(1), call(2), call(3), call(4), call(5)])

    def testLoadThrowsIOErrorIfChunkCannotBeFound(self):
        metadata = MiniboxFile("file.txt", 0)
        metadata.add_chunk_id(1)
        metadata.add_chunk_id(2)

        self.object_store_mock.load.return_value = None
        self.assertRaises(IOError, self.storage._load, metadata)

    def testLoadReturnsStream(self):
        exp_stream = BytesIO('12345'.encode())
        chunk_size = 1

        mbf = MiniboxFile("file.txt", chunk_size)
        mbf.set_file_stream(exp_stream)
        mbf.add_chunk_id(1)
        mbf.add_chunk_id(2)
        mbf.add_chunk_id(3)
        mbf.add_chunk_id(4)
        mbf.add_chunk_id(5)

        # Work around as I cannot manage to make it working with Mock library
        def load_return_exp_stream(id):
            return exp_stream.read(chunk_size)

        self.storage._object_store.load = load_return_exp_stream
        self.storage._load(mbf)

        act_stream = mbf.get_file_stream()
        exp_stream.seek(0)
        self.assertEqual(act_stream.read(), exp_stream.read())

    # VALIDATION INTERNAL DELETE METHOD

    def testDeleteThrowsValueErrorIfFileMetadataHasNoChunks(self):
        mbf = MiniboxFile("file.txt", 0)
        self.assertRaises(ValueError, self.storage._delete, mbf)

    def testDeleteCallsObjectStoreDeleteForEachChunkId(self):
        mbf = MiniboxFile("file.txt", 0)
        mbf.add_chunk_id(1)
        mbf.add_chunk_id(2)
        mbf.add_chunk_id(3)

        calls = [call(1), call(2), call(3)]
        self.storage._delete(mbf)
        self.object_store_mock.delete.assert_has_calls(calls)

    def testDeleteThrowsIoErrorIfChunkNotFound(self):
        metadata = MiniboxFile("file.txt", 0)
        metadata.add_chunk_id(1)

        def delete_raise_io_error(id):
            raise IOError("ObjectStore: Chunk not found id = %s" % id)
        self.storage._object_store.delete = delete_raise_io_error

        self.assertRaises(IOError, self.storage._delete, metadata)
