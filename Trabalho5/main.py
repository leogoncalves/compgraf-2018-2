#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Try import libs. Throw except if fail
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print("OpenGL not found")

from math import *
import random 
# List to store random click points
collection = []
curves = []
hull = []
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


def binomial(n, i):
    return factorial(n) / float(
           factorial(i) * factorial(n-i)
    )

def bernstein(n, i, t):
    # print(n, i, t)
    return binomial(n, i) * (t ** i) * ((1-t) ** (n-i))

def bezier(points, t):
    n = len(points)
    point = Point()    
    for i in range(n+1):        
        if (i != n):
            point.x += bernstein(n-1, i, t) * points[i].x
            point.y += bernstein(n-1, i, t) * points[i].y
    return point

def f(points, t):
    x = bezier(points, t).x
    y = bezier(points, t).y
    return Point(x, y)

def criaCurva(points):
    curves = []
    for i in range(0, 11):
        t = float(i)/10
        x = f(points, t)
        curves.append(f(points, t))
    return curves



# Keyboard events. Here's our controls
def keyboard(key, x, y):
    global collection    
    global hull
    global curves

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
    
    # bezier curve - Press f
    if key == chr(70) or key == chr(102):
        # global curves
        curves = criaCurva(collection)

    # rotate - Press x
    if key == chr(88) or key == chr(120):        
        glRotatef(10,1,0,0)
        glutPostRedisplay()
    
    # rotate - Press y
    if key == chr(89) or key == chr(121):        
        glRotatef(10,0,1,0)
        glutPostRedisplay()
    
    # rotate - Press z
    if key == chr(90) or key == chr(122):        
        glRotatef(10,0,0,1)
        glutPostRedisplay()

# Mouse controls. Let's the play begin
def mouse(button, state, x, y):

    # When press mouse left button, create a point.
    # If polygon is open, add point to polygon list. Else, add
    # point to other list
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            xx = ((x / float(_WIDTH)) - 0.5) * 2.0
            yy = (0.5 - (y / float(_HEIGHT))) * 2.0
            zz = random.uniform(0.0, 1.0)
            print(zz)
            point = Point(xx, yy, zz)
            collection.append(point)

    # Repaint screen
    glutPostRedisplay()


# Paint display
def display():
    glMatrixMode(GL_MODELVIEW)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glPointSize(3.50)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

    glBegin(GL_POINTS)
    for point in collection:
        glColor3f(0.0, 1.0, 0.0)
        glVertex2d(point.x, point.y)
    glEnd()

    glBegin(GL_LINE_LOOP)
    for point in hull:
        point.createLineBetweenDots()
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
