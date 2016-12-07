#!/usr/bin/env python

import sys
import math

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import LPoint3, LVector3
from panda3d.core import TextNode
from panda3d.core import WindowProperties
from panda3d.core import loadPrcFileData

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)


# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1, 1, 1, 1), scale=.08,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))


class StreetView(ShowBase):
    """
    Position
    (right, forward, up)
    Hpr
    (heading, pitch, roll) - degrees
    We change only heading to move our walls.
    +1 - move towards 'forward' axis
    -1 - move towards 'right' axis

    """

    def __init__(self):
        # Configure the parallax mapping settings (these are just the defaults)
        loadPrcFileData("", "parallax-mapping-samples 3\n"
                            "parallax-mapping-scale 0.1")

        ShowBase.__init__(self)

        self.camera_z = 100
        self.camera_default_z = 100
        self.level_height = 100
        self.level_number = 1

        # Post the instructions
        self.title = addTitle("StreetView")
        self.inst1 = addInstructions(0.06, "ESC - wyjście")
        self.inst2 = addInstructions(0.12, "1: Ustaw kamerę we wcześniejszym węźle.")
        self.inst3 = addInstructions(0.18, "2: Ustaw kamerę w następnym węźle.")
        self.inst4 = OnscreenText(text="Numer punktu: 1", style=1, fg=(1, 1, 1, 1), scale=.05,
                                  shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                                  pos=(0.08, -0.24 - 0.04), align=TextNode.ALeft)

        axes_texture = self.loader.loadTexture("maps/TextureMap.tif")
        self.axes = self.loader.loadModel("models/Axes.egg")
        self.axes.setTexture(axes_texture)
        self.axes.reparentTo(self.render)
        self.axes.setScale(5, 5, 5)
        self.axes.setPos(0, 0.1, 0)

        self.number_of_points = 5
        # for i in range(1, self.number_of_points + 1, 1):
        #     positions = [(0, 0, self.level_height * i), (30, 0, self.level_height*i), (60, 0, self.level_height*i)]
        #     index = 0
        #     # positions = [(0, 0, self.level_height * i), (0, 60, self.level_height * i), (60, 120, self.level_height * i)]
        #     photo_numbers = [1, 2, 3]
        #     for position_vector in positions:
        #         # myTexture = self.loader.loadTexture("images/img" + str(number_of_photo) + ".jpg")
        #         myTexture = self.loader.loadTexture("images/out" + str(3-index%2) + ".jpg")
        #         index += 1
        #         self.wall = self.loader.loadModel('models/Square.egg')
        #         self.wall.reparentTo(self.render)
        #         self.wall.setTexture(myTexture)
        #         # self.wall.setScale(10, 10, 10)
        #         self.wall.setScale(10,10,10)
        #         self.wall.setPos(position_vector)
        for i in range(1, self.number_of_points + 1, 1):
            # obrót obrazka wokół osi Z
            # self.wall.setHpr(kąt_obrotu,0,0)
            walls_number = 18
            szerokosc = 32.75
            kat = 360/walls_number
            katRad = math.radians(kat)
            R = szerokosc/(2*math.tan(katRad/2))

            # for j in range(walls_number, 0, -1):
            #     myTexture = self.loader.loadTexture("sklejanie/images/stiched/" + str(j) + ".jpg")
            #     self.wall = self.loader.loadModel('models/Square.egg')
            #     self.wall.reparentTo(self.render)
            #     self.wall.setTexture(myTexture)
            #     # self.wall.setScale(10, 10, 10)
            #     self.wall.setScale(10, 10, 10)

            for j in range(1, walls_number+1, 1):
                myTexture = self.loader.loadTexture("sklejanie/images/stiched/" + str(j) + ".jpg")
                self.wall = self.loader.loadModel('models/Square.egg')
                self.wall.reparentTo(self.render)
                self.wall.setTexture(myTexture)
                # self.wall.setScale(10, 10, 10)
                self.wall.setScale(10, 10, 10)

                angle = j*kat
                angleRad = math.radians(-angle)
                x = R*math.cos(angleRad)
                y = R*math.sin(angleRad)

                #self.wall.setPos(szerokosc - (1 - math.cos(katRad)) * szerokosc / 2, math.sin(katRad) * szerokosc / 2, self.level_height * i)
                self.wall.setPos(x, y, self.level_height * i)
                self.wall.setHpr(90-angle, 0, 0)



        # Rozmiar ściany to (1x0x1) * skala

        # self.wall.reparentTo(self.render)
        # self.wall.setScale(5, 5, 5)

        # Make the mouse invisible, turn off normal mouse controls
        self.disableMouse()

        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
        self.camLens.setFov(60)

        # Set the current viewing target
        self.focus = LVector3(0, 0, 0)  # First camera position
        self.heading = 180
        self.pitch = 0
        self.mousex = 0
        self.mousey = 0
        self.last = 0
        self.mousebtn = [0, 0, 0]

        self.h = 0
        self.p = 0
        self.r = 0

        # Start the camera control task:
        taskMgr.add(self.controlCamera, "camera-task")
        self.changeCameraPos(-1)
        self.accept("escape", sys.exit, [0])

        # DO USUNIECIA
        self.accept("mouse1", self.setMouseBtn, [0, 1])
        self.accept("mouse1-up", self.setMouseBtn, [0, 0])
        self.accept("mouse2", self.setMouseBtn, [1, 1])
        self.accept("mouse2-up", self.setMouseBtn, [1, 0])
        self.accept("mouse3", self.setMouseBtn, [2, 1])
        self.accept("mouse3-up", self.setMouseBtn, [2, 0])
        #####

        self.accept("arrow_left", self.rotateCam, [-1])
        self.accept("arrow_right", self.rotateCam, [1])
        self.accept("1-up", self.changeCameraPos, [-1])
        self.accept("2-up", self.changeCameraPos, [1])

        # Rotating walls
        # self.accept("q-up", self.change_h, [5])
        # self.accept("w-up", self.change_h, [-5])
        # self.accept("a-up", self.change_p, [5])
        # self.accept("s-up", self.change_p, [-5])
        # self.accept("z-up", self.change_r, [5])
        # self.accept("x-up", self.change_r, [-5])

    def change_h(self, value):
        self.h += value

    def change_p(self, value):
        self.p += value

    def change_r(self, value):
        self.r += value

    def setMouseBtn(self, btn, value):
        self.mousebtn[btn] = value

    def rotateCam(self, offset):
        self.heading = self.heading - offset * 10

    def changeCameraPos(self, up_or_down):
        if self.camera_z == self.camera_default_z and up_or_down == -1:
            self.focus = LVector3(0, 0, self.camera_z)
            return
        if self.camera_z == self.level_height * self.number_of_points and up_or_down == 1:
            self.focus = LVector3(0, 0, self.camera_z)
            return
        self.camera_z += up_or_down * self.level_height
        self.level_number += up_or_down
        self.focus = LVector3(0, 0, self.camera_z)
        self.inst4.setText("Numer punktu: " + str(self.level_number))

    def controlCamera(self, task):
        # DO USUNIECIA
        # figure out how much the mouse has moved (in pixels)
        md = self.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if self.win.movePointer(0, 100, 100):
            self.heading = self.heading - (x - 100) * 0.2
            self.pitch = self.pitch - (y - 100) * 0.2
        #######

        self.camera.setHpr(self.heading, self.pitch, 0)
        self.wall.setHpr(self.h, self.p, self.r) # Rotating walls
        dir = self.camera.getMat().getRow3(1)
        elapsed = task.time - self.last
        if self.last == 0:
            elapsed = 0
        if self.mousebtn[0]:
            self.focus = self.focus + dir * elapsed * 30
        if self.mousebtn[1] or self.mousebtn[2]:
            self.focus = self.focus - dir * elapsed * 30
        self.camera.setPos(self.focus - (dir * 5))
        self.focus = self.camera.getPos() + (dir * 5)
        self.last = task.time
        return Task.cont


if __name__ == '__main__':
    engine = StreetView()
    engine.run()
