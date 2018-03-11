import os

# CONFIGURATION VARIABLE
MINIFILEBOX_CHUNK_SIZE = 500
MINIFILEBOX_BASE_URI = '/minifilebox/api/v1'
MINIFILEBOX_STORAGE_TYPE = 'remote'


# REMOTE FILE STORAGE CONFIGURATION
MINIFILEBOX_CONTEXTSTORE_HOST = os.environ.get('MINIFILEBOX_CONTEXTSTORE_HOST', '0.0.0.0')
MINIFILEBOX_CONTEXTSTORE_PORT = os.environ.get('MINIFILEBOX_CONTEXTSTORE_PORT', '5002')

MINIFILEBOX_OBJECTSTORE_HOST = os.environ.get('MINIFILEBOX_OBJECTSTORE_HOST', '0.0.0.0')
MINIFILEBOX_OBJECTSTORE_PORT = os.environ.get('MINIFILEBOX_OBJECTSTORE_PORT', '5001')
