"""
Storage interfaces handled by FileStorage
"""


class ContextStoreInterface:
    """
    The ContextStore interface
    """

    def save(self, minifile):
        """
        Save the metadata inside the given Minifile in the ContextStore. A unique file id is assigned
        :param minifile: The file metadata to store in the context. At the end of execution, a unique file id is assigned
        :return Unique file id
        """
        pass

    def load(self, file_id):
        """
        Load the metadata associated to the given id
        :param file_id: The unique file id
        :return Minifile instance
        :except KeyError if file not found
        """
        pass

    def delete(self, file_id):
        """
        Delete the metadata of the given file id
        :param file_id: The id of the file to delete
        :except KeyError if file not found
        """
        pass

    def list(self):
        """
        Returns information about all the file store in the FileStorage
        :return: List[Minifile]
        """
        pass


class ObjectStoreInterface:
    """
    The ObjectStore interface
    """
    
    def save(self, key, value):
        """
        Store the given (key, object) in the store

        :param key: unique key
        :param value: the object to store
        """
        pass

    def load(self, key):
        """
        Return the object identified by the given key

        :param key: unique object key
        :return: value the associated value
        :except KeyError if key cannot be found
        """
        pass

    def delete(self, key):
        """
        Delete the object with the given object key

        :param key: unique object key
        :except KeyError if object cannot be found
        """
        pass
