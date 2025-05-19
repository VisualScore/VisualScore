import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic

class StaffPreviewItem(QtWidgets.QGraphicsItem):
    def __init__(self, line_count=5, default_line_spacing=10, line_distance=1, width=400):
        super().__init__()
        self.line_count = line_count
        self.default_line_spacing = default_line_spacing
        self.line_distance = line_distance
        self.width = width
        self.pen = QtGui.QPen(QtCore.Qt.black, 1)

        self.height = (self.line_count - 1) * self.line_distance

    def boundingRect(self):
        height = (self.line_count - 1) * self.line_distance
        return QtCore.QRectF(0, 0, self.width, height)

    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.lightGray, 1))
        for i in range(self.line_count * self.line_distance - self.line_distance - 1):
            y = i * self.default_line_spacing
            painter.drawLine(0, y, self.width, y)

        painter.setPen(self.pen)
        for i in range(self.line_count):
            y = i * self.line_distance
            painter.drawLine(0, y, self.width, y)