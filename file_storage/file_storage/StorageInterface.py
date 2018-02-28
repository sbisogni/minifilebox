"""
Storage interfaces handled by FileStorage
"""


class ContextStoreInterface:
    """
    The ContextStore interface
    """

    def save(self, miniboxfile):
        """
        Save the metadata inside the given MiniboxFile in the ContextStore. A unique file id is assigned
        :param miniboxfile: The file metadata to store in the context. At the end of execution, a unique file id is assigned
        :return Unique file id
        """
        pass

    def load(self, file_id):
        """
        Load the metadata associated to the given id
        :param file_id: The unique file id
        :return: MiniboxFile holding the information of the file
        """
        pass

    def delete(self, file_id):
        """
        Delete the metadata of the given file id
        :param file_id: The id of the file to delete
        :return: MiniboxFile holding the information of the deleted file
        """
    def list(self):
        """
        Returns information about all the file store in the FileStorage
        :return: List[MiniboxFile]
        """
        pass


class ObjectStoreInterface:
    """
    The ObjectStore interface
    """
    
    def save(self, obj):
        """
        Store the given object and return its unique id inside the storage

        :param obj: the obj to store
        :return: Unique obj id
        """
        pass

    def load(self, obj_id):
        """
        Return the object identified by the given obj_id

        :param obj_id: unique object id
        :return: the object, None if not found
        """
        pass

    def delete(self, obj_id):
        """
        Delete the object with the given object id

        :param obj_id: unique object id
        :except IOError if object cannot be deleted
        """
        pass