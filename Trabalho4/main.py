#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Try import libs. Throw except if fail
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print("OpenGL not found")

from math import sqrt, acos

# List to store random click points
collection = []
hull = []
triangulation = []

# Window dimension
_WIDTH = 500
_HEIGHT = 500


class Point:

    def __init__(self, x, y, r=1, g=1, b=1, a=1):

        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    # Create line segment between two dots
    def createLineBetweenDots(self):
        glColor4d(self.r, self.g, self.b, self.a)
        glVertex2d(self.x, self.y)

    # Some simple arithmetic operations

    def sum(self, x, y):
        return Point(self.x + x, self.y + y)

    def subtract(self, x, y):
        return Point(self.x - x, self.y - y)
    
    def product(self, scalar):
        return Point(self.x * scalar, self.y * scalar)

    def division(self, scalar):
        return Point(self.x / scalar, self.y / scalar)

def dot(p, q):
    return (p.x*q.x) + (p.y*q.y)

def norm(a):
    return sqrt(pow(a.x, 2) + pow(a.y, 2))

def theta(a, b):
    return dot(a,b)/(norm(a)*norm(b))

# Define orientation
def orientation(p, q, r):
    k = ((q.y - p.y) * (r.x - q.x)) - ((q.x - p.x) * (r.y - q.y))
    if k == 0:
        return 0    # Collinear
    if k > 0:
        return 1    # Clockwise orientation
    else:
        return 2    # Counterclockwise orientation

# Jarvis March
def jarvis_convex_hull(points):
    n = len(points)     # Size of points on cloud
    hull = []   # Store cloud points

    # Get leftmost point on x-axis
    l = 0
    for i in range(n):
        if points[i].x < points[l].x:
            l = i
    p = l

    # Start from leaftmost point, keep moving
    # counterclockwise until the start point again
    while True:
        hull.append(points[p])      # Add current point to list

        # Search the point to wrap cloud points.
        q = (p + 1) % n
        for i in range(n):
            # if i is more ccw than current q, then update q
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
        p = q   # set p for next iteration

        # End the road
        if p == l:
            # hull.append(points[l])      # Trick to close path
            break
    return hull

def delaunay(points):
    convex_hull = jarvis_convex_hull(points)
    queue = convex_hull[0:2]
    triangle = convex_hull[0:2]
    cos = 1
    point = 0
    for i in range(0, len(queue), 1):
        for j in range(0, len(points), 1):
            if theta(queue[i], points[j]) < cos:
                cos = theta(queue[i], points[j])
                point = j
        triangle.append(points[point])
        queue.append(points[point])
        queue.pop(0)
    return triangle

# Keyboard events. Here's our controls
def keyboard(key, x, y):
    global collection
    global hull
    global triangulation

    # Press 'esc' key to close window
    if key == chr(27):
        sys.exit()

    # Press 'C' or 'c' to clear screen
    if key == chr(67) or key == chr(99):
        collection[:] = []
        glutPostRedisplay()

    # Convex hull - Press h
    if key == chr(72) or key == chr(104):
        # global hull
        hull = jarvis_convex_hull(collection)

    # Triangulation
    if key == chr(84) or key == chr(116):
        triangulation = delaunay(collection)


# Mouse controls. Let's the play begin
def mouse(button, state, x, y):

    # When press mouse left button, create a point.
    # If polygon is open, add point to polygon list. Else, add
    # point to other list
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            xx = ((x / float(_WIDTH)) - 0.5) * 2.0
            yy = (0.5 - (y / float(_HEIGHT))) * 2.0
            point = Point(xx, yy)
            collection.append(point)

    # Repaint screen
    glutPostRedisplay()


# Paint display
def display():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

    glPointSize(3.50)

    glBegin(GL_POINTS)
    for point in collection:
        glColor3f(0.0, 1.0, 0.0)
        glVertex2d(point.x, point.y)
    glEnd()

    glBegin(GL_LINE_LOOP)
    for point in hull:
        point.createLineBetweenDots()
    glEnd()

    glBegin(GL_LINE_LOOP)
    for point in triangulation:
        point.createLineBetweenDots()
    glEnd()

    glutPostRedisplay()
    glutSwapBuffers()
    glFlush()


def main():
    glutInitWindowSize(_WIDTH, _HEIGHT)
    glutInitWindowPosition(10, 10)
    glutInit(sys.argv)
    glutCreateWindow("Trabalho 4")
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutMainLoop()


# Call the main function
if __name__ == '__main__':
    main()
