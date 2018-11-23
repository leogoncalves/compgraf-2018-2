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

def delTriangle(p1, p2, points):
    v1 = p2.subtract(p1)  
    cos = 2
    p3 = Point()

    for candidato in points:
        if not candidato.isEquals(p1) and not candidato.isEquals(p2):            
            v2 = candidato.subtract(p1)
            v3 = v1.cross(v2)
        
            if v3.z > 0:
                v2 = p1.subtract(candidato).normalize()
                v3 = p2.subtract(candidato).normalize()
                cos_candidato = v2.dot(v3)
            
                if cos_candidato < cos:
                    cos = cos_candidato
                    p3 = candidato
    return p3

def item_in_collection(item, collection):
  return item in collection

# Give edges from triangle
def edge_destine(item):
  return 3 * (item//3) + (item+1) % 3

def delaunay(points):
    convex_hull = jarvis_convex_hull(points)
    triangle = convex_hull[0:2]
    
    # Triangle indexes queue
    queue = [1, 2]

    point = delTriangle(convex_hull[0], convex_hull[1], points)
    triangle.append(point)
    
    # Add in queue the index of first element from delaunay triangulation 
    for i in range(0, len(queue), 1):
        p1 = triangle[edge_destine(queue[i])]
        p2 = triangle[edge_destine(queue[i] + 1)]
        point = delTriangle(p2, p1, points)
        
        

        triangle.append(p2)
        triangle.append(p1)
        triangle.append(point)


        queue.pop(0)
        queue.append()
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
    
    
  

