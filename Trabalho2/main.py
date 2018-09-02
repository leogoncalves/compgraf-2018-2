#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Try import libs. Throw except if fail
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
    from math import sqrt, pow
except:
    print "OpenGL not found"

# List to store polygonal points
polygon = [] 

# List to store random click points
collection = []

# Used to verify if polygon is closed
closed = bool

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

# Mouse controls. Let's the play begin
def mouse(button, state, x, y):    
    
    # When press mouse left button, create a point.
    # If polygon is open, add point to polygon list. Else, add 
    # point to other list
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:            
            xx = ((x / float(_WIDTH)) - 0.5) * 2.0
            yy= (0.5 - (y / float(_HEIGHT))) * 2.0            
            point = Point(xx, yy)
            if closed == True:
                collection.append(point)
            else:
                polygon.append(point)

    # If press right button, the polygon is closed
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:    
            global closed
            polygon.append(polygon[0])
            closed = True        

    # Repaint screen
    glutPostRedisplay()

# Check if point is inside or outside of the polygon. 
# Receive a point and a polygon
def isInside(point, polygon):
    n = len(polygon)
    inside = False

    # Get the firt polygon point
    a_point = polygon[0]

    # Walks by all polygon points
    for i in range(n+1):

        # Get each point of polygon
        b_point = polygon[i%n]
        if point.y > min(a_point.y, b_point.y):
            if point.y <= max(a_point.y, b_point.y):
                if point.x <= max(a_point.x, b_point.x):
                    # Calculate internal product between points if y coords are not equals
                    if a_point.y != b_point.y:
                        xinters = (point.y - a_point.y) * (b_point.x-a_point.x)/(b_point.y - a_point.y) + a_point.x
                    if a_point.x == b_point.x or point.x <  xinters:
                        inside = not inside
        # Update first point
        a_point = b_point
    # Return true if point is inside. False if outside
    return inside



def smooth(polygon):
    # Create list to store smoothed points
    newPolygon = [] 
    i = 0    

    # Walks for every points in polygon
    for point in polygon:
        if i == 0:
            newPolygon.append(point)
            i+=1
            continue

        # Divide line segment in four pieces and store three
        p = point.subtract(polygon[i-1].x, polygon[i-1].y)
        p = p.division(4.0)
        
        newPolygon.append(p.sum(polygon[i-1].x, polygon[i-1].y))


        p = p.product(3.0)
        newPolygon.append(p.sum(polygon[i-1].x, polygon[i-1].y))

        # Store last created point
        if i == len(polygon) - 1:
            newPolygon.append(point)
        i+=1
    # Return points to create a smoothed polygon
    return newPolygon


# Keyboard events. Here's our controls
def keyboard(key, x, y):

    # Press 'esc' key to close window
    if key == chr(27):
        sys.exit()
    
    # Press 'C' or 'c' to clear screen
    if key == chr(67) or key == chr(99):
        global polygon
        polygon[:] = []
        glutPostRedisplay()        

    # press 'S' or 's' key to smooth
    if key == chr(83) or key == chr(115):
        global polygon
        smoothPolygon = smooth(polygon)
        polygon = smoothPolygon
        glutPostRedisplay()

# Paint display
def display():
    glClearColor(0.0,0.0,0.0,1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    
    glPointSize(3.50)
    

    glBegin(GL_LINE_STRIP)    
    for point in polygon:
        point.createLineBetweenDots()    
    glEnd()

    glBegin(GL_POINTS)    
    for point in collection:
        if isInside(point, polygon):
            glColor3f(0.0, 1.0, 0.0)
            glVertex2d(point.x, point.y)
        else:
            glColor3f(1.0, 0.0, 0.0)
            glVertex2d(point.x, point.y)
    
    glEnd()
    glutSwapBuffers()
    glFlush()


def main():
    glutInitWindowSize(_WIDTH, _HEIGHT)
    glutInitWindowPosition(10, 10)
    glutInit(sys.argv)
    glutCreateWindow("Trabalho 2")
    glutMouseFunc(mouse)    
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutMainLoop()

# Call the main function
if __name__ == '__main__':
    main()
