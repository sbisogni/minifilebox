import unittest
from file_storage.ContextStoreInMemory import ContextStoreMemory
from file_storage.Minifile import Minifile

class ContextStoreMemoryTestCase(unittest.TestCase):

    def setUp(self):
        self.context_store = ContextStoreMemory()

    def testSaveGeneratesUniqueId(self):
        mbf = Minifile("file.txt", 1)
        id = self.context_store.save(mbf)

        self.assertTrue(mbf.get_file_id())
        self.assertEqual(id, mbf.get_file_id())

    def testLoadRetrieveMinifileById(self):
        exp_mbf = Minifile("file.txt", 1)

        self.context_store.save(exp_mbf)
        act_mbf = self.context_store.load(exp_mbf.get_file_id())

        self.assertEqual(exp_mbf, act_mbf)

    def testDeleteErasesMinifileById(self):
        mbf = Minifile("file.txt", 1)

        id = self.context_store.save(mbf)
        self.context_store.load(id)
        self.context_store.delete(id)

        self.assertRaises(KeyError, self.context_store.load, id)

    def testDeleteReturnsErasedMinifile(self):
        exp_mbf = Minifile("file.txt", 1)

        id = self.context_store.save(exp_mbf)
        act_mbf = self.context_store.delete(id)

        self.assertEqual(exp_mbf, act_mbf)

    def testListIsReturningAllFiles(self):
        exp_list = [Minifile("file", 1), Minifile("file", 1), Minifile("file", 1)]

        for mbf in exp_list:
            self.context_store.save(mbf)

        act_list = self.context_store.list()

        self.assertEqual(exp_list, act_list)