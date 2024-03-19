class Backpack:
    """
    Class for Backpack - contains a list of objects
    """

    def __init__(self, max_weight):
        """
        Constructor for Backpack class
        :param max_weight: maximum weight of the Backpack
        """
        self.__objects = []
        self.__max_weight = int(max_weight)

    def add_object(self, object):
        """
        Function to adda an object to the Backpack
        :return: the added object
        """
        self.__objects.append(object)
        return object

    def del_objects(self, object):
        """
        Function to delete an object
        :param object: the object to be deleted
        :return: the deleted object
        """

        self.__objects.remove(object)
        return object

    def get_objects(self):
        """
        Function to get all objects from the Backpack
        :return: a list containing all objects from the Backpack
        """
        return self.__objects

    def get_weight(self):
        """
        Function to get the maximum weight of the Backpack
        :return: maximum weight of the Backpack
        """
        return self.__max_weight

    def set_weight(self, w):
        """
        Function to set Backpack's objects
        :param objects: new list of objects
        :return: None
        """
        self.__weight = w

    def set_objects(self, objects):
        """
        Function to set Backpack's objects
        :param objects: new list of objects
        :return: None
        """
        self.__objects = objects