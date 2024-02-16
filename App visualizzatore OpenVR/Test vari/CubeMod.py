import numpy
import itertools
import ctypes

from textwrap import dedent

from OpenGL.GL import *  # @UnusedWildImport # this comment squelches an IDE warning
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileShader, compileProgram

from openvr.glframework import shader_string

"""
Color cube for use in "hello world" openvr apps
"""


class CubeMod(object):
    """
    Draws a cube
    
       2________ 3
       /|      /|
     6/_|____7/ |
      | |_____|_| 
      | /0    | /1
      |/______|/
      4       5
    """

    
    def __init__(self):
        self.shader = 0
        self.vao = None
        self.vao2 = None
        self.vbo = None
        self.vertices= [
        [-1.0, 0.0, -1.0,1.0], 
        [1.0, 0.0, -1.0,1.0],  
        [-1.0, 2.0, -1.0,1.0],
        [1.0, 2.0, -1.0,1.0], 
        [-1.0, 0.0, 1.0,1.0],  
        [1.0, 0.0, 1.0,1.0],
        [-1.0, 2.0, 1.0,1.0],
        [1.0, 2.0, 1.0,1.0]   
        ]
        self.vertices_iter=itertools.cycle(self.vertices)
    def init_gl(self): #trova un modo per caricare correttamente aPos!
        vertex_shader = compileShader( 
            shader_string("""
            // Adapted from @jherico's RiftDemo.py in pyovr
            
            layout(location = 0) uniform mat4 Projection = mat4(1);
            layout(location = 4) uniform mat4 ModelView = mat4(1);

            layout(std430, binding = 3) buffer positionBuffer
            {
                vec4 aPos[];
            };
            
            // Minimum Y value is zero, so cube sits on the floor in room scale
            const vec3 UNIT_CUBE[8] = vec3[8](
              vec3(-1.0, -0.0, -1.0), // 0: lower left rear
              vec3(+1.0, -0.0, -1.0), // 1: lower right rear
              vec3(-1.0, +2.0, -1.0), // 2: upper left rear
              vec3(+1.0, +2.0, -1.0), // 3: upper right rear
              vec3(-1.0, -0.0, +1.0), // 4: lower left front
              vec3(+1.0, -0.0, +1.0), // 5: lower right front
              vec3(-1.0, +2.0, +1.0), // 6: upper left front
              vec3(+1.0, +2.0, +1.0)  // 7: upper right front
            );
            
            const vec3 UNIT_CUBE_NORMALS[6] = vec3[6](
              vec3(0.0, 0.0, -1.0),
              vec3(0.0, 0.0, 1.0),
              vec3(1.0, 0.0, 0.0),
              vec3(-1.0, 0.0, 0.0),
              vec3(0.0, 1.0, 0.0),
              vec3(0.0, -1.0, 0.0)
            );
            
            const int CUBE_INDICES[36] = int[36](
              0, 1, 2, 2, 1, 3, // front
              4, 6, 5, 6, 5, 7, // back
              0, 2, 4, 4, 2, 6, // left
              1, 3, 5, 5, 3, 7, // right
              2, 6, 3, 6, 3, 7, // top
              0, 1, 4, 4, 1, 5  // bottom
            );
            
            out vec3 _color;
            vec4 final_pos;
            void main() {
              _color = vec3(1.0, 0.0, 0.0);
              int vertexIndex = CUBE_INDICES[gl_VertexID];
              int normalIndex = gl_VertexID / 6;
              
              _color = UNIT_CUBE_NORMALS[normalIndex];
              if (any(lessThan(_color, vec3(0.0)))) {
                  _color = vec3(1.0) + _color;
              }       
              
              final_pos.x=aPos[vertexIndex].x*0.3;
              final_pos.y=aPos[vertexIndex].y*0.3;
              final_pos.z=aPos[vertexIndex].z*0.3;
              final_pos.w=1.0;
              gl_Position = Projection * ModelView * final_pos;
            }
            """), 
            GL_VERTEX_SHADER)
        success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS);
        print("vertex success:")
        print(success)
        fragment_shader = compileShader(
            shader_string("""
            in vec3 _color;
            out vec4 FragColor;
            
            void main() {
              FragColor = vec4(_color, 1.0);
            }
            """), 
            GL_FRAGMENT_SHADER)
        self.shader = compileProgram(vertex_shader, fragment_shader)

        error=glGetError()
        if error != 0:
            print("compile:")
            print(gluErrorString(error))

        success=0
        success = glGetProgramiv(self.shader, GL_LINK_STATUS);
        print("link success:")
        print(success)

        self.vao2 = glGenVertexArrays(1)
        glBindVertexArray(self.vao2)

        vertices_array=numpy.array(self.vertices,dtype = numpy.float32)
        # self.vbo=glGenBuffers(1)
        # glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        # glBufferData(GL_ARRAY_BUFFER, vertices_array.size * vertices_array.itemsize, vertices_array, GL_STATIC_DRAW)

        # posAttrib = glGetAttribLocation(self.shader, "aPos")
        # error=glGetError()

        # if error != 0:
        #     print("Location:")
        #     print(gluErrorString(error))

        # print("posAttrib:")
        # print(posAttrib)

        # glEnableVertexAttribArray(posAttrib);
        # glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
        # glVertexAttribPointer(posAttrib, 3, GL_FLOAT, GL_FALSE, 3 * vertices_array.itemsize, 0);
        
        #self.vao = glGenVertexArrays(1)
        #glBindVertexArray(self.vao)

        ssbo=glGenBuffers(1)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, ssbo)
        print("size:")
        print(vertices_array.size)
        print("itemsize:")
        print(vertices_array.itemsize)
        glBufferData(GL_SHADER_STORAGE_BUFFER, vertices_array.size * vertices_array.itemsize, vertices_array, GL_STATIC_DRAW)
        glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 3, ssbo)
        glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)
        glEnable(GL_DEPTH_TEST)
        # print("vao(init):")
        # print(self.vao2)
        # print("vbo(init):")
        # print(self.vbo)
        # glUseProgram(self.shader)
        # glUniform3fv(8,6,self.vertices)
        
    def display_gl(self, modelview, projection):
        glUseProgram(self.shader)
        glUniformMatrix4fv(0, 1, False, projection)
        glUniformMatrix4fv(4, 1, False, modelview)
        # elem=next(self.vertices_iter)
        # glUniform3f(8,elem[0],elem[1],elem[2])
        glBindVertexArray(self.vao2)

        # vertices_array=numpy.array(self.vertices,dtype = numpy.float32)
        # posAttrib = glGetAttribLocation(self.shader, "aPos")
        # glEnableVertexAttribArray(posAttrib);
        # glBindBuffer(GL_ARRAY_BUFFER,self.vbo)
 
        # glVertexAttribPointer(posAttrib, 3, GL_FLOAT, GL_FALSE, 0, 0);
        # print("vao:")
        # print(self.vao2)
        # print("vbo:")
        # print(self.vbo)
        glDrawArrays(GL_TRIANGLES, 0, 36)

        # glDisableVertexAttribArray(posAttrib);


    def dispose_gl(self):
        glDeleteProgram(self.shader)
        self.shader = 0
        if self.vao:
            glDeleteVertexArrays(1, (self.vao,))
        self.vao = 0



        #         print("buffer size:")
        # ptr = glMapBuffer(GL_ARRAY_BUFFER, GL_READ_WRITE)
        # size = glGetBufferParameteriv(GL_ARRAY_BUFFER, GL_BUFFER_SIZE)
        # a = numpy.ctypeslib.as_array(ctypes.cast(ptr, ctypes.POINTER(ctypes.c_float)),
        #                        shape=(size, ))
        # print(a)