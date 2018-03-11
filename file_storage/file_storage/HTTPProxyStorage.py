from file_storage.StorageInterface import ObjectStoreInterface, ContextStoreInterface
from file_storage.KeyValue import KeyValue
from file_storage.Minifile import Minifile
import requests
import json


class ObjectStoreHTTPProxy(ObjectStoreInterface):

    def __init__(self, rest_endpoint):
        self.rest_endpoint = rest_endpoint

    def save(self, obj):
        res = requests.post(self.rest_endpoint, json=obj.to_dict())
        if res.status_code is not 200:
            raise IOError('Impossible to store object')

    def load(self, key):
        res = requests.get(self.rest_endpoint + '/%s' % key)
        if res.status_code is not 200:
            raise IOError('Impossible to load the object')
        x = KeyValue().from_dict(res.json())
        return x

    def delete(self, key):
        res = requests.delete(self.rest_endpoint + '/%s' % key)
        if res.status_code is not 200:
            raise IOError('Impossible to delete the file')


class ContextStoreHTTPProxy(ContextStoreInterface):

    def __init__(self, rest_endpoint):
        self.rest_endpoint = rest_endpoint

    def save(self, mini_file):
        res = requests.post(self.rest_endpoint, json=mini_file.to_dict())
        if res.status_code is not 200:
            raise IOError('Impossible to store object')

    def load(self, file_id):
        res = requests.get(self.rest_endpoint + '/%s' % file_id)
        if res.status_code is not 200:
            raise IOError('Impossible to load the object')
        return Minifile().from_dict(res.json())

    def delete(self, file_id):
        res = requests.delete(self.rest_endpoint + '/%s' % file_id)
        if res.status_code is not 200:
            raise IOError('Impossible to delete the file')

    def list(self):
        res = requests.get(self.rest_endpoint + '/%s' % file_id)
        if res.status_code is not 200:
            raise IOError('Impossible to load the object')
        return [Minifile().from_dict(x) for x in res.json()]
