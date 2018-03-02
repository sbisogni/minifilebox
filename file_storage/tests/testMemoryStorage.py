import unittest
from file_storage.MemoryStorage import ObjectStoreInMemory, ContextStoreInMemory, KeyValue, Minifile


class ObjectStoreInMemoryTestCase(unittest.TestCase):

    def setUp(self):
        self.object_store = ObjectStoreInMemory()

    def testSaveAndLoadObject(self):
        exp_obj = KeyValue(key='key', value=b'value')

        self.object_store.save(exp_obj)
        act_obj = self.object_store.load(exp_obj.key)

        self.assertEqual(exp_obj, act_obj)

    def testDeleteErasesObjectById(self):
        exp_obj = KeyValue(key='key', value=b'value')

        self.object_store.save(exp_obj)
        self.object_store.delete(exp_obj.key)

        self.assertRaises(KeyError, self.object_store.load, exp_obj.key)


class ContextStoreInMemoryTestCase(unittest.TestCase):

    def setUp(self):
        self.context_store = ContextStoreInMemory()

    def testSaveAndLoadObject(self):
        exp_file = Minifile(file_id='id', file_name='name')

        self.context_store.save(exp_file)
        act_file = self.context_store.load(exp_file.file_id)

        self.assertEqual(exp_file, act_file)

    def testDeleteErasesObjectById(self):
        exp_file = Minifile(file_id='id', file_name='name')

        self.context_store.save(exp_file)
        self.context_store.delete(exp_file.file_id)

        self.assertRaises(KeyError, self.context_store.load, exp_file.file_id)

    def testListReturnsAllFiles(self):
        exp_list = [ Minifile(file_id='1', file_name='name'),
                     Minifile(file_id='2', file_name='name'),
                     Minifile(file_id='3', file_name='name'),
                     Minifile(file_id='4', file_name='name')]

        for file in exp_list:
            self.context_store.save(file)

        self.assertEqual(exp_list, self.context_store.list())
