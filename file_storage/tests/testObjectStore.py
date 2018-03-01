import unittest
from file_storage.ObjectStoreInMemory import ObjectStoreInMemory


class ObjectStoreInMemoryTestCase(unittest.TestCase):

    def setUp(self):
        self.object_store = ObjectStoreInMemory()

    def testSaveIsGeneratingUniqueId(self):
        obj = "object"
        self.assertTrue(self.object_store.save(obj))

    def testLoadRetrieveObjectById(self):
        exp_obj = "object"
        id = self.object_store.save(exp_obj)

        act_obj = self.object_store.load(id);

        self.assertEqual(exp_obj, act_obj)

    def testDeleteErasesObjectById(self):
        obj = "object"
        id = self.object_store.save(obj)
        self.object_store.delete(id)

        self.assertRaises(KeyError, self.object_store.load, id)

    def testDeleteReturnsErasedObject(self):
        exp_obj = "object"
        id = self.object_store.save(exp_obj)
        act_obj = self.object_store.delete(id)

        self.assertEqual(exp_obj, act_obj)
