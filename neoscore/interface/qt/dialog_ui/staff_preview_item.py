import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic

class StaffPreviewItem(QtWidgets.QGraphicsItem):
    def __init__(self, line_count=5, default_line_spacing=10, line_distance=1, width=400):
        super().__init__()
        self.line_count = line_count
        self.default_line_spacing = default_line_spacing
        self.line_distance = line_distance
        self.width = width

        self.line_spacing = default_line_spacing * line_distance

        self.pen = QtGui.QPen(QtCore.Qt.black, 1)

        self.height_in_spaces = (self.line_count - 1) * self.line_distance
        self.height_in_px = (self.line_count - 1) * self.line_spacing

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width, self.height_in_spaces)

    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtCore.Qt.lightGray, 1))
        for i in range(self.line_count * self.line_distance - (self.line_distance - 1)):
            y = i * self.default_line_spacing
            painter.drawLine(0, y, self.width, y)

        painter.setPen(self.pen)

        for i in range(self.line_count):
            y = i * self.line_spacing
            print(f"{i}, {self.line_spacing}, {y}")
            painter.drawLine(0, y, self.width, y)