from neoscore.core.neoscore import setup, show
from neoscore.core.mouse_event import MouseEvent, MouseEventType, MouseButton
from neoscore.core.paper import LETTER
from neoscore.core.text import Text
from neoscore.core.point import ORIGIN
from neoscore.common import *

setup(LETTER)
# hard code for now
# font = MusicFont("Bravura", Unit(10))
# MusicText(ORIGIN, None, "staff1Line", font)
# MusicText(ORIGIN, None, "gClef", font)
# second_page = neoscore.document.pages[1]
# third_page = neoscore.document.pages[2]

def updateProps():
    for page in neoscore.document.pages:
        for obj in page.descendants:
            interfaces = getattr(obj, "interfaces", None)
            if interfaces:
                iface_pos = interfaces[0].pos
                # Rebuild position with Unit-wrapped values
                obj.pos = Point(Unit(iface_pos.x), Unit(iface_pos.y))
    
def mouseReleaseEvent(event):
    if event.event_type == MouseEventType.RELEASE:
        print("Mouse button released")
        updateProps()
    # if event.button() == QtCore.Qt.LeftButton:
    #     updateProps()

neoscore.set_mouse_event_handler(mouseReleaseEvent)

show()