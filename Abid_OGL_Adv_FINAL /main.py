"""
Author: Liz Matthews
Code modified from Developing Graphics Frameworks
  with Python and OpenGL by Lee Stemkoski and
  Michael Pascale.
"""

from modules.oGL.base import Base
from modules.renderer import Renderer
from modules.objects import Scene, Camera, MovingMesh, AxesHelper, GridHelper, Mesh
from modules.geometry import *
from modules.movementRig import MovementRig
from modules.materials import SurfaceMaterial
from modules.materials.bumpMap import BumpMaterial

from modules.objects.light import DirectionalLight, Light, PointLight
from modules.materials.phong import PhongMaterial
from modules.objects.world import Group

from modules.materials.texMaterial import TextureMaterial
from modules.oGL.texture import Texture


import pygame
import numpy as np

class Main(Base):
    def handleOtherInput(self, event):
        self.rig.handleOtherInput(event, self.deltaTime)
                
    def initialize(self):        
        
        
        print("Initializing program...")
        
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        


        
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspectRatio=self.aspectRatio)
        
        self.rig = MovementRig()
        self.rig.add(self.camera)
        

        
        # The following does not work until part 2 is completed
        
        self.rig.setPosition([1, 1, 4])
        self.scene.add(self.rig)
        
        axes = AxesHelper(axisLength=2)
        self.scene.add( axes )
        grid = GridHelper(size=20, gridColor=[1,1,1],
        centerColor=[1,1,0])
        grid.setRotateX(-np.pi/2)
        self.scene.add(grid)
        
    
    
    
    #===============================================

    #for the dice
        dice = DiceGeometry(width=2, height=2, depth=2)
        dice_texture = TextureMaterial(Texture("./textures/d6.png"))
        mesh = MovingMesh(dice, dice_texture)
        #mesh.setRotVel((0.0337, 0.0514, 0))
        mesh.setPosition([0,1,0])
 
        self.scene.add(mesh)
        

    #===============================================
    #bump mapping

        bump_material = Texture("./textures/jewels_normal.png")
        usual_material = Texture("./textures/jewels.png")
        bump_map = BumpMaterial(usual_material, bump_material)

        sphere = SphereGeometry()
        mesh = MovingMesh(sphere, bump_map)
        mesh.setRotVel((0.0337, 0.0514, 0))
        mesh.setPosition([0,3,-8])
        self.scene.add(mesh)
        
        
        
    #for the box
        box = BoxGeometry(width=2, height=2, depth=2)
        box_texture = TextureMaterial(Texture("./textures/cobble.png"))
        mesh = MovingMesh(box, box_texture)
        #mesh.setRotVel((0.0337, 0.0514, 0))
        mesh.setPosition([0,1,-8])
 
        self.scene.add(mesh)
        
    #=======sphere and box on other end
        #disco ball sphere
        geometry = SphereGeometry(radius=1, colorFunction=None)
        earth_texture = TextureMaterial(Texture("./textures/purpleGrid.png"))

        mesh = MovingMesh(geometry, earth_texture)
        mesh.setRotVel((0.0337, 0.0514, 0))
        mesh.setPosition([0,3,8])
        self.scene.add(mesh)
        
        
        
    #for the box
        box = BoxGeometry(width=2, height=2, depth=2)
        box_texture = TextureMaterial(Texture("./textures/bricks.png"))
        mesh = MovingMesh(box, box_texture)
        #mesh.setRotVel((0.0337, 0.0514, 0))
        mesh.setPosition([0,1,8])
 
        self.scene.add(mesh)
        
        
        
        # bump_material = Texture("./textures/earth_normal.png")
        # usual_material = Texture("./textures/earth_daymap.jpg")
        # bump_map = BumpMaterial(usual_material, bump_material)

        # sphere = SphereGeometry()
        # mesh = MovingMesh(sphere, bump_map)
        # mesh.setRotVel((0.0337, 0.0514, 0))
        # mesh.setPosition([-8,8,-4])
        # self.scene.add(mesh)
        
        
        #=======================DONUTTTTTTT==============================
        #extra cREDIT:
        
        torus = TorusGeometry(majorRadius=1.0, minorRadius=0.3, uResolution=64, vResolution=32)
        material = SurfaceMaterial({"useVertexColors": True, "doubleSide":True} )
        mesh = MovingMesh(torus, material)
        mesh.setPosition([0, 4, 0])
        mesh.setRotVel((0.05, 0.1, 0.03))
        self.scene.add(mesh)

        #========================
        
        
        #random rainbow sphere
        geometry = SphereGeometry(radius=1.5, colorFunction=rainbowGradient)
        material = SurfaceMaterial({"useVertexColors" : True,
                                    "doubleSide"      : True})
        mesh = MovingMesh(geometry, material)
        mesh.setRotVel((0.0337, 0.0514, 0))
        mesh.setPosition([8,2,0])
        self.scene.add(mesh)
        
        
        #earth sphere
        geometry = SphereGeometry(radius=1.5, colorFunction=None)
        earth_texture = TextureMaterial(Texture("./textures/earth_daymap.jpg"))

        mesh = MovingMesh(geometry, earth_texture)
        mesh.setRotVel((0.002, 0.05, 0))
        mesh.setPosition([-8,2,0])
        self.scene.add(mesh)
        
        
        
        geometry = SphereGeometry()
        material = PhongMaterial({"useVertexColors" : False,
                                   "useFaceNormals" : True})
        
        self.light = DirectionalLight(color=vec(1, 1, 1),
                                 direction=vec(0,1,0))
        
        self.scene.add(self.light)
        
    #===============================================

    #for part-2 
    #skysphere
        sky_sphere = SphereGeometry(radius=100)
        sky_texture = TextureMaterial(Texture("./textures/sunflowers_puresky.jpg"),{"doubleSide": True, "wireframe": False, "useVertexColors": False})
        sky_mesh = Mesh(sky_sphere, sky_texture)
        sky_mesh.position = [0,0,0]
        self.scene.add(sky_mesh)
        
      #===============================================
        
        
        print("Initialization done!")
        
        
    def update(self):
        """Most of the work is in scene, rig, and renderer!"""
        
        self.scene.update(self.deltaTime)
        self.rig.update(self.deltaTime)
        self.renderer.render( self.scene, self.camera)
        
if __name__ == '__main__':
    Main(fullScreen=True).run()
