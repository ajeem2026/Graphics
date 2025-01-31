from abc import ABC, abstractmethod


#All ABC does is force anything that inherets from you: it has to implement getVector and getDistance
#getDistance is for point lights (distance depedns on how close you are to the point)
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
        