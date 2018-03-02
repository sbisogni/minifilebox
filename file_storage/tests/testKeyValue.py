import unittest
import json
import base64
from file_storage.KeyValue import KeyValue


class KeyValueTestCase(unittest.TestCase):

    def testKeyValueToJsonWhenNoFields(self):
        self.assertEqual('{}', KeyValue().to_json())

    def testKeyValueToJson(self):
        key_value = KeyValue(key='1', value=b'value')
        d = {'key': key_value.key, 'value': base64.encodebytes(key_value.value).decode()}

        self.assertEqual(json.dumps(d, sort_keys=True), key_value.to_json())

    def testKeyValueFromJson(self):
        exp_key_value = KeyValue(key='1', value=b'value')
        json_obj = exp_key_value.to_json()

        self.assertEqual(exp_key_value, KeyValue().from_json(json_obj))
