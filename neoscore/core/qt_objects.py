from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtWidgets import QGraphicsItem
from neoscore.core.point import Point

class MovableClippingPath(QGraphicsPathItem):
    def __init__(self, interface, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interface = interface
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            new_pos = value
            object.__setattr__(self.interface, "pos", Point(new_pos.x(), new_pos.y()))
        return super().itemChange(change, value)