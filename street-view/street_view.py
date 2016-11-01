#!/usr/bin/env python

import sys

from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase, LVecBase3f
from direct.task.Task import Task
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

    """

    def __init__(self):
        # Configure the parallax mapping settings (these are just the defaults)
        loadPrcFileData("", "parallax-mapping-samples 3\n"
                            "parallax-mapping-scale 0.1")

        ShowBase.__init__(self)

        # Post the instructions
        self.title = addTitle("StreetView")
        self.inst1 = addInstructions(0.06, "ESC - wyjście")
        self.inst2 = addInstructions(0.12, "Porusz myszą by obrócić kamerę")
        self.inst3 = addInstructions(0.18, "LPM: Ruch w przód")
        self.inst4 = addInstructions(0.24, "PPM: Ruch do tyłu")
        self.inst5 = addInstructions(0.30, "1: Ustaw kamerę w pozycji 0")

        axes_texture = self.loader.loadTexture("maps/TextureMap.tif")
        self.axes = self.loader.loadModel("models/Axes.egg")
        self.axes.setTexture(axes_texture)
        self.axes.reparentTo(self.render)
        self.axes.setScale(5, 5, 5)
        self.axes.setPos(0, 0.1, 0)

        # Rozmiar ściany to (1x0x1) * skala
        myTexture = self.loader.loadTexture("images/image13.jpg")
        self.wall = self.loader.loadModel('models/Square.egg')
        self.wall.reparentTo(self.render)
        self.wall.setTexture(myTexture)
        self.wall.setScale(10, 10, 10)
        self.wall.setPos(-50, 0, 15)

        self.wall2 = self.wall
        self.wall2.reparentTo(self.render)
        self.wall2.setScale(5, 5, 5)

        # Make the mouse invisible, turn off normal mouse controls
        self.disableMouse()
        point1 = LVecBase3f(0.0, 10.0, 10.0)

        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)
        self.camLens.setFov(60)

        # Set the current viewing target
        self.focus = LVector3(0, 50, 0)  # First camera position
        self.heading = 180
        self.pitch = 0
        self.mousex = 0
        self.mousey = 0
        self.last = 0
        self.mousebtn = [0, 0, 0]

        # Start the camera control task:
        taskMgr.add(self.controlCamera, "camera-task")
        self.accept("escape", sys.exit, [0])
        self.accept("mouse1", self.setMouseBtn, [0, 1])
        self.accept("mouse1-up", self.setMouseBtn, [0, 0])
        self.accept("mouse2", self.setMouseBtn, [1, 1])
        self.accept("mouse2-up", self.setMouseBtn, [1, 0])
        self.accept("mouse3", self.setMouseBtn, [2, 1])
        self.accept("mouse3-up", self.setMouseBtn, [2, 0])
        self.accept("arrow_left", self.rotateCam, [-1])
        self.accept("arrow_right", self.rotateCam, [1])
        self.accept("1-up", self.changeCameraPos, [LVector3(0, 0, 0)])

    def setMouseBtn(self, btn, value):
        self.mousebtn[btn] = value

    def rotateCam(self, offset):
        self.heading = self.heading - offset * 10

    def changeCameraPos(self, focus):
        self.focus = focus

    def controlCamera(self, task):
        # figure out how much the mouse has moved (in pixels)
        md = self.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if self.win.movePointer(0, 100, 100):
            self.heading = self.heading - (x - 100) * 0.2
            self.pitch = self.pitch - (y - 100) * 0.2
        if self.pitch < -45:
            self.pitch = -45
        if self.pitch > 45:
            self.pitch = 45
        self.camera.setHpr(self.heading, self.pitch, 0)
        dir = self.camera.getMat().getRow3(1)
        elapsed = task.time - self.last
        if self.last == 0:
            elapsed = 0
        if self.mousebtn[0]:
            self.focus = self.focus + dir * elapsed * 30
        if self.mousebtn[1] or self.mousebtn[2]:
            self.focus = self.focus - dir * elapsed * 30
        self.camera.setPos(self.focus - (dir * 5))
        if self.camera.getX() < -59.0:
            self.camera.setX(-59)
        if self.camera.getX() > 59.0:
            self.camera.setX(59)
        if self.camera.getY() < -59.0:
            self.camera.setY(-59)
        if self.camera.getY() > 59.0:
            self.camera.setY(59)
        if self.camera.getZ() < 5.0:
            self.camera.setZ(5)
        if self.camera.getZ() > 45.0:
            self.camera.setZ(45)
        self.focus = self.camera.getPos() + (dir * 5)
        self.last = task.time
        return Task.cont


if __name__ == '__main__':
    engine = StreetView()
    engine.run()
