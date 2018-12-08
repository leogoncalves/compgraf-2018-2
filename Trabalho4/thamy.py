#!/usr/bin/env python
# -*- coding: utf-8 -*-
from OpenGL.GL import * #importando o OpenGl e suas libs... 
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
# Criamos uma variável global que receberá os pontos criados
array_pontos = [] 
# Criamos a estrutura que vai armazenar a triangulacao de delaunay
#classe half-edge linha 35
triang = []
#array com as arestas ja visitadas
visitadas = []
#armazenando as arestas do fecho convexo
fecho_convex = []

width = 600 # Valor a largura da janela
height = 600 # Valor a altura da janela

class Ponto:

    # Construtor do objeto. Recebe a posição (x, y) do ponto na tela

    def __init__(self, x, y):
        # Seta a posição do ponto
        self.x = x
        self.y = y
        
    # Criando linhas entre dois pontos
    def criaAresta(self):
        glVertex2d(self.x, self.y)

#estrutura para armazenar as arestas....
class HalfEdge:
	#construtor da classe
	def __init__(self, ponto_inicial, ponto_final):
		self.ponto_inicial = ponto_inicial
		self.ponto_final = ponto_final
		self.listaTriangulos = []
		#o indice no array é o número da halfedge...

		#triangulo a qual a half-edge pertence:
		#floor da divisão do indice da aresta no array por 3
		def he_origem():
			pass
		#Origem da aresta:
		#valor do ponto no índice do array que guarda as arestas

		#destino/proxima da aresta:
		#3*(floor da divisão do indice da aresta no array por 3) + (aresta+1)mod3

		#aresta oposta:
		# eu posso checar na hora de chamar a função de triangulação se a oposta já está no array de faces de triangulos
		#eu posso achar se o ponto oposto tá incluso e chamo a função de destino para saber se o destino é o ponto que já temos
		#se sim, não adicionamos na fila de arestas.


#temos que saber se a half-edge já ta no fecho convexo ou se ela ja possui oposta... 
#se sim, nao dar append na lista de triangulos...

#mouse para criar os pontos
def mouse(button, state, x, y):

	#clique principal para desenhar o ponto na tela
	if button == GLUT_LEFT_BUTTON:
		if state == GLUT_DOWN:            
			xx = ((x / float(width)) - 0.5) * 2.0
			yy= (0.5 - (y / float(height))) * 2.0            
			ponto = Ponto(xx, yy)
			array_pontos.append(ponto)

	# Repaint screen
	glutPostRedisplay()


# controle do teclado
def keyboard(bkey, x, y):
	# paranaue do python pra converter objeto bytes pra string 
	key = bkey.decode("utf-8") #senao nao pega a teclinha pra fechar
	# tecla esc encerra o programa
	if key == chr(27):
		sys.exit()
	# para iniciar o fecho convexo, tecla F maiuscula
	elif key == chr(70):
		global fecho_convex
		fecho_convex = jarvis(array_pontos)
	#Para iniciar a triangulacao tecla T maiuscula
	elif key == chr(84):
		global triang
		triang = delaunay(array_pontos)
		#global triangulacaodela
		#triangulacaodela = triangulacao_del(array_pontos, fecho_convex)
	else:
		print("Nao eh possivel fazer essa operação ainda, tente novamente")

#estrategia para realizar a tarefa:
#armazenar os pontos em uma lista (etapa 1) - done
#dado uma nuvem de pontos fazer o fecho convexo dessa nuvem (etapa 2) - done
#estrutura para armazenar a triangulação:
# (etapa 3) - done ????? conferir
#realizar a triangulação de delaunay (etapa 4) - 
#as arestas do fecho convexo são mão única, não vão entrar na fila


def orientacao_pontos(p0, p1, p2):
	#usamos o slope da reta para saber a sua orientação
	#a formula abaixo leva em conta os slopes das retas que ligam p0 a p1 e p1 a p2
	produto_pontos = ((p1.y - p0.y) * (p2.x - p1.x)) - ((p1.x - p0.x) * (p2.y - p1.y))
	if produto_pontos == 0:
		return 0    # Colinear
	elif produto_pontos > 0:
		return 1    # sentido horario
	else:
		return 2    # sentido anti-horario

def prod_interno(p, q, r): #v0 e v1 são dois vetores
#aqui fazemos o produto interno do ponto candidato a terceiro ponto e o produto, onde q é o nosso ponto candidato
#e p e r são os dois pontos que já temos
	pq = (p.x * q.x) + (p.y * q.y)
	qr = (q.x * r.x) + (q.y * r.y)
	return pq + qr

def normalizeVector(a, b): #a e b são os pontos do vetor que queremos normalizar
	print(sqrt(pow(b.x-a.x, 2) + pow(b.y-a.y, 2)))
	return sqrt(pow(b.x-a.x, 2) + pow(b.y-a.y, 2))

def maiorAngulo(p, q, r): #retorna um valor de cosseno de theta
	#cos = <v1, v2>/norm(v1)*norm(v2) isso nos retorna um número... queremos que esse número esteja entre -1 e 1
	dividendo = (normalizeVector(p, q) * normalizeVector(q, r))
	produtinho = prod_interno(p, q, r)
	if dividendo == 0.0:
		print("entrei")
		dividendo = 1
		produtinho = 1
	print ("mudei!!!", dividendo, produtinho)
	result = produtinho/dividendo
	print result
	return result




