"""
Author: Liz Matthews
Code modified from
  https://medium.com/swlh/ray-tracing-from-scratch-in-python-41670e6a96f9
"""

from ..oGL.attribute import Attribute
from ..utils.vector import *
from ..utils.definitions import *

import numpy as np

class AbstractGeometry(object):
    """Abstract geometry which sets up attributes,
       applies matrices, merge with other geometry,
       and count vertices."""
       
    def __init__(self):
        self.attributes = {}        
        self.vertexCount = None
    
    def addAttribute(self, dataType, variableName, data):            
        self.attributes[variableName] = Attribute(dataType, data)
       
    def countVertices(self):
        """Separate counting method so that merge()
           can work.
        
           The number of vertices may be calculated from
           the length of any Attribute object's array
           of data."""
           
        attrib = list(self.attributes.values())[0]
        self.vertexCount = len(attrib.data)
        
    def uploadData(self):
        for attrib in self.attributes.values():
            attrib.uploadData()
    
    def applyMatrix(self, matrix, variableName="vertexPosition"):
        """Applies a transformation matrix to itself."""
        
        oldPositionData = self.attributes[variableName].data
        newPositionData = []
        for oldPos in oldPositionData:
            newPos = oldPos.copy()
            
            # Add homogeneous fourth coordinate, multiply,
            #  and remove 4th coord
            newPos.append(1)
            newPos = matrix @ newPos
            newPos = list(newPos[0:3])
            
            # Add to new data list
            newPositionData.append(newPos)
            self.attributes[variableName].data = newPositionData
            
            rotationMatrix = np.array(matrix)[:3, :3]
            self.applyRotationToNormals(rotationMatrix)
            
            # New data must be uploaded
            #self.attributes[variableName].uploadData()
            
            
    def applyRotationToNormals(self, rotationMatrix):
        
        """Apply rot matrix to vertex and face normal"""

        def transform_normals(normal_data):
            return [rotationMatrix @ normal for normal in normal_data]

        if "vertexNormal" in self.attributes:
            self.attributes["vertexNormal"].data = transform_normals(
                self.attributes["vertexNormal"].data
            )

        if "faceNormal" in self.attributes:
            self.attributes["faceNormal"].data = transform_normals(
                self.attributes["faceNormal"].data
            )
    
    
    def merge(self, otherGeometry):
        for variableName, attributeObject in self.attributes.items():
            attributeObject.data += otherGeometry.attributes[variableName].data
            
            # New data must be uploaded
            attributeObject.uploadData()
            
        # Update the number of vertices
        self.countVertices()
        
