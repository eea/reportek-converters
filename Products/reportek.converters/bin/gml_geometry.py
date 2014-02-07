# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA). Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency. All
# Rights Reserved.
#
# Authors:
# Alexandru Ghica, Finsiel Romania
# Bogdan Grama, Finsiel Romania
# Iulian Iuga, Finsiel Romania

__doc__ = """
    Collection of geometry utility methods
"""


# Check if two line segments intersects.
# Slightly deficient function to determine if the two lines p1, p2 and
# p2, p3 turn in counter clockwise direction}
# Algorithm from Sedgewick
def ccw(p0x,p0y,p1x,p1y,p2x,p2y):
    dx1 = p1x-p0x
    dy1 = p1y-p0y
    dx2 = p2x-p0x
    dy2 = p2y-p0y
    if (dx1*dy2)>(dy1*dx2):
        ccwr = 1
    if (dx1*dy2)<(dy1*dx2):
        ccwr = -1
    if (dx1*dy2)==(dy1*dx2):
        if ((dx1*dx2)<0) or ((dy1*dy2)<0):
            ccwr=-1
        elif ((dx1*dx1)+(dy1*dy1))>=((dx2*dx2)+(dy2*dy2)):
            ccwr=0
        else:
            ccwr=1
    return ccwr

# Check if two line segments intersects.
# Algorithm from Sedgewick
def intersect2lines(x0, y0, x1, y1, x2, y2, x3, y3):
    rez =((ccw(x0, y0, x1, y1, x2, y2)*ccw(x0, y0, x1, y1, x3, y3))<=0)and ((ccw(x2, y2, x3, y3, x0, y0)*ccw(x2, y2, x3, y3,x1, y1))<=0)
    return rez

# Check if a specified point is inside a specified rectangle.
# @param x0, y0, x1, y1  Upper left and lower right corner of rectangle (inclusive)
# @param x,y             Point to check.
# @return                True if the point is inside the rectangle, false otherwise.
# int x0, int y0, int x1, int y1, int x, int y
def isPointInsideRectangle (x0,y0,x1,y1,x,y):
    return (x >= x0) and (x <= x1) and (y <= y0) and (y >= y1)




# Check if a specified line intersects a specified rectangle.
# Integer domain.
# 
# @param lx0, ly0        1st end point of line
# @param ly1, ly1        2nd end point of line
# @param x0, y0, x1, y1  Upper left and lower right corner of rectangle
#                       (inclusive).
# @return                True if the line intersects the rectangle,
#                        false otherwise.
def isLineIntersectingRectangle (lx0, ly0, lx1, ly1, x0, y0, x1, y1):
    #Is one of the line endpoints inside the rectangle
    if isPointInsideRectangle(x0, y0, x1, y1, lx0, ly0) or isPointInsideRectangle(x0, y0, x1, y1, lx1, ly1):
        return True

    #If it intersects it goes through. Need to check three sides only.
    # Check against top rectangle line
    if intersect2lines (lx0, ly0, lx1, ly1,x0, y0, x1, y0):
        return True

    # Check against left rectangle line
    if intersect2lines (lx0, ly0, lx1, ly1, x0, y0, x0, y1):
        return True

    # Check against bottom rectangle line
    if intersect2lines (lx0, ly0, lx1, ly1,x0, y1, x1, y1):
        return True

    return False



 #Check if a specified polyline intersects a specified rectangle.
 #Integer domain.
 #
 #@param ls_xy            Polyline to check.
 #@param x0, y0, x1, y1  Upper left and lower left corner of rectangle
 #                       (inclusive).
 #@return                True if the polyline intersects the rectangle,
 #                       false otherwise.

def isPolylineIntersectingRectangle (ls_xy, x0, y0, x1, y1):
    if (len(ls_xy) == 0):
        return 0
    if (isPointInsideRectangle (ls_xy[0][0], ls_xy[0][1], x0, y0, x1, y1)):
        return 1
    elif (len(ls_xy) == 1):
        return 0
    for i in range(len(ls_xy)):
        if (ls_xy[i-1][0] != ls_xy[i][0] or ls_xy[i-1][1] != ls_xy[i][1]):
            if (isLineIntersectingRectangle (ls_xy[i-1][0], ls_xy[i-1][1], ls_xy[i][0], ls_xy[i][1], x0, y0, x1, y1)):
                return 1
    return 0


 #Check if a specified polygon intersects a specified rectangle.
 #Integer domain.
 #
 #@param ls_xy   coordinates of polyline.
 #@param x0  X of upper left corner of rectangle.
 #@param y0  Y of upper left corner of rectangle.   
 #@param x1  X of lower right corner of rectangle.
 #@param y1  Y of lower right corner of rectangle.   
 #@return    True if the polyline intersects the rectangle, false otherwise.

def isPolygonIntersectingRectangle (ls_xy, x0, y0, x1, y1):

    if (len(ls_xy) == 0):
        return 0    
    if (isPointInsideRectangle (ls_xy[0][0], ls_xy[0][1], x0, y0, x1, y1)):
        return 1
    elif (len(ls_xy) == 1):
        return 0
    # If the polyline constituting the polygon intersects the rectangle
    # the polygon does too.

    if (isPolylineIntersectingRectangle (ls_xy, x0, y0, x1, y1)):
        return 1
    # Check last leg as well
    if (isLineIntersectingRectangle (ls_xy[len(ls_xy)-2][0], ls_xy[len(ls_xy)-2][1], ls_xy[len(ls_xy)-1][0], ls_xy[len(ls_xy)-1][1], x0, y0, x1, y1)):
        return 1
    
    # The rectangle and polygon are now completely including each other
    # or separate.
    #isPointInsidePolygon (x, y, x0, y0) or 
    if (isPointInsideRectangle (x0, y0, x1, y1, ls_xy[0][0], ls_xy[0][1])):
        return 1
    return 0


# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.

def point_inside_polygon(x,y,l_poly):

    n = len(l_poly)
    inside =False

    j = 0
    for i in range(n):
        j+=1
        if (j == n):
            j = 0
        if (l_poly[i][1] < y and l_poly[j][1] >= y or l_poly[j][1] < y and l_poly[i][1] >= y):
            if (l_poly[i][0] + (y - l_poly[i][1]) / (l_poly[j][1] - l_poly[i][1]) * (l_poly[j][0] - l_poly[i][0]) < x):
                inside = not inside
    return inside