#Algoritmo de Jarvis (Jarvis March) fecho convexo
def jarvis(pontos):
	aberto = True #variavel para fazer iteracao no loop para dar a volta no fecho
	n_pontos = len(pontos)     # pontos que estão no emaranhado
	guarda_pontos = []   #array para guardar os pontos

	#agora precisamos achar o ponto mais à esquerda no eixo x
	esquerda = 0
	for pontinho in range(n_pontos):
		if pontos[pontinho].x < pontos[esquerda].x: #pontos no eixo x
			esquerda = pontinho
	pnt = esquerda

	#depois que achamos o ponto mais a esquerda, iremos seguir no sentido
	#anti-horario até retornar o ponto inicial e assim fazer o fecho
	while aberto==True:
	#adicionamos o ponto atual na lista
		guarda_pontos.append(pontos[pnt])

		p1 = (pnt + 1) % n_pontos
		for k in range(n_pontos):
			# vamos usar a orientacao dos pontos para saber quem esta no sentido anti-horario
			#e assim atualizar nosso p1
			if orientacao_pontos(pontos[pnt], pontos[k], pontos[p1]) == 2:
				p1 = k
		#preparamos o próximo ponto na nova iteração para manter o sentido
		pnt = p1 
		#testando se voltamos ao ponto inicial
		if pnt == esquerda:
			guarda_pontos.append(pontos[esquerda])
			aberto = False #saímos do loop do fecho convexo
	return guarda_pontos

def delaunay(pontos):
	global fecho_convex
	# Fecho convexo
	fecho_convex = jarvis(pontos)
	# Fila de arestas
	fila = fecho_convex[0:2]
	# Lista de triangulações
	halfEdge = []
	cosseno = 1
	for i in xrange(0,len(fila),2): #andando de dois em dois pontos na fila, (de aresta em aresta)
		for j in xrange(0, len(pontos), 1):
			cos = maiorAngulo(fila[i], pontos[j], fila[i+1])
			if  cos < cosseno:
				p = pontos[j] 
				halfEdge.append(fila[i])
				halfEdge.append(p)
				halfEdge.append(fila[i+1])
		#checando se os pontos que formam a aresta nova(voltando) já existem no fecho convexo ou se já estão na fila
		#se nao estiverem podemos add na nossa fila
		if (p not in fecho_convex and fila[i+1] not in fecho_convex) or (p not in halfEdge and fila[i+1] not in halfEdge):
			fila.append(p)
			fila.append(fila[i+1])
		elif (fila[i] not in fecho_convex and p not in fecho_convex) or (fila[i] not in halfEdge and p not in halfEdge):
			fila.append(fila[i])
			fila.append(p)
	return halfEdge


# def triangulacao_del(pontos, fecho_convexo):
# 	#temos a primeira aresta do fecho convexo, dela vamos achar o terceiro ponto pra fechar o triangulo
# 	#esse terceiro ponto vamos achar buscando o que faz o maior angulo acontecer, depois armazenamos as duas arestas
# 	#novas formadas numa fila para então continuarmos a triangulacao
# 	cosseno_menor = 1 #aqui vamos atualizar.. quanto menor o cosseno maior o angulo formado
# 	#então a gente começa pelo maior cosseno possível, i.e., menor ângulo
# 	global fila_de_arestas
# 	cos = 1
# 	p = None 
# 	fila_de_arestas = [fecho_convexo[0:2]] #copiando a primeira aresta do fecho para nossa fila (dois primeiros pontos)
# 	for point in pontos:
# 		if maior_angulo(fila_de_arestas[0], point, fila_de_arestas[1]) < cos
# 			cos = maior_angulo(fila_de_arestas[0], point, fila_de_arestas[1])
# 			p = point
# 	fila_de_arestas.append(p)
# 	fila_de_arestas.append([0])
# 	return


	# Desenhamos a tela e desenhamos os pontos e retas
def display():
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClear(GL_COLOR_BUFFER_BIT)
	glColor3f(0.5, 0.5, 0.5)
	glPointSize(4.0)
	glLineWidth(2)
	#glPointSize(3.50)
	glBegin(GL_POINTS)
	for ponto in array_pontos:
		glColor3f(0.99, 0.49, 0.61)
		glVertex2d(ponto.x, ponto.y)
	glEnd()

	glBegin(GL_LINE_STRIP)
	for ponto in fecho_convex:
		ponto.criaAresta()
	glEnd()

	# glBegin(GL_LINE_STRIP)
	# for ponto in fila_de_arestas:
	# 	ponto.criaAresta()
	# glEnd()
	glBegin(GL_TRIANGLE_STRIP)
	for item in triang:
		#item.criaAresta()
		glVertex2d(item.x, item.y)
		#glVertex2d((item+1).x, (item+1).y)
		#glVertex2d((item+2).x, (item+2).y)
	# for item in xrange(0, len(triang), 3):	
	# 	glVertex2d(item)
	# 	glVertex2d(item+1)
	# 	glVertex2d(item+2)
	glEnd()


	glutPostRedisplay()
	glutSwapBuffers()
	glFlush()



def main():
	glutInit(sys.argv)
	glutInitWindowSize(width, height)
	glutCreateWindow("Trabalho 4")
	glutMouseFunc(mouse)    
	glutKeyboardFunc(keyboard)
	glutDisplayFunc(display)
	glutMainLoop()


# Call the main function
if __name__ == '__main__':
	main()
