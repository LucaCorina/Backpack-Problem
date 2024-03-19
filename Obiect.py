class Obiect:
    def __int__(self):
        self.__index = 0
        self.__cost = 0
        self.greutate =0
    def __init__(self,ind, cost, weight):
        """
        Constructor for object class
        :param cost: -cost of the object
        :param weight: -weight of the object
        """
        self.__index= ind
        self.__cost = cost
        self.greutate = weight

    # Getters and setters

    def get_index(self):
        return self.__index

    def get_cost(self):
        return self.__cost

    def get_weight(self):
        return self.__weight

    def set_index(self,ind):
        self.__index=ind

    def set_cost(self, new_cost):
        self.__cost = new_cost

    def set_weight(self, new_weight):
        self.__weight = new_weight

    # Overriding __eq__
    def __eq__(self, other):
        return self.__weight == other.get_weight() and self.__cost == other.get_cost()