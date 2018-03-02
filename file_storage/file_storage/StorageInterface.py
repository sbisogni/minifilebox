"""
Storage interfaces handled by FileStorage
"""


class ObjectStoreInterface:
    """
    The ObjectStore interface. Aimed for documentation
    """
    
    def save(self, obj):
        """
        A KeyValue object to store

        :param KeyValue object
        """
        pass

    def load(self, key):
        """
        Retrieve the Object identified by the given key

        :param key: unique object key
        :return: the KeyValue object
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


class ContextStoreInterface:
    """
    The ContextStore interface. Aimed for documentation
    """

    def save(self, mini_file):
        """
        Save the given Minifile in the box

        :param The Minifile object to store
        """
        pass

    def load(self, file_id):
        """
        Retrieve the Minifile identified by the given key

        :param file_id: unique object key
        :return: The associated Minifile
        :except KeyError if file_id cannot be found
        """
        pass

    def delete(self, file_id):
        """
        Delete the Minifile with the given object key

        :param file_id: unique Minifile id
        :except KeyError if object cannot be found
        """
        pass

    def list(self):
        """
        List all Minifile in the box
        :return: List of Minifile objects
        """
        pass