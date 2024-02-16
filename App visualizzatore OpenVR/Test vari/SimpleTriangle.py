

# file color_cube_actor.py
import numpy

from textwrap import dedent

from OpenGL.GL import *  # @UnusedWildImport # this comment squelches an IDE warning
from OpenGL.GL.shaders import compileShader, compileProgram

from openvr.glframework import shader_string

"""
Color cube for use in "hello world" openvr apps
"""


class SimpleTriangle(object):
    """
    Draws a triangle

    """
    vertices= [
         [0.5, -0.5, 0.0], # bottom right
        [-0.5, -0.5, 0.0],  # bottom left
         [0.0,  0.5, 0.0]   # top 
    ]

    def __init__(self):
        self.shader = 0
        self.vao = None
        self.vbo = None
        self.vertices= [
         [0.5, -0.5, 0.0], # bottom right
        [-0.5, -0.5, 0.0],  # bottom left
         [0.0,  0.5, 0.0]   # top 
         ]
    
    def init_gl(self):
        vertex_shader = compileShader(
            shader_string("""
            
            
            layout(location = 0) uniform mat4 Projection = mat4(1);
            layout(location = 4) uniform mat4 ModelView = mat4(1);
            
            
            layout(location = 8) in vec3 aPos;
            
            
            
            void main() {
             
              
            
              gl_Position = Projection * ModelView * vec4(aPos* 0.3, 1.0);
            }
            """), 
            GL_VERTEX_SHADER)
        fragment_shader = compileShader(
            shader_string("""
            out vec4 FragColor;
            
            void main() {
              FragColor = vec4(1.0, 0.0, 0.0, 1.0);
            }
            """), 
            GL_FRAGMENT_SHADER)

        success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS);
        print(success)
        print(glGetShaderInfoLog(vertex_shader))
        success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS);
        print(success)
        self.shader = compileProgram(vertex_shader, fragment_shader)
        error=glGetError()
        if error != 0:
            print(glGetError())
        success=0
        success = glGetProgramiv(self.shader, GL_LINK_STATUS);
        print(success)
        print(glGetProgramInfoLog(self.shader))

        self.vao = glGenVertexArrays(1)
        self.vbo=glGenBuffers(1)
        glBindVertexArray(self.vao)
        #print(sizeof(GLfloat))
        print(self.vertices)
        
        vertices_array=numpy.array(self.vertices)

        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices_array.size * vertices_array.itemsize, vertices_array, GL_STATIC_DRAW)

        posAttrib = glGetAttribLocation(self.shader, "aPos")
        print(posAttrib)
        glVertexAttribPointer(posAttrib, 3, GL_FLOAT, GL_FALSE, 3 * vertices_array.itemsize, 0);
        glEnableVertexAttribArray(posAttrib);
        glEnable(GL_DEPTH_TEST)

    def display_gl(self, modelview, projection):
        print("vao:")
        print(vao)
        print("vbo:")
        print(vbo)
        glUseProgram(self.shader)
        glUniformMatrix4fv(0, 1, False, projection)
        glUniformMatrix4fv(4, 1, False, modelview)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        glDrawArrays(GL_TRIANGLES, 0, 9)
    
    def dispose_gl(self):
        glDeleteProgram(self.shader)
        self.shader = 0
        if self.vao:
            glDeleteVertexArrays(1, (self.vao,))
        self.vao = 0