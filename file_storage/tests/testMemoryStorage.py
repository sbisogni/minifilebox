import unittest
from file_storage.MemoryStorage import ObjectStoreInMemory


class ObjectStoreInMemoryTestCase(unittest.TestCase):

    def setUp(self):
        self.object_store = ObjectStoreInMemory()

    def testLoadRetrieveObjectById(self):
        exp_obj = "object"
        id = "key"

        self.object_store.save(id, exp_obj)
        act_obj = self.object_store.load(id)

        self.assertEqual(exp_obj, act_obj)

    def testDeleteErasesObjectById(self):
        obj = "object"
        id = "id"

        self.object_store.save(id, obj)
        self.object_store.delete(id)

        self.assertRaises(KeyError, self.object_store.load, id)

    def testDeleteReturnsErasedObject(self):
        exp_obj = "object"
        id = "key"

        self.object_store.save(id, exp_obj)
        act_obj = self.object_store.delete(id)

        self.assertEqual(exp_obj, act_obj)

    def testListIsReturningAllObjects(self):
        exp_obj_list = ["object1", "object2", "object3"]

        for key in range(len(exp_obj_list)):
            self.object_store.save(key, exp_obj_list[key])

        act_obj_list = self.object_store.list()

        self.assertEqual(exp_obj_list, act_obj_list)