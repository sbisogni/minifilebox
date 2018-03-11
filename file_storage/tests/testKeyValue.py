import unittest
import base64
from file_storage.KeyValue import KeyValue


class KeyValueTestCase(unittest.TestCase):

    def testKeyValueIsInitialized(self):
        exp_key = 'key'
        exp_value = 'value'

        obj = KeyValue(exp_key, exp_value)

        self.assertEqual(exp_key, obj.key)
        self.assertEqual(exp_value, obj.value)

    def testKeyValueToJsonWhenNoFields(self):
        self.assertEqual({}, KeyValue().to_dict())

    def testKeyValueToJson(self):
        key_value = KeyValue(key='1', value=b'value')
        d = {'key': key_value.key, 'value': base64.encodebytes(key_value.value).decode()}

        self.assertEqual(d, key_value.to_dict())

    def testKeyValueFromJson(self):
        exp_key_value = KeyValue(key='1', value=b'value')
        exp_dict = exp_key_value.to_dict()

        self.assertEqual(exp_key_value, KeyValue().from_dict(exp_dict))
