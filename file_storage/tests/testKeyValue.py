import unittest
import json
import uuid
from file_storage.KeyValue import KeyValue


class KeyValueTestCase(unittest.TestCase):

    def testKeyValueToJsonWhenNoFields(self):
        self.assertEqual('{}', KeyValue().to_json())

    def testKeyValueToJson(self):
        key_value = KeyValue(key=uuid.uuid4(), value="value")
        d = {'key': key_value.key.hex, 'value': key_value.value}

        self.assertEqual(json.dumps(d, sort_keys=True), key_value.to_json())

    def testKeyValueFromJson(self):
        exp_key_value = KeyValue(key=uuid.uuid4(), value="value")
        json_obj = exp_key_value.to_json()

        self.assertEqual(exp_key_value, KeyValue().from_json(json_obj))
