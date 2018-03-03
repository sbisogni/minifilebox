# from file_storage.StorageInterface import ObjectStoreInterface, ContextStoreInterface
# from file_storage.KeyValue import KeyValue
# from file_storage.Minifile import Minifile
# import requests
# import json
#
# class ObjectStoreHTTPProxy(ObjectStoreInterface):
#
#     def __init__(self, rest_endpoint):
#         self.rest_endpoint = rest_endpoint
#
#     def save(self, obj):
#         res = requests.post(self.rest_endpoint, data=obj.to_json())
#         if res.status_code is not 200:
#             raise IOError('Impossible to store object')
#
#     def load(self, key):
#         res = requests.get(self.rest_endpoint + '/%s' % key)
#         if res.status_code is not 200:
#             raise IOError('Impossible to load the object')
#         return KeyValue().from_json(res.json())
#
#     def delete(self, key):
#         res = requests.delete(self.rest_endpoint + '/%s' % key)
#         if res.status_code is not 200:
#             raise IOError('Impossible to delete the file')
#
#
# class ContextStoreHTTPProxy(ContextStoreInterface):
#
#     def __init__(self, rest_endpoint):
#         self.rest_endpoint = rest_endpoint
#
#     def save(self, mini_file):
#         res = requests.post(self.rest_endpoint, data=mini_file.to_json())
#         if res.status_code is not 200:
#             raise IOError('Impossible to store object')
#
#     def load(self, file_id):
#         res = requests.get(self.rest_endpoint + '/%s' % file_id)
#         if res.status_code is not 200:
#             raise IOError('Impossible to load the object')
#         return Minifile().from_json(res.json())
#
#     def delete(self, file_id):
#         res = requests.delete(self.rest_endpoint + '/%s' % file_id)
#         if res.status_code is not 200:
#             raise IOError('Impossible to delete the file')
#
#     def list(self):
#         res = requests.get(self.rest_endpoint + '/%s' % file_id)
#         if res.status_code is not 200:
#             raise IOError('Impossible to load the object')
#         return [Minifile().from_json(json.dumps(x)) for x in res.json()]
