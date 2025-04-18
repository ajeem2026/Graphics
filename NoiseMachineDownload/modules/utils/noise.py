"""
Author: Liz Matthews, Geoff Matthews
Noise manager class
"""

import numpy as np
from .vector import smerp, lerp
from .definitions import COLORS


class NoiseMachine:
    def __init__(self,
                 noctaves=5,
                 octaveDilation=2,
                 minimum=0,
                 maximum=1,
                 nvalues=256,
                 seed=1234):
        self.noctaves = noctaves
        self.octaveDilation = octaveDilation
        self.nvalues = nvalues
        self.values = np.linspace(minimum, maximum, nvalues)
        self.permutations = np.arange(0, nvalues, 1)
        np.random.seed(seed)
        np.random.shuffle(self.values)
        np.random.shuffle(self.permutations)

    # One-dimensional noise
    def intNoise(self, i):
        return self.values[int(i) % self.nvalues]

    def smerpNoise(self, x):
        a = self.intNoise(np.floor(x))
        b = self.intNoise(np.ceil(x))
        xFrac = x - np.floor(x)
        return smerp(a, b, xFrac)

    def noise(self, x):
        s = 0.0
        for i in range(self.noctaves):
            s += self.smerpNoise(x*self.octaveDilation**i)/2**i
        return s*0.5

    # Two-dimensional noise
    def intNoise2d(self, i, j):
        """Given i and j, return a pseudo-random value.
        Uses permutations to shift i/j."""
        a = self.permutations[j % self.nvalues]
        b = self.permutations[(i + a) % self.nvalues]
        return self.values[b % self.nvalues]

    def smerpNoise2d(self, x, y):
        """Smoothly interpolate given two dimensional points."""
        i = int(np.floor(x))
        j = int(np.floor(y))
        xFrac = x-i
        yFrac = y-j

        # randoms at four corners:
        n00 = self.intNoise2d(i, j)
        n10 = self.intNoise2d(i+1, j)
        n01 = self.intNoise2d(i, j+1)
        n11 = self.intNoise2d(i+1, j+1)

        # smerp along x
        nx0 = smerp(n00, n10, xFrac)
        nx1 = smerp(n01, n11, xFrac)
        # smerp along y
        return smerp(nx0, nx1, yFrac)

    def noise2d(self, x, y):
        """Cumulative noise at x and y using smerp."""
        s = 0.0
        for i in range(self.noctaves):
            s += self.smerpNoise2d(x*self.octaveDilation**i,
                                   y*self.octaveDilation**i)/2**i
        return s*0.5

    def noise2dTiled(self, x, y, xMod, yMod):
        """Cumulative noise at x and y using smerp, tilable."""
        s = 0.0
        for i in range(self.noctaves):
            s += self.smerpNoise2dTiled(x*self.octaveDilation**i,
                                        y*self.octaveDilation**i,
                                        xMod*self.octaveDilation**i,
                                        yMod*self.octaveDilation**i)/2**i
        return s*0.5

    def smerpNoise2dTiled(self, x, y, xMod, yMod):
        """Smoothly interpolate given two dimensional points, tilable."""
        i = int(np.floor(x))
        j = int(np.floor(y))
        xFrac = x-i
        yFrac = y-j

        # randoms at four corners:
        n00 = self.intNoise2d(i % xMod,     j % yMod)
        n10 = self.intNoise2d((i+1) % xMod,     j % yMod)
        n01 = self.intNoise2d(i % xMod, (j+1) % yMod)
        n11 = self.intNoise2d((i+1) % xMod, (j+1) % yMod)

        # smerp along x
        nx0 = smerp(n00, n10, xFrac)
        nx1 = smerp(n01, n11, xFrac)
        # smerp along y
        return smerp(nx0, nx1, yFrac)


