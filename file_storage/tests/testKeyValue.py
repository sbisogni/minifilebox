import unittest
from file_storage.KeyValue import KeyValue


class KeyValueTestCase(unittest.TestCase):

    def testKeyValueThrowsValueErrorIfKeyIsNone(self):
        self.assertRaises(ValueError, KeyValue, None, "Any")

    def testKeyValueThrowsValueErrorIfValueIsNone(self):
        self.assertRaises(ValueError, KeyValue, "Any", None)

    def testKeyIsSetAndRetrieved(self):
        exp_key = "key"
        self.assertEqual(exp_key, KeyValue(exp_key, "Any").get_key())

    def testValueIsSetAndRetrieved(self):
        exp_value = "value"
        self.assertEqual(exp_value, KeyValue("Any", exp_value).get_value())

    def testKeyValueToDict(self):
        exp_key = "key"
        exp_value = "value"
        exp_dict = {'key': exp_key, 'value': exp_value}

        self.assertEqual(exp_dict, KeyValue(exp_key, exp_value).to_dict())