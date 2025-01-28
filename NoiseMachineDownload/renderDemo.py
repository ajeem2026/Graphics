from render import ProgressiveRenderer, ShowTypes
from modules.utils.noise import NoisePatterns
from modules.utils.vector import lerp, smerp
import numpy as np
import pygame
import random


class RandomRenderer(ProgressiveRenderer):

    # Shows how renderer is restarted
    # This is mainly for artifacts that don't look right in lower res
    def __init__(self, width=640, height=480,
                 showTime=True,
                 show=ShowTypes.PerColumn,
                 minimumPixel=0,
                 startPixelSize=256):
        """An unnecessary override but provided to show how
        to override the __init__ in future inheritance classes."""
        super().__init__(width, height,
                         showTime,
                         show,
                         minimumPixel,
                         startPixelSize)

    def getColor(self, x, y):
        """Gives a random color per pixel."""
        return np.array((random.random(),
                         random.random(),
                         random.random()))

    def handleOtherInput(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            type(self).restart()

# TODO: Create a RainbowRenderer class here
# What is color based on? x and y coord as a % of total width and height
# Horizontal %: Red component and Vertical %: Green component
# 100% - Horizontal %: Blue component


class RainbowRenderer(ProgressiveRenderer):

    # Shows how renderer is restarted
    # This is mainly for artifacts that don't look right in lower res
    def __init__(self, width=640, height=480,
                 showTime=True,
                 show=ShowTypes.PerColumn,
                 minimumPixel=0,
                 startPixelSize=256):
        """An unnecessary override but provided to show how
        to override the __init__ in future inheritance classes."""
        super().__init__(width, height,
                         showTime,
                         show,
                         minimumPixel,
                         startPixelSize)

        # Initialising each component
        self.red_mode = 0
        self.green_mode = 1
        self.blue_mode = 2

    def getColor(self, x, y):
        """Component Calculation"""

        width = self.width
        height = self.height

        # Calculations for the red component

        # For horizontal
        if self.red_mode == 0:
            red = x / width

        # For vertical

        elif self.red_mode == 1:
            red = y / height

        # For horizontal complement
        elif self.red_mode == 2:
            red = 1 - (x / width)
        # For vertical complement
        elif self.red_mode == 3:
            red = 1 - (y / height)
        else:
            red = 0

        # Calculations for the green component
        if self.green_mode == 0:
            green = x / width
        elif self.green_mode == 1:
            green = y / height
        elif self.green_mode == 2:
            green = 1 - (x / width)
        elif self.green_mode == 3:
            green = 1 - (y / height)
        else:
            green = 0

       # Calculations for the blue component
        if self.blue_mode == 0:
            blue = x / width
        elif self.blue_mode == 1:
            blue = y / height
        elif self.blue_mode == 2:
            blue = 1 - (x / width)
        elif self.blue_mode == 3:
            blue = 1 - (y / height)
        else:
            blue = 0

        return np.array((red, green, blue))

    def handleOtherInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:

                # Wraps around thanks to modulus logic
                self.red_mode = (self.red_mode + 1) % 4
                type(self).restart()
            elif event.key == pygame.K_2:
                self.green_mode = (self.green_mode + 1) % 4
                type(self).restart()
            elif event.key == pygame.K_3:
                self.blue_mode = (self.blue_mode + 1) % 4
                type(self).restart()

# TODO: Create a NoiseRenderer class here


class NoiseRenderer(ProgressiveRenderer):

    # Shows how renderer is restarted
    # This is mainly for artifacts that don't look right in lower res
    def __init__(self, width=640, height=480,
                 showTime=True,
                 show=ShowTypes.PerColumn,
                 minimumPixel=0,
                 startPixelSize=256):
        """An unnecessary override but provided to show how
        to override the __init__ in future inheritance classes."""
        super().__init__(width, height,
                         showTime,
                         show,
                         minimumPixel,
                         startPixelSize)

      # Instance Properties --------------------------------

      # An integer representing the current noise pattern id
        self.pattern_id = 0

      # Lambda documentation cited from https://realpython.com/python-lambda/

        # self.patterns = [lambda x, y: NoisePatterns.getInstance().clouds(x, y)]
        # self.patterns = [lambda x, y: NoisePatterns.getInstance().cloudsTiled(x, y,5,5)]
        # self.patterns = [lambda x, y: NoisePatterns.getInstance().marble(x, y)]
        # self.patterns = [lambda x, y: NoisePatterns.getInstance().wood(x, y)]
        # self.patterns = [lambda x, y: NoisePatterns.getInstance().fire(x, y)]
        
        self.patterns = [
            lambda x, y: NoisePatterns.getInstance().clouds(x, y),
            lambda x, y: NoisePatterns.getInstance().cloudsTiled(x, y, 3, 3),
            lambda x, y: NoisePatterns.getInstance().marble(x, y, noiseStrength=0),
            lambda x, y: NoisePatterns.getInstance().wood(x, y, noiseStrength=0 ),
            lambda x, y: NoisePatterns.getInstance().fire(x, y,noiseStrength=0.6)
        ]


      # Instance Methods ----------------------------------------------------------------

      # and a list of NoisePatterns method references.

    def getColor(self, x, y, scale=64):
        """Gives a random color per pixel."""
        # divides x and y by the scale and then calls the current method of noise.
        # While the methods in NoisePatterns return colors in 1.0 mode,
        # the progressive renderer will multiply by 255 to satisfy PyGame.

        scaled_x = x/scale
        scaled_y = y/scale

        return self.patterns[self.pattern_id](scaled_x, scaled_y)

    def handleOtherInput(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                # Wraps around thanks to modulus logic
                self.pattern_id = (self.pattern_id-1) % len(self.patterns)
                type(self).restart()
            elif event.key == pygame.K_w:
                self.pattern_id = (self.pattern_id+1) % len(self.patterns)
                type(self).restart()
            elif event.key == pygame.K_e:
                NoisePatterns.getInstance().previous()
                type(self).restart()
            elif event.key == pygame.K_r:
                NoisePatterns.getInstance().next()
                type(self).restart()


# Calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        # RandomRenderer.main()
        #RainbowRenderer.main()
        NoiseRenderer.main() 
    finally:
        pygame.quit()
