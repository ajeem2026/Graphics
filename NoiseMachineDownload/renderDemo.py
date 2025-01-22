from render import ProgressiveRenderer, ShowTypes
from modules.utils.noise import NoisePatterns
from modules.utils.vector import lerp, smerp
import numpy as np
import pygame
import random


class RandomRenderer(ProgressiveRenderer):
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

    
# Calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        RandomRenderer.main()
    finally:
        pygame.quit()
