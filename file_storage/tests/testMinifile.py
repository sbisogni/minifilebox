import unittest
import io

from file_storage.Minifile import Minifile


class MinifileTestCase(unittest.TestCase):

    def testMinifileThrownValueErrorIfEmptyFileName(self):
        self.assertRaises(ValueError, Minifile, "", 0)

    def testMinifileSetAndReturnFileId(self):
        exp_file_id = "file_id"
        minifile = Minifile("filename", 0)

        minifile.set_file_id(exp_file_id)
        self.assertEqual(exp_file_id, minifile.get_file_id())

    def testMinifileReturnFileName(self):
        exp_file_name = "file_name"
        minifile = Minifile(exp_file_name, 0)

        self.assertEqual(exp_file_name, minifile.get_file_name())

    def testMinifileReturnChunkSize(self):
        exp_chunk_size = 0
        minifile = Minifile("file", exp_chunk_size)

        self.assertEqual(exp_chunk_size, minifile.get_chunk_size())

    def testMinifileSetAndReturnChunkIds(self):
        exp_chunk_ids = [1, 2, 3, 4, 5]
        minifile = Minifile("file", 0)

        for id in exp_chunk_ids:
            minifile.add_chunk_id(id)

        self.assertEqual(exp_chunk_ids, minifile.get_chunk_ids())

    def testMinifileSetAndReturnStream(self):
        exp_stream = io.StringIO("12345")
        minifile = Minifile("file", 0)
        minifile.set_file_stream(exp_stream)

        self.assertEqual(exp_stream, minifile.get_file_stream())

    def testMinifileToDictNoChunksNoId(self):
        exp_file_name = 'file'
        exp_chunk_size = 10

        exp_result = {
            'file_name': exp_file_name,
            'chunk_size': exp_chunk_size
        }

        self.assertEqual(exp_result, Minifile(exp_file_name, exp_chunk_size).to_dict())

    def testMinifileToDictWithChunksWithId(self):
        exp_file_name = 'file'
        exp_chunk_size = 10
        exp_file_id = 'unique_id'
        exp_chunk_ids = ['1', '2', '3']

        exp_result = {
            'file_name': exp_file_name,
            'chunk_size': exp_chunk_size,
            'file_id': exp_file_id,
            'chunks': exp_chunk_ids
        }

        minifile = Minifile(exp_file_name, exp_chunk_size)
        minifile.set_file_id(exp_file_id)
        for id in exp_chunk_ids:
            minifile.add_chunk_id(id)

        self.assertEqual(exp_result, minifile.to_dict())