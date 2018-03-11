import unittest

from file_storage.Minifile import Minifile


class MinifileTestCase(unittest.TestCase):

    def testMinifileToDictWhenNoFields(self):
        self.assertEqual({}, Minifile().to_dict())

    def testMinifileToDict(self):
        minifile = Minifile(file_id='1',
                            file_name='name',
                            chunk_ids=['1', '2', '3'],
                            chunk_size=10)

        d = {
            'file_id': minifile.file_id,
            'file_name': minifile.file_name,
            'chunk_size': minifile.chunk_size,
            'chunk_ids': minifile.chunk_ids
        }

        self.assertEqual(d, minifile.to_dict())

    def testMifileFromJson(self):
        exp_file = Minifile(file_id='1',
                            file_name='name',
                            chunk_ids=['1', '2', '3'],
                            chunk_size=10)

        ext_dict = exp_file.to_dict()

        self.assertEqual(exp_file, Minifile().from_dict(ext_dict))
