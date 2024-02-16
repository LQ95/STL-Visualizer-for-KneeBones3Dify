from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from STLinto3DModel import STLloader
loader=STLloader()
loader.load_stl('C:\\Users\\mrapo\\AppData\\Local\\Temp\\MRI.stl')
model=loader.model 

name = "Hello, World"
height = 500
width = 500
rotate = 0
beginx = 0.
beginy = 0.
rotx = 0.
roty = 0.

def display(): #Questa è la routine che effettivamente disegna
     glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
     glLoadIdentity()
     gluLookAt(-30,0,160,90,47,45,0,1,0) #mettersi a distanza (modificando il 10, presumibilmente aumentando)
     glRotatef(roty,0,1,0)
     glRotatef(rotx,1,0,0)
     glCallList(1) 
     glutSwapBuffers()
     return

def mouse(button,state,x,y):
     global beginx,beginy,rotate
     if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
         rotate = 1
         beginx = x
         beginy = y
     if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
         rotate = 0
     return

def motion(x,y):
     global rotx,roty,beginx,beginy,rotate
     if rotate:
         rotx = rotx + (y - beginy)
         roty = roty + (x - beginx)
         beginx = x
         beginy = y
         glutPostRedisplay()
     return

def keyboard(a,b,c):
     return

glutInit(name)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(height,width)
glutCreateWindow(name)
glClearColor(0., 0., 0., 1.)

# setup display list
glNewList(1, GL_COMPILE) #glNewList è un comando che permette di caricare una lista comandi OPenGL in un intero,per poi farli eseguire dopo.
for m in model.meshes:
    print(dir(m))
    print("\n")
    print(m.num_vertices)
    print(len(m.indices))
    print(len(m.normals))
    print(len(m.colors))
    i=0
    print (min(m.vertices))
    print (max(m.vertices))
        



    glBegin(GL_TRIANGLES)

    for i in range(m.num_vertices):
        glNormal3f(m.normals[i][0],m.normals[i][1],m.normals[i][2])
        glVertex3f(m.vertices[i][0],m.vertices[i][1],m.vertices[i][2])
                
                
    glEnd()    

glEndList()

#setup lighting
glEnable(GL_CULL_FACE)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
lightZeroPosition = [10., 4., 10., 1.]
lightZeroColor = [1, 1.0, 1, 1.0] # greenish
glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.02)
glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.02)
glEnable(GL_LIGHT0)

#setup cameras
glMatrixMode(GL_PROJECTION)
gluPerspective(40., 1., 1., 1240.)
glMatrixMode(GL_MODELVIEW)
gluLookAt(0,0, 760,-70, 0, 0, 0, 1, 0)   
glPushMatrix()

#setup callbacks
glutDisplayFunc(display)
glutMouseFunc(mouse)
glutMotionFunc(motion)
glutKeyboardFunc(keyboard)

glutMainLoop()