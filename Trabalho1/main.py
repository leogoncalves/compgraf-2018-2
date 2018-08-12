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

# Criamos uma variável global que receberá os pontos criados
# que serão usados para desenhar as linhas
polygonal = [] 

width = 500 # Valor a largura da janela
height = 500 # Valor a altura da janela

class Point:

    # Construtor do objeto. Recebe a posição (x, y) do ponto na tela
    # e cores rgba (Optei por manter apenas preto e branco no exercício)
    def __init__(self, x, y, r=1, g=1, b=1, a=1):
        # Seta a posição do ponto
        self.x = x
        self.y = y
        
        # Seta o valor da cor definida em rgba em rgba
        # self.r = r 
        # self.g = g
        # self.b = b
        # self.a = a

    # Create line segment between two dots
    def createLineBetweenDots(self):
        # glColor4d(self.r, self.g, self.b, self.a)
        glVertex2d(self.x, self.y)

    # As duas funções abaixo criam um novo objeto com base na posição
    # do ponto atual
    def subtract(self, xx, yy):
        return Point(self.x - xx, self.y - yy)

    def sum(self, xx, yy):
        return Point(self.x + xx, self.y + yy)
    
# As duas funções abaixo serão utilizadas para atualizar os 
# valores que serão usados para atualizar a posição de um ponto 

def product(point, value):
    point.x = point.x*value
    point.y = point.y*value
    
def division(point, value):
    point.x = point.x/value
    point.y = point.y/value

# Captura a posição do mouse na janela a cada 
# clique com o botão esquerdo. Cada clique cria
# um novo ponto e adiciona ele ao vetor de pontos
# que criamos globalmente

def mouse(button, state, x, y):    
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:            
            xx = ((x / float(width)) - 0.5) * 2.0
            yy= (0.5 - (y / float(height))) * 2.0            
            point = Point(xx, yy)
            polygonal.append(point)            
    glutPostRedisplay()

# Captura um evento do teclado. Como pedido, fazemos a suavização apertando qualquer tecla
def keyboard(key, x, y):
    newPolygonal = [] # Cria um novo vetor que usaremos para armazenar os pontos
    i = 0    

    # Aqui, fazemos o seguinte: Para cada par de pontos, dividimos a reta em quatro partes
    # e criamos novos pontos, descartando o último
    for point in polygonal:
        if i == 0:
            newPolygonal.append(point)
            i+=1
            continue

        p = point.subtract(polygonal[i-1].x, polygonal[i-1].y)
        division(p, 4.0)        
        
        newPolygonal.append(p.sum(polygonal[i-1].x, polygonal[i-1].y))

        product(p, 3.0)
        newPolygonal.append(p.sum(polygonal[i-1].x, polygonal[i-1].y))

        if i == len(polygonal) - 1:
            newPolygonal.append(point)
        i+=1
    
    # Atualizamos o objeto que continha os antigos 
    # pontos com os pontos da nova curva
    global polygonal
    polygonal = newPolygonal

    # Redesenhamos a tela
    glutPostRedisplay()

# Desenhamos a tela e desenhamos os pontos e retas
def display():
    glClearColor(0.0,0.0,0.0,1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA); 
    glEnable(GL_LINE_SMOOTH);
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
    
    glPointSize(1.50)
    

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
    glutInitWindowPosition(10, 10)
    glutInit(sys.argv)
    glutCreateWindow("Trabalho 1")
    glutMouseFunc(mouse)    
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutMainLoop()

# Call the main function
if __name__ == '__main__':
    main()
