#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tenta importar o OpenGL, o GLU e o GLUT.
# caso falhe em importar, exibe mensagem de erro
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print "OpenGL not found"

polygonal = [] 
closed = False
width = 500
height = 500

class Point:

    
    def __init__(self, x, y, r=1, g=1, b=1, a=1):
        self.x = x
        self.y = y
        self.r = r 
        self.g = g
        self.b = b
        self.a = a

    
    def createLineBetweenDots(self):
        # glColor4d(self.r, self.g, self.b, self.a)
        glVertex2f(self.x, self.y)
    
    def subtract(self, xx, yy):
        return Point(self.x - xx, self.y - yy)

    def sum(self, xx, yy):
        return Point(self.x + xx, self.y + yy)
    
def product(point, value):
    point.x = point.x*value
    point.y = point.y*value
    
def division(point, value):
    point.x = point.x/value
    point.y = point.y/value


def getMousePosition(button, state, x, y):    
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:            
            xx = ((x / float(width)) - 0.5) * 2.0
            yy= (0.5 - (y / float(height))) * 2.0            
            point = Point(xx, yy)
            polygonal.append(point)
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:    
        polygonal.append(polygonal[0])
       
    glutPostRedisplay()


def display():
    

    glClearColor(0.0,0.0,0.0,1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    
    glPointSize(3.)
    
    glBegin(GL_LINE_STRIP)    
    for ponto in polygonal:
        ponto.createLineBetweenDots()                
    glEnd()

    glBegin(GL_POINTS)    
    for ponto in polygonal:
        ponto.createLineBetweenDots()           
    glEnd()   

    glFlush()


def main():
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    glutInit(sys.argv)
    glutCreateWindow("Trabalho 2")
    glutMouseFunc(getMousePosition)        
    glutDisplayFunc(display)
    glutMainLoop()

# Call the main function
if __name__ == '__main__':
    main()
