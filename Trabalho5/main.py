#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Try import libs. Throw except if fail
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print("OpenGL not found")

import math

# List to store random click points
collection = []
curves = []

# Window dimension
_WIDTH = 500
_HEIGHT = 500


class Point:

    def __init__(self, x = 0, y = 0, z = 0, r=1, g=1, b=1, a=1):

        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    # Create line segment between two dots
    def createLineBetweenDots(self):
        glColor4d(self.r, self.g, self.b, self.a)
        glVertex2d(self.x, self.y)

    # Some simple arithmetic operations

    def add(self, point):
        return Point(self.x + point.x, self.y + point.y, self.z + point.z)

    def subtract(self, point):
        return Point(self.x - point.x, self.y - point.y, self.z - point.z)
    
    def product(self, scalar):
        return Point(self.x * scalar, self.y * scalar, self.z * scalar)

    def division(self, scalar):
        return Point(self.x / scalar, self.y / scalar, self.z / scalar)

    def isEquals(self, point):
        return (self.x == point.x) and (self.y == point.y)            
    
    def dot(self, point):
      return (self.x * point.x) + (self.y * point.y) + (self.z * point.z)
    
    def cross(self, point):
      x = (self.y * point.z) - (self.z * point.y)
      y = (self.z * point.x) - (self.x * point.z)
      z = (self.x - point.y) - (self.y * point.x)
      return Point(x, y, z)
    
    def norm(self):
      return sqrt(pow(self.x, 2) + pow(self.y, 2) + pow(self.z, 2))
		
    def normalize(self):
      return self.division(self.norm())
    



def binomial(i, n):
    return math.factorial(n) / float(
        math.factorial(i) * math.factorial(n-i)
    )

def bernstein(t, i, n):
    return binomial(i, n) * (t ** i) * ((1-t) ** (n-i))

def bezier(points, t):
    n = len(points)
    point = Point()    
    for i in range(n+1):
        if (i != n):
            point.x += bernstein(n-1, i, t) * points[i].x
            point.y += bernstein(n-1, i, t) * points[i].y
    return point

def bezier_curve_range(n, points):
    for i in xrange(n):
        t = i / float(n-1)
        yield bezier(t, points)

def f(points, t):
    x = bezier(points, t).x
    y = bezier(points, t).y
    return Point(x, y)

def criaCurva(points):
    for i in range(0, 11):
        t = float(i)/10
        curves.append(f(points, t))


# Keyboard events. Here's our controls
def keyboard(key, x, y):
    global collection    
    global curves

    # Press 'esc' key to close window
    if key == chr(27):
        sys.exit()

    # Press 'C' or 'c' to clear screen
    if key == chr(67) or key == chr(99):
        collection[:] = []
        glutPostRedisplay()
    
    # bezier curve - Press f
    if key == chr(70) or key == chr(102):
        print(collection)
        print(curves)
        curves = criaCurva(collection)

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
    
    glBegin(GL_LINE_STRIP)
    for point in curves:
        point.createLineBetweenDots()
    glEnd()

    glutPostRedisplay()
    glutSwapBuffers()
    glFlush()


def main():
    glutInitWindowSize(_WIDTH, _HEIGHT)
    glutInitWindowPosition(10, 10)
    glutInit(sys.argv)
    glutCreateWindow("Trabalho 5")
    glutMouseFunc(mouse)
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutMainLoop()


# Call the main function
if __name__ == '__main__':
    main()
