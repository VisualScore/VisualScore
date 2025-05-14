from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from warnings import warn

from PyQt5.QtWidgets import QGraphicsSimpleTextItem
from neoscore.core import neoscore
from neoscore.core.point import Point

# this makes the class abstract
@dataclass(frozen=True)
class PositionedObjectInterface:
    """Interface for a generic graphic object.

    All graphic interfaces for renderable objects should descend from
    this and also be immutable dataclasses.
    """

    pos: Point
    """The position of the object.

    If a parent is provided, this position is relative to that interface. Otherwise it
    is in absolute document coordinates.
    """

    parent: Optional[PositionedObjectInterface]
    """The object's parent, if any.

    If a parent interface is provided, it must be rendered before this interface.
    """

    scale: float
    """A scaling factor, where 1 is no scaling.

    This occurs relative to ``transform_origin``.

    Scaling is inherited from parents to children along the interface tree.
    """

    rotation: float
    """Rotation angle in degrees, where 0 is no rotation.

    This occurs relative to ``transform_origin``.

    Rotation is inherited from parents to children along the interface tree.
    """

    transform_origin: Point
    """The origin point for rotation and scaling transforms"""

    _qt_object: Optional[QGraphicsSimpleTextItem] = field(init=False, compare=False, repr=False)
    """A corresponding Qt object for internal use only.

    This value is set during rendering and is not meant to be set more than once.
    """

    class _MovableTextItem(QGraphicsSimpleTextItem):
        """Internal Qt item subclass that syncs position to interface."""

        def __init__(self, interface: PositionedObjectInterface, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._interface = interface

        def itemChange(self, change, value):
            if change == QGraphicsSimpleTextItem.ItemPositionChange:
                new_pos: Point = value
                print(f"[DEBUG] Qt item moved to: {new_pos.x()}, {new_pos.y()}")
                object.__setattr__(self._interface, "pos", Point(new_pos.x(), new_pos.y()))
            return super().itemChange(change, value)

    def render(self):
        """Render the object to the scene.

        This is typically done by constructing a `QGraphicsSimpleTextItem` subclass and calling
        `_register_qt_object` with it. Do *not* manually assign the Qt object's parent
        or add it to the Qt scene.
        """
        raise NotImplementedError

    def _parent_qt_obj(self) -> Optional[QGraphicsSimpleTextItem]:
        if self.parent:
            parent_qt_obj = getattr(self.parent, "_qt_object", None)
            if not parent_qt_obj:
                warn(
                    "Parent interface was provided but corresponding Qt object"
                    + f" not available when needed for {self}"
                )  # implicitly return None
            return parent_qt_obj
        return None

    def _register_qt_object(self, obj: QGraphicsSimpleTextItem):
        parent_obj = self._parent_qt_obj()
        obj.setFlag(QGraphicsSimpleTextItem.ItemIsMovable, True)
        obj.setFlag(QGraphicsSimpleTextItem.ItemIsSelectable, True)
        obj.setFlag(QGraphicsSimpleTextItem.ItemSendsGeometryChanges, True)
        # obj.setFlag(QGraphicsSimpleTextItem.ItemIsFocusable, True)
        if parent_obj:
            obj.setParentItem(parent_obj)
        else:
            neoscore.app_interface.scene.addItem(obj) # TODO look more closely at this line
        
        super().__setattr__("_qt_object", obj)
