from abc import ABC, abstractmethod

from modules.utils.vector import *

"Changes Made: Abid Jeem"

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

class PointLight(AbstractLight):
    def __init__(self,position, color):
        super().__init__(color)
        self.position = vec(position)
        
    def getVectorToLight(self, point):
        #The light's position minus the point on the sphere
        return normalize(self.position-point)
    
    def getDistance(self, point):
        return posDot(self.position-point, self.position-point) **0.5
    
class DirectionLight(AbstractLight):
    def __init__(self,direction, color):
        super().__init__(color)
        #Vectors dont have positions
        self.direction = normalize(vec(direction))
        
    def getVectorToLight(self, point):
        #A constant vector
        return self.direction
    
    def getDistance(self, point):
        #tends to infinity
        return np.inf