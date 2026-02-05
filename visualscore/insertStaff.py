from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QPainter

from neoscore.core.units import Unit, Mm
from neoscore.core.pen import Pen
from neoscore.core.path import Path
from neoscore.core.point import Point, ORIGIN
from neoscore.western.staff import Staff


class VSStaff(Staff):
    """Composite object of neoscore staff with staff overlay"""

    def __init__(
        self,
        staff_params,
    ):
        self.pos = staff_params.get("mouse_pos")
        self.line_num = staff_params.get("line_num")
        self.line_dist = staff_params.get("line_dist") # in staff spaces
        self.length = Unit(100)
        self.line_space = Mm(1.75)

        self.invis_line_count = self.line_num * self.line_dist - (self.line_dist - 1)

        super().__init__(
            self.pos, None, self.length, None, self.line_space, self.invis_line_count, pen=Pen.no_pen()
        )

        self.draw_visible_staff()
        self.render()


    def draw_visible_staff(self):
        for i in range(self.line_num):
            y = i * self.line_space * self.line_dist
            
            line = Path(Point(Unit(0), y), self, "000000")
            line.straight_line(Point(Unit(0), y), self, Point(self.length, Unit(0)))
