import unittest
import io

from file_storage.Minifile import Minifile


class MinifileTestCase(unittest.TestCase):

    def testMinifileThrownValueErrorIfEmptyFileName(self):
        self.assertRaises(ValueError, Minifile, "", 0)

    def testMinifileSetAndReturnFileId(self):
        exp_file_id = "file_id"
        metadata = Minifile("filename", 0)

        metadata.set_file_id(exp_file_id)
        self.assertEqual(exp_file_id, metadata.get_file_id())

    def testMinifileReturnFileName(self):
        exp_file_name = "file_name"
        metadata = Minifile(exp_file_name, 0)

        self.assertEqual(exp_file_name, metadata.get_file_name())

    def testMinifileReturnChunkSize(self):
        exp_chunk_size = 0
        metadata = Minifile("file", exp_chunk_size)

        self.assertEqual(exp_chunk_size, metadata.get_chunk_size())

    def testMinifileSetAndReturnChunkIds(self):
        exp_chunk_ids = [1, 2, 3, 4, 5]
        metadata = Minifile("file", 0)

        for id in exp_chunk_ids:
            metadata.add_chunk_id(id)

        self.assertEqual(exp_chunk_ids, metadata.get_chunk_ids())

    def testMinifileSetAndReturnStream(self):
        exp_stream = io.StringIO("12345")
        metadata = Minifile("file", 0)
        metadata.set_file_stream(exp_stream)

        self.assertEqual(exp_stream, metadata.get_file_stream())
