import numpy as np

from .geometry import area_4points
from .vortices import (vortex_position_in_panel,
                       v_induced_by_horseshoe_vortex)


class Panel(object):
    """
           y ^
             |              The panel is defined by the (x, y) coordinates
        P3-C-|-D-P4         of four points ordered clockwise - namely P1,
         | | | |  |         P3, P3 and P4 -. Points defining the horseshoe
         | | +-P--|--->     - A, B, C and D - are named clockwise as well.
         | |   |  |   x
        P2-B---A-P1

    Parameters
    ----------
    P1, P2, P3, P4 : array_like
                     Corner points in a 2D euclidean space
    """

    def __init__(self, P1, P2, P3, P4):
        self.P1 = P1
        self.P2 = P2
        self.P3 = P3
        self.P4 = P4

        P1P2 = self.P2 - self.P1
        P3P4 = self.P4 - self.P3

        if np.cross(P1P2, P3P4) != 0:
            msg = 'Panel incorrectly defined, P1P2 and P3P4 not parallel'
            raise ValueError(msg)

    def area(self):
        """ Yields the area calculated with the points provided as
            arguments """

        return area_4points(self.P1, self.P2, self.P3, self.P4)

    def span(self):
        """ Yields the span of the panel, which must be constant - P1P2
            and P3P4 must be parallel - """

        b = self.P3[1] - self.P2[1]
        b__ = self.P4[1] - self.P1[1]

        if abs(b) != abs(b__):
            msg = 'Panel incorrectly defined, |P1P4| =/ |P2P3|'
            raise ValueError(msg)

        return abs(b)

    def _vortex_position(self):
        """ Returns the (x, y) coordinates of the four points that define
            the position of the vortex horseshoe within the panel plus
            the control point, identified as PABCD in the documentation
            above.

                *Remainder: the coordinates are returned as a list,
                            following the order [P, A, B, C, D] """

        points_of_the_vortex = vortex_position_in_panel(self.P1,
                                                        self.P2,
                                                        self.P3,
                                                        self.P4)

        return points_of_the_vortex

    def control_point(self):
        """ Returns the (x, y) coordinates position of the control point """

        control_point_position = self._vortex_position()[0]

        return control_point_position

    def induced_velocity(self, control_point_pos):
        """ Calculates and returns the induced velocity by a horseshoe
            vortex on a control point, defined as argument of the method """

        _points_vortex = self._vortex_position()
        v = v_induced_by_horseshoe_vortex(control_point_pos,
                                          _points_vortex[1],
                                          _points_vortex[2],
                                          _points_vortex[3],
                                          _points_vortex[4])

        return v
