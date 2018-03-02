import unittest
import json
import uuid

from file_storage.Minifile import Minifile


class MinifileTestCase(unittest.TestCase):

    def testMinifileToJsonWhenNoFields(self):
        self.assertEqual('{}', Minifile().to_json())

    def testMinifileToJson(self):
        minifile = Minifile(file_id=uuid.uuid4(),
                            file_name='name',
                            chunk_ids=['1', '2', '3'],
                            chunk_size=10)

        d = {
            'file_id': minifile.file_id.hex,
            'file_name': minifile.file_name,
            'chunk_size': minifile.chunk_size,
            'chunk_ids': minifile.chunk_ids,
        }

        self.assertEqual(json.dumps(d, sort_keys=True), minifile.to_json())

    def testMifileFromJson(self):
        exp_file = Minifile(file_id=uuid.uuid4(),
                            file_name='name',
                            chunk_ids=['1', '2', '3'],
                            chunk_size=10)
        json_obj = exp_file.to_json()

        self.assertEqual(exp_file, Minifile().from_json(json_obj))
