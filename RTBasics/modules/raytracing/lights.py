from abc import ABC, abstractmethod

class AbstractLight(ABC):
    def __init__(self, color):
        self.color = color
    
    def getColor(self):
        """Returns the color of the light"""
        return self.color
        
    @abstractmethod
    def getVectorToLight(self, point):
        """Returns a vector pointing towards the light"""
        pass
    
    @abstractmethod
    def getDistance(self, point):
        """Returns the distance to the light"""
        pass
        