# cf https://www.youtube.com/watch?v=tVF62GoJ8dA
# Kain character: https://free3d.com/3d-model/kain-77272.html

import maya.cmds as cmds
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import json
from PySide2 import QtGui, QtCore, QtWidgets

def getMayaWindow():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

class Synoptic(QtWidgets.QDialog):
    def __init__(self, title='Synoptic window'):
        super(Synoptic, self).__init__(getMayaWindow(), QtCore.Qt.Window)

        self.setWindowTitle(title)

        color = QtGui.QColor(255, 243, 49)
        hoveredColor = QtGui.QColor(0, 255, 100)
        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setColor(color)
        self.hoveredPen = QtGui.QPen()
        self.hoveredPen.setWidth(2)
        self.hoveredPen.setColor(hoveredColor)
        self.brush = QtGui.QBrush(color)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView()
        self.view.setScene(self.scene)

        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

        with open('C:/agr/perso/dev/maya/kain.json', 'r') as f:
            self.data = json.load(f)

        self.refreshAll()

    def addImage(self, src):
        pixmap = QtGui.QPixmap(src)
        self.scene.addPixmap(pixmap)

    def addSelectionButtons(self, controls):
        for ctrl in controls:
            SelectionButton(self, ctrl['x'], ctrl['y'], ctrl['name'], ctrl['size'])

    def addControlPanel(self):
        self.controlPanel = ControlPanel(self, QtCore.Qt.Horizontal)

    def refreshAll(self):
        self.scene.clear()
        self.addImage(self.data['background'])
        self.addSelectionButtons(self.data['controls'])
        self.addControlPanel()

class ControlPanel(QtWidgets.QGroupBox):
    def __init__(self, parent, orientation, name='Parameter'):
        super(ControlPanel, self).__init__(name, parent)
        self.name = name
        self.slider = QtWidgets.QSlider(orientation)
        slidersLayout = QtWidgets.QVBoxLayout()
        slidersLayout.addWidget(self.slider)
        self.setLayout(slidersLayout)
        parent.layout.addWidget(self)

class SelectionButton(QtWidgets.QGraphicsItem):
    def __init__(self, parent, x=0, y=0, name=None, size='big'):
        super(SelectionButton, self).__init__()
        self.parent = parent
        sizePx = 20 if size == 'small' else 30 if size == 'medium' else 40
        self.globalRect = QtCore.QRectF(0, 0, sizePx, sizePx)
        self.setPos(x, y)
        self.parent.scene.addItem(self)
        self.setAcceptHoverEvents(1)
        self.hovered = False
        self.selected = False
        self.name = name
        self.sJob = cmds.scriptJob(event=['SelectionChanged', self.updateSelection])

    def __del__(self):
        cmds.scriptJob(kill=self.sJob)

    def updateSelection(self):
        selection = cmds.ls(sl=True) or []
        selected = self.name in selection
        if self.selected != selected:
            self.selected = selected
            self.update()

    def boundingRect(self):
        return self.globalRect

    def paint(self, painter, option, widget):
        if self.hovered or self.selected:
            painter.setPen(self.parent.hoveredPen)
        else:
            painter.setPen(self.parent.pen)
        if self.selected:
            painter.setBrush(self.parent.brush)
        painter.drawEllipse(self.globalRect)

    def hoverEnterEvent(self, event):
       self.hovered = True
       self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        selected = self.selected
        if self.name:
            cmds.select(self.name)
            self.parent.controlPanel.init(self.name)
        if selected:
            cmds.setAttr(self.name+'.rotateY', 50)

window = Synoptic()
window.show()
