from PyQt5.QtCore import QPointF

from neoscore.core import neoscore
from neoscore.core.point import Point
from neoscore.core.units import Unit
from neoscore.interface.qt.converters import qt_point_to_point

from visualscore import insertStaff


def updateProps():
    for page in neoscore.document.pages:
        for obj in page.descendants:
            interfaces = getattr(obj, "interfaces", None)
            if interfaces:
                iface_pos = interfaces[0].pos
                # Rebuild position with Unit-wrapped values
                obj.pos = Point(Unit(iface_pos.x), Unit(iface_pos.y))
    
def openMenu(event):
    updateProps()

    zoom_coef = neoscore.get_viewport_scale()

    window_corner = neoscore.app_interface.view.window_document_pos()
    click_from_window_corner = QPointF(*event.window_pos)

    pages = neoscore.document.pages

    mouse_pos = qt_point_to_point((click_from_window_corner/zoom_coef) + window_corner)

    for page in pages:
        min_point = Point(page.left_margin_x, page.top_margin_y)
        max_point = Point(page.right_margin_x, page.bottom_margin_y)

        bounding_rect = page.document_space_bounding_rect
        scaled_bounding_offset = Point(bounding_rect.x/zoom_coef, bounding_rect.y/zoom_coef)

        mouse_pos = mouse_pos + Point(-(scaled_bounding_offset.x/10), (9*scaled_bounding_offset.y)/10)
        

        if (mouse_pos.x > min_point.x and mouse_pos.y > min_point.y) and (mouse_pos.x < max_point.x and mouse_pos.y < max_point.y):
            neoscore.app_interface.main_window.createStaffDialogPopup(mouse_pos)