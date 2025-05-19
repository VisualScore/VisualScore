import os
import resources
from time import time
from typing import Optional, Tuple

from PyQt5 import QtCore, QtWidgets, uic

from neoscore.western.staff import Staff
from neoscore.core.point import ORIGIN, Point
from neoscore.core.units import Mm, Unit
from neoscore.core import *
from neoscore.core import neoscore
from neoscore.interface.qt import viewport
from neoscore.core.brush import Brush, Color
from neoscore.core.path import Path

from neoscore.interface.qt.dialog_ui.staff_preview_item import StaffPreviewItem

_X_MARGIN = 10

class CreateStaffDialog(QtWidgets.QDialog):

    _ui_path = os.path.join(os.path.dirname(__file__), "create_staff.ui")
    
    def __init__(self):
        super().__init__()
        uic.loadUi(CreateStaffDialog._ui_path, self)

        self.stackedWidget.setCurrentWidget(self.uniform_page)
        
        # Connect signals to slots
        self.lineNumber_spinBox.valueChanged.connect(self.updateStaffPreview)
        self.uniformLineDistance_checkBox.toggled.connect(self.changeStackedWidget)

        self.lineDistance_spinBox.valueChanged.connect(self.updateStaffPreview)
        
        self.setWindowTitle("Create Staff")

        # Set up QGraphicsScene + View
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect((self.staffPreview_graphicsView.width() - _X_MARGIN), 50, self.staffPreview_graphicsView.width(), self.staffPreview_graphicsView.height())
        print(f"Scene rect: {self.scene.sceneRect()}")

        self.staffPreview_graphicsView.setScene(self.scene)
        self.staffPreview_graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.staffPreview_graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.updateStaffPreview()

        #self.staffPreview_graphicsView.invalidateScene(updateStaffPreview)

    def updateStaffPreview(self):
        print("Updating staff preview...")

        # Clear old items
        self.scene.clear()

        # Get parameters from UI
        line_count = self.lineNumber_spinBox.value()
        default_line_spacing = 10
        uniform_line_spacing = self.lineDistance_spinBox.value()
        line_distance = uniform_line_spacing * default_line_spacing
        width = self.staffPreview_graphicsView.width() - (_X_MARGIN * 2)
        center_y = self.staffPreview_graphicsView.height() / 2

        staff_item = StaffPreviewItem(line_count, default_line_spacing, line_distance, width)

        staff_item.setPos(_X_MARGIN, center_y - (staff_item.height / 2))
        self.scene.addItem(staff_item)

    def changeStackedWidget(self):
        if self.uniformLineDistance_checkBox.checkState(): # if checked
            self.stackedWidget.setCurrentWidget(self.uniform_page)
        else: # if unchecked
            self.stackedWidget.setCurrentWidget(self.variable_page)

    def show(self):
        self.updateStaffPreview()
        super().show()

        