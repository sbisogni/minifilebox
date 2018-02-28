import unittest
import io

from file_storage.MiniboxFile import MiniboxFile


class MiniboxFileTestCase(unittest.TestCase):

    def testMiniboxFileThrownValueErrorIfEmptyFileName(self):
        self.assertRaises(ValueError, MiniboxFile, "", 0)

    def testMiniboxFileSetAndReturnFileId(self):
        exp_file_id = "file_id"
        metadata = MiniboxFile("filename", 0)

        metadata.set_file_id(exp_file_id)
        self.assertEqual(exp_file_id, metadata.get_file_id())

    def testMiniboxFileReturnFileName(self):
        exp_file_name = "file_name"
        metadata = MiniboxFile(exp_file_name, 0)

        self.assertEqual(exp_file_name, metadata.get_file_name())

    def testMiniboxFileReturnChunkSize(self):
        exp_chunk_size = 0
        metadata = MiniboxFile("file", exp_chunk_size)

        self.assertEqual(exp_chunk_size, metadata.get_chunk_size())

    def testMiniboxFileSetAndReturnChunkIds(self):
        exp_chunk_ids = [1, 2, 3, 4, 5]
        metadata = MiniboxFile("file", 0)

        for id in exp_chunk_ids:
            metadata.add_chunk_id(id)

        self.assertEqual(exp_chunk_ids, metadata.get_chunk_ids())

    def testMiniboxFileSetAndReturnStream(self):
        exp_stream = io.StringIO("12345")
        metadata = MiniboxFile("file", 0)
        metadata.set_file_stream(exp_stream)

        self.assertEqual(exp_stream, metadata.get_file_stream())
