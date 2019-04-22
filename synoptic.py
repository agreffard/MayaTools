# cf https://www.youtube.com/watch?v=tVF62GoJ8dA

import maya.cmds as cmds
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtGui, QtCore, QtWidgets

def getMayaWindow():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

class Synoptic(QtWidgets.QDialog):
    def __init__(self, title='Synoptic window'):
        super(Synoptic, self).__init__(getMayaWindow(), QtCore.Qt.Window)

        self.setWindowTitle(title)

        color = QtGui.QColor(255, 243, 49)
        self.pen = QtGui.QPen()
        self.pen.setWidth(2)
        self.pen.setColor(color)
        self.brush = QtGui.QBrush(color)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView()
        self.view.setScene(self.scene)

        layout.addWidget(self.view)
        self.setLayout(layout)
        self.refreshAll()

    def addImage(self):
        pixmap = QtGui.QPixmap('C:/agr/perso/dev/maya/base.png')
        self.scene.addPixmap(pixmap)

    def addControls(self):
        ControlButton(self, 10, 50, 'con_r_fk_wrist')
        ControlButton(self, 80, 55, 'con_r_fk_elbow', size='medium')
        ControlButton(self, 320, 50, 'con_l_fk_wrist')
        ControlButton(self, 260, 55, 'con_l_fk_elbow', size='medium')
        ControlButton(self, 164, 5, 'con_neck')
        ControlButton(self, 164, 140, 'con_waist')
        ControlButton(self, 160, 330, 'con_IK_r_leg', size='small')
        ControlButton(self, 187, 330, 'con_IK_l_leg', size='small')

    def refreshAll(self):
        self.scene.clear()
        self.addImage()
        self.addControls()

class ControlButton(QtWidgets.QGraphicsItem):
    def __init__(self, parent, x=0, y=0, control=None, size='big'):
        super(ControlButton, self).__init__()
        self.parent = parent
        sizePx = 20 if size == 'small' else 30 if size == 'medium' else 40
        self.globalRect = QtCore.QRectF(0, 0, sizePx, sizePx)
        self.setPos(x, y)
        self.parent.scene.addItem(self)
        self.setAcceptHoverEvents(1)
        self.selected = False
        self.control = control

    def boundingRect(self):
        return self.globalRect

    def paint(self, painter, option, widget):
        if self.selected:
            painter.setBrush(self.parent.brush)
        painter.setPen(self.parent.pen)
        painter.drawEllipse(self.globalRect)

    def hoverEnterEvent(self, event):
       self.selected = True
       self.update()

    def hoverLeaveEvent(self, event):
        self.selected = False
        self.update()

    def mousePressEvent(self, event):
        if self.control:
            cmds.select(self.control)

window = Synoptic()
window.show()
