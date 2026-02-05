from neoscore.core import neoscore
from neoscore.core.neoscore import setup, show
from neoscore.core.mouse_event import MouseEventType
from neoscore.core.paper import LETTER

from visualscore import visualscore

setup(LETTER)
    
def mouseReleaseEvent(event):
    if event.event_type == MouseEventType.RELEASE:
        visualscore.openMenu(event)

neoscore.set_mouse_event_handler(mouseReleaseEvent)

show()