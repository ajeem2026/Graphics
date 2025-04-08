"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

import numpy as np


class Matrix(object):
    @staticmethod
    def makeIdentity():
        return np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]).astype(float)
    
    @staticmethod
    def makeTranslation(x, y, z):    
        return np.array([[1, 0, 0, x],
                         [0, 1, 0, y],
                         [0, 0, 1, z],
                         [0, 0, 0, 1]]).astype(float)
    
    @staticmethod
    def makeRotationX(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[ 1, 0, 0, 0],
                         [ 0, c,-s, 0],
                         [ 0, s, c, 0],
                         [ 0, 0, 0, 1]]).astype(float)
    
    @staticmethod
    def makeRotationY(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[ c, 0, s, 0],
                         [ 0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [ 0, 0, 0, 1]]).astype(float)
    
    @staticmethod
    def makeRotationZ(angle):
        c = np.cos(angle)
        s = np.sin(angle)
        return np.array([[ c, -s, 0, 0],
                         [ s,  c, 0, 0],
                         [ 0,  0, 1, 0],
                         [ 0,  0, 0, 1]]).astype(float)
    
    def makeRotation(angleX, angleY, angleZ):
        return Matrix.makeRotationZ(angleZ) @ \
               Matrix.makeRotationY(angleY) @ \
               Matrix.makeRotationX(angleX)

    @staticmethod
    def makeScale(s):
        return np.array([[ s, 0, 0, 0],
                         [ 0, s, 0, 0],
                         [ 0, 0, s, 0],
                         [ 0, 0, 0, 1]]).astype(float)
    
    def makeScaleAsymmetric(sx, sy, sz):
        return np.array([[ sx,  0,  0, 0],
                         [  0, sy,  0, 0],
                         [  0,  0, sz, 0],
                         [  0,  0,  0, 1]]).astype(float)
   
    @staticmethod
    def makePerspective(angleOfView=60, aspectRatio=1, near=0.1, far=1000):
        a = angleOfView * np.pi / 180.0
        d = 1.0 / np.tan(a/2)
        r = aspectRatio
        b = (far + near) / (near - far)
        c =   2*far*near / (near - far)
        return np.array([[d/r, 0, 0, 0],
                         [  0, d, 0, 0],
                         [  0, 0, b, c],
                         [  0, 0,-1, 0]]).astype(float)
                 
    @staticmethod
    def inverse(matrix):
        return np.linalg.inv(matrix)
    
    @staticmethod
    def applyMatrix(transform, matrix, localCoord=True):
        """Apply matrix to the transform given."""
        if localCoord:
            transform = transform @ matrix
        else:
            transform = matrix @ transform
        
        return transform
    
    @staticmethod
    def translate(transform, x,y,z, localCoord=True):
        m = Matrix.makeTranslation(x,y,z)
        return Matrix.applyMatrix(transform, m, localCoord)
    
    @staticmethod   
    def rotateX(transform, angle, localCoord=True):
        m = Matrix.makeRotationX(angle)
        return Matrix.applyMatrix(transform, m, localCoord)
    
    @staticmethod    
    def rotateY(transform, angle, localCoord=True):
        m = Matrix.makeRotationY(angle)
        return Matrix.applyMatrix(transform, m, localCoord)
    
    @staticmethod    
    def rotateZ(transform, angle, localCoord=True):
        m = Matrix.makeRotationZ(angle)
        return Matrix.applyMatrix(transform, m, localCoord)
    
    @staticmethod
    def rotate(transform, angleX, angleY, angleZ, localCoord=True):
        m = Matrix.makeRotation(angleX, angleY, angleZ)
        return Matrix.applyMatrix(transform, m, localCoord)
    
    @staticmethod   
    def scale(transform, s, localCoord=True):
        m = Matrix.makeScale(s)
        return Matrix.applyMatrix(transform, m, localCoord)
    
    @staticmethod
    def scaleAsymmetric(transform, sx, sy, sz, localCoord=True):
        m = Matrix.makeScaleAsymmetric(sx, sy, sz)
        return Matrix.applyMatrix(transform, m, localCoord)
    