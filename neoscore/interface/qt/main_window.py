import os
import resources
from time import time
from typing import Optional, Tuple

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsItem

# cannot import setup/show again here, circular import
# from neoscore.core.neoscore import setup, show
from neoscore.core.text import Text
from neoscore.core.point import ORIGIN
from neoscore.common import *

QT_PRECISE_TIMER = 0


class MainWindow(QtWidgets.QMainWindow):
    """The primary entry point for all UI code.

    This bootstraps the ``main_window.ui`` structure.
    """

    _ui_path = os.path.join(os.path.dirname(__file__), "main_window.ui")

    def __init__(self):
        super().__init__()
        uic.loadUi(MainWindow._ui_path, self)
        self.statusBar().showMessage("Example status message")
        self.refresh_func = None
        self.mouse_event_handler = None
        self._frame = 0  # Frame counter used in debug mode
                
        self.actionNew.triggered.connect(self.newFile)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_as.triggered.connect(self.saveAsFile)
        self.actionCut.triggered.connect(self.cutFile)
        self.actionCopy.triggered.connect(self.copyFile)
        self.actionPaste.triggered.connect(self.pasteFile)

        self.addPageButton.clicked.connect(self.addPage)
        self.delPageButton.clicked.connect(self.removePage)

        # Create a dynamic map: {button: symbol_name}
        button_method_map = {}

        for attr in dir(self):
            if attr.endswith("_Button") or attr.endswith("_button"):
                if not attr.startswith("menu"):
                    button = getattr(self, attr)
                    symbol_name = attr.removesuffix("_Button").removesuffix("_button")
                    button_method_map[button] = symbol_name

        for button, symbol_name in button_method_map.items():
            print(f"Button: {button}, Symbol Name: {symbol_name}")
            button.clicked.connect(lambda checked=False, name=symbol_name: self.createMusicText(name))
        
        # Hide Widget Menu
        self.scrollArea.setHidden(True)
        
        # Hide Dropdowns
        self.Staff_dropdown.setHidden(True)
        self.Stave_dropdown.setHidden(True)
        self.Barlines_dropdown.setHidden(True)
        self.Repeats_dropdown.setHidden(True)
        self.Clefs_dropdown.setHidden(True)
        self.Time_dropdown.setHidden(True)
        self.Note_Heads_dropdown.setHidden(True)
        self.Slash_dropdown.setHidden(True)
        self.Round_dropdown.setHidden(True)
        self.Note_Clusters_dropdown.setHidden(True)

    def newFile(self):
        print("New file clicked")
        
    def openFile(self):
        print("Open file clicked")
        
    def saveFile(self):
        print("Save file clicked")
        
    def saveAsFile(self):
        print("Save as file clicked")
        
    def cutFile(self):
        print("Cut file clicked")
        
    def copyFile(self):
        print("Copy file clicked")
        
    def pasteFile(self):
        print("Paste file clicked")

    # Makes page, page shadow, margin outline not dragable or selectable
    def make_previews_immovable(self):
        for page in neoscore.document.pages:
            for obj in page.descendants:
                if getattr(obj, "_is_preview", False):
                    qt_object = obj._interfaces[0]._qt_object
                    qt_object.setFlag(QGraphicsItem.ItemIsMovable, False)
                    qt_object.setFlag(QGraphicsItem.ItemIsSelectable, False)

    def updatePage(self):
        # neoscore.app_interface.clear_scene() 
        neoscore._render_document(True, Brush("#FFFFFF"))
        # self.graphicsView.viewport().update()
        self.make_previews_immovable()

        self.refresh()

    def addPage(self):
        new_page_index = len(neoscore.document.pages)
        print(new_page_index)

        Text(ORIGIN, neoscore.document.pages[new_page_index], f"This is page {new_page_index + 1}")
        neoscore.document.pages[new_page_index]
        
        # render the document again to show the new page
        self.updatePage()
    
    #TODO needs to remove deleted page from being rendered on graphicsView
    
    def removePage(self):
        if len(neoscore.document.pages) > 0:
            # Remove the last page
            last_page_index = len(neoscore.document.pages) - 1
            print(last_page_index)
            neoscore.document.pages.pop(last_page_index)

        else:
            print("No pages to remove.")
            
        # render the document again to reflect the removed page
        self.updatePage()

    def createMusicText(self, symbol_name):
        font = MusicFont("Bravura", Unit(10))
        MusicText(ORIGIN, None, symbol_name, font)
        self.updatePage()
    
    def show(
        self,
        min_size: Optional[Tuple[int, int]] = None,
        max_size: Optional[Tuple[int, int]] = None,
        fullscreen: bool = False,
    ):
        if min_size:
            self.setMinimumSize(QtCore.QSize(min_size[0], min_size[1]))
        if max_size:
            self.setMaximumSize(QtCore.QSize(max_size[0], max_size[1]))
        QtCore.QTimer.singleShot(0, QT_PRECISE_TIMER, self.refresh)  # noqa
        if fullscreen:
            super().showFullScreen()
        else:
            super().show()

    @QtCore.pyqtSlot()
    def refresh(self):
        start_time = time()
        if self.refresh_func:
            requested_delay_s = self.refresh_func(start_time)
            requested_delay_ms = int(requested_delay_s * 1000)
            QtCore.QTimer.singleShot(
                requested_delay_ms, QT_PRECISE_TIMER, self.refresh  # noqa
            )
            # if env.DEBUG:
            #     update_time = time() - start_time
            #     refresh_fps = int(1 / (time() - start_time))
            #     if self._frame % 30 == 0:
            #         print(
            #             f"Scene update took {int(update_time * 1000)} ms ({refresh_fps} / s)"
            #         )
            #         print(f"requested delay was {requested_delay_ms} ms")
            #     self._frame += 1
        # The viewport is unconditionally updated because we disable automatic updates
        self.graphicsView.viewport().update()