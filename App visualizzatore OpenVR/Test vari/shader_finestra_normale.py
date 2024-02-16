import numpy
import itertools
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from OpenGL.GL import shaders

vertex_s=0

fragment_s=0

vbo= None
vao= None
w,h= 500,500
def on_Init:
      global vertex_s,fragment_s,vbo,vao
      vertex_s = shaders.compileShader(
            """
            uniform mat4 projectionMatrix;
            uniform mat4 modelViewMatrix;
            in vec2 vertex_pos;
            void main() {
                gl_Position = projectionMatrix * modelViewMatrix * vertex_pos;
            }""",GL_VERTEX_SHADER)
      fragment_s = shaders.compileShader("""
            varying vec4 vertex_color;
            void main() {
                gl_FragColor = vertex_color;
            }""",GL_FRAGMENT_SHADER)
      vao = glGenVertexArrays(1)
      vbo=glGenBuffers(1)
      glBindVertexArray(self.vao)
           
      #print(self.vertices)
        
      vertices_array=numpy.array(vertices)

      glBindBuffer(GL_ARRAY_BUFFER,vbo)
      glBufferData(GL_ARRAY_BUFFER, vertices_array.size * vertices_array.itemsize, vertices_array, GL_STATIC_DRAW)

      posAttrib = glGetAttribLocation(shader, "vertex_Pos")
      print(posAttrib)
      glVertexAttribPointer(posAttrib, 2, GL_FLOAT, GL_FALSE, 2 * vertices_array.itemsize, 0);
      glEnableVertexAttribArray(posAttrib);
      glEnable(GL_DEPTH_TEST)     

def square():
    glBegin(GL_QUADS)
    glVertex2f(100, 100)
    glVertex2f(200, 100)
    glVertex2f(200, 200)
    glVertex2f(100, 200)
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glUniformMatrix4fv(0, 1, False, numpy.asarray(glGetfloatv(GL_PROJECTION_MATRIX))) #credo che queste due chiamate vogliano dati dagli shader
    glUniformMatrix4fv(1, 1, False, numpy.asarray(glGetfloatv(GL_MODELVIEW_MATRIX)))
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 0.0, 3.0)
    square()
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMainLoop()