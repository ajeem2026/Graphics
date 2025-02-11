from ..utils.vector import normalize, vec

#Rays here are just glorified struct 
#Rays always normalize their direction 

#Ray has Vector Properties: (Position & Direction)
class Ray(object):
    def __init__(self, position, direction):
        self.position = vec(position)
        self.direction = normalize(vec(direction))

    def __repr__(self):
        return "Ray: " + repr(self.position) + repr(self.direction)
    
    def __str__(self):
        return repr(self)
    
    #Given a scalar t, what would that position be? 
    #Calculations gives us scalar T--> NOT THE ACTUAL POSITION
    #We use this to find position 
    def getPositionAt(self, distance):
        return self.position + distance * self.direction

if __name__ == "__main__":
    r = Ray((2,0,0),(-1,0,0))
    r2 = Ray((22,33,44), (-22,-33,-44))
    print(r)
    print(r2)