class NoisePatterns(object):
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = NoisePatterns()
        return cls._instance

    def __init__(self):
        self.noiseId = 0
        self.scale = 50
        self.nms = [NoiseMachine(seed=i) for i in range(5)]

    def next(self):
        self.noiseId += 1
        self.noiseId %= len(self.nms)

    def previous(self):
        self.noiseId -= 1
        self.noiseId %= len(self.nms)

    def clouds(self, x, y,
               c1=COLORS["blue"], c2=COLORS["white"]):
        noise = self.nms[self.noiseId].noise2d(x, y)
        return lerp(c1, c2, noise)

    # TODO: Create a cloudsTiled() function

    def cloudsTiled(self, x, y, xMod, yMod, c1=COLORS["blue"], c2=COLORS["white"]):
        """Cumulative noise at x and y using smerp, tilable."""
        noise = self.nms[self.noiseId].noise2dTiled(x,y, xMod, yMod)
        return lerp(c1, c2, noise)
    
    # TODO: Create a marble() function
    
    def marble(self, x, y, c1=COLORS["marble1"], c2=COLORS["marble2"], noiseStrength=0.2):
        """Cumulative noise at x and y using smerp, tilable."""
        
        #At a given x and y, obtain a noise2d() value
        noise = self.nms[self.noiseId].noise2d(x,y)
        
        #Then calculate the sine of x + y + noise * noiseStrength * scale to obtain a value between -1 and +1
        
        sine= np.sin(x + y + noise * noiseStrength * self.scale)
        
        #Adjust the result to be a value between 0 and 1 and use the value to linearly interpolate between c1 and c2
        
        normalised= (sine+1)/2
        
        return lerp(c1, c2, normalised)
    
    # TODO: Create a wood() function
    
    def wood(self, x, y, c1=COLORS["wood1"], c2=COLORS["wood2"], noiseStrength=0.2):
        """Cumulative noise at x and y using smerp, tilable."""
        #At a given x and y, obtain a noise2d() value
        noise = self.nms[self.noiseId].noise2d(x,y)
        
        #Calculate the radius value as the square-root of x squared plus y squared, then multiply by 10
        
        radius= np.sqrt(x**2 + y**2)*10
        
        #Then calculate the sine of radius + noise * noiseStrength * scale to obtain a value between -1 and +1
        
        sine= np.sin(radius+ noise * noiseStrength * self.scale)
        
        #Adjust the result to be a value between 0 and 1 and use the value to linearly interpolate between c1 and c2
        
        normalised= (sine+1)/2
        
        return lerp(c1, c2, normalised)


    # TODO: Create a fire() function
    
    def fire(self, x, y, c1=COLORS["red"], c2=COLORS["yellow"], noiseStrength=0.8):
        """Cumulative noise at x and y using smerp, tilable."""
        y = y / 2
       
        #To calculate the fire shape, get the color by obtaining a noise2d() value at x*2 and y*2 and using the noise to interpolate between c1 and c2
        noise = self.nms[self.noiseId].noise2d(x*2,y*2)
        
        initial_color= lerp(c1, c2, noise)
        
        #Calculate a radius about a midpoint by np.sqrt((x-xMiddle)**2 + (y-yMiddle)**2)/4. Set the midpoint to 4, 3.
        xMiddle= 4
        yMiddle=3
        radius= np.sqrt((x-xMiddle)**2 + (y-yMiddle)**2)/4
        
        #======== For the wiggles ======================
        
        #For the wiggles, obtain a new noise2d() at x + sine(y * 2) * 0.5, y
        newNoise= self.nms[self.noiseId].noise2d(x+np.sin(y*2)*0.5,y)
        
        #Increase the radius value from before by (noise - 0.5) * noiseStrength.
        
        radius+= (newNoise - 0.5) * noiseStrength
        
        #Then calculate a color multiplier s as 1.0 - smerp(0.1, 1.0, radius)
        
        s= 1.0 - smerp(0.1, 1.0, radius)
        
        return initial_color*s