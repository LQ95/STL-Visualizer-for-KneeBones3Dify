

# file color_cube_actor.py
import numpy
import ctypes
import time
import math
import multiprocessing
import queue
import sys
from textwrap import dedent

from OpenGL.GL import *  # @UnusedWildImport # this comment squelches an IDE warning
from OpenGL.GL.shaders import compileShader, compileProgram

from openvr.glframework import shader_string
from controlModule import controlInputModule
from TextureControl import TextureControl
#global variables
controlMod= None
menu_width=900
texControl= TextureControl(menu_width)
texture_proc_done = multiprocessing.Value(ctypes.c_bool,False)
texture_proc_generate = multiprocessing.Value(ctypes.c_bool,False)
processOver= multiprocessing.Value(ctypes.c_bool,False)
texture_is_loading= multiprocessing.Value(ctypes.c_bool,False)
#menu_tex= None

shared_queue= multiprocessing.Queue(maxsize=2)

#this is the subroutine that the subprocess executes
def tex_modify_proc_routine(shared_queue, texture_proc_done, texture_proc_generate,processOver,menu_width,texture_is_loading):
    
    #setup
    texControl= TextureControl(menu_width)
    rerendering_has_been_flagged= False
    status = None

    #htis is necessary to have the menu texture look correct
    menu_dict= {}
    menu_dict['intensity_threshold'] = 600
    menu_dict['convex_hull_dilation'] = 6
    menu_dict['final_closing'] = 8
    menu_dict['protrusion_removal'] = 3
    menu_dict['final_dilation'] = 1
    texControl.generateTexture(menu_dict,'intensity_threshold')
    
    #ciclo
    while(1):
        #print("subprocesso avviato, flag generazione: ",file=sys.stderr)
        #print(texture_proc_generate.value,file=sys.stderr)
        #print("subprocesso avviato, flag processOver: ",file=sys.stderr)
        #print(processOver.value,file=sys.stderr)
        
            
        
        if(texture_proc_generate.value  == True):
            #print("the sub-process is generating a texture",file=sys.stderr)

            #print("queue size before extracting user input:",file=sys.stderr)
            #print(shared_queue.qsize(),file=sys.stderr)
            
            received=shared_queue.get()
            status= received[0]
            selected_param= received[1]
            #print("status:",file=sys.stderr)
            #print(status,file=sys.stderr)
            
            #print("parametro selezionato:",file=sys.stderr)
            #print(selected_param,file=sys.stderr)
            
            #we set this shared value true 
            #this way, the rendering routine can't send anything, 
            #while we're still modifying the texture here

            texture_is_loading.value = True

            if(status['re-rendering'] == True):
                if(rerendering_has_been_flagged == False):
                    texControl.flagRerendering()
                    rerendering_has_been_flagged = True
            menu_tex= texControl.modifyTexture(status,selected_param)
            
            
            #print("queue size before putting a texture on it:",file=sys.stderr)
            #print(shared_queue.qsize(),file=sys.stderr)

            shared_queue.put(menu_tex)
            texture_proc_done.value= True
            texture_proc_generate.value= False
        if (status!= None):

            if(status['re-rendering'] == False):
                if(rerendering_has_been_flagged == True):
                    texture_is_loading.value = True
                    menu_tex = texControl.unflagRerendering()
                    rerendering_has_been_flagged = False
                    shared_queue.put(menu_tex)
                    texture_proc_done.value= True


texture_modifying_process = multiprocessing.Process(target=tex_modify_proc_routine, args = (shared_queue, texture_proc_done, texture_proc_generate, processOver,menu_width,texture_is_loading ))
"""
Menu for the STL Visualizer app
"""


class MenuScreen(object):
    """
    Draws the menu

    """
    



    


    def __init__(self,control_mod):
        global controlMod,texControl,menu_width
        
        self.shader = 0
        self.vao = None
   
        
        self.menu_texture= None
        #self.pixel_buffer= None
        #self.mapped_pixel_buffer = None 
        self.tex = None 
        self.width=menu_width
        self.height=math.ceil(self.width/1.57)
        controlMod=control_mod
        
        
    
    def init_gl(self):
        global texture_modifying_process
        vertex_shader = compileShader(
            shader_string("""
            
            
            layout(location = 0) uniform mat4 Projection = mat4(1);
            layout(location = 4) uniform mat4 ModelView = mat4(1);
            
            

            const vec3 vertices[4] = vec3[4](
              vec3(-0.45, 0.5, -0.5), // 0: lower left rear
              vec3(+0.45, 0.5, -0.5), // 1: lower right rear
              vec3(-0.45, +1.5, -0.5), // 2: upper left rear
              vec3(+0.45, +1.5, -0.5) // 3: upper right rear
            );
            
            const vec2 texCoords[4]= vec2[4](
            vec2(0.0, 1.0), // 0: lower left rear
            vec2(1.0, 1.0), // 1: lower right rear
            vec2(0.0, 0.0), // 2: upper left rear
            vec2(1.0, 0.0) // 3: upper right rear

            );

           

            out vec2 texCoord; 
            
            void main() {
             
             
              texCoord=texCoords[gl_VertexID];
              gl_Position = Projection * ModelView * vec4(vertices[gl_VertexID] , 1.0);
            }
            """), 
            GL_VERTEX_SHADER)
        fragment_shader = compileShader(
            shader_string("""
            out vec4 FragColor;
            uniform sampler2D Tex;
            in vec2 texCoord;

    
            void main() {
              //FragColor =  vec4(0.5,0.0,0.9,1.0);
              FragColor = texture(Tex, texCoord);
            }
            """), 
            GL_FRAGMENT_SHADER)

        #success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS);
        #print("vertex:",file=sys.stderr)
        #print(success,file=sys.stderr)
        #print(glGetShaderInfoLog(vertex_shader),file=sys.stderr)
        #success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS);
        #print("fragment:",file=sys.stderr)
        #print(success,file=sys.stderr)
        #print(glGetShaderInfoLog(fragment_shader),file=sys.stderr)
        #print("program:",file=sys.stderr)
        
        self.shader = compileProgram(vertex_shader, fragment_shader)
        #glGetProgramInfoLog(self.shader)
        error=glGetError()
        if error != 0:
            print(glGetError(),file=sys.stderr)
        #success=0
        #success = glGetProgramiv(self.shader, GL_LINK_STATUS);
        #print(success,file=sys.stderr)
        #print(glGetProgramInfoLog(self.shader),file=sys.stderr)

        self.vao = glGenVertexArrays(1)
        
        glBindVertexArray(self.vao)
        #print(sizeof(GLfloat),file=sys.stderr)
        
        
        glEnable(GL_DEPTH_TEST)   

        #initializing a texture
        self.menu_texture = glGenTextures(1)
        #print("generating texture name:",file=sys.stderr)
        #print(self.menu_texture,file=sys.stderr)
        
        self.tex = texControl.generateTexture(controlMod.menuStatus.menu_dict,'intensity_threshold')
        
        #this instruction was used when the menu was rendered as a grayscale image visualized using the GL_RED mode
        #if you decide to do that again this needs to be uncommented
        #currently commented because the menu is a RGBA image right now
        #glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        
        glBindTexture(GL_TEXTURE_2D, self.menu_texture)
        #the GL_RGBA8 internal format is necessary to visualize the app logo correctly in the menu
        #if the image is generated in RGBA mode like it is now
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8,self.width,self.height,0,GL_RGBA,GL_UNSIGNED_BYTE,self.tex)
        

        #this instruction can be used for a possible performance increase if the image is generated in 8 bit grayscale
        #glTexImage2D(GL_TEXTURE_2D, 0, GL_R8,self.width,self.height,0,GL_RED,GL_UNSIGNED_BYTE,self.tex)
        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        

        self.pixel_buffer=glGenBuffers(1)
        #glBindBuffer(GL_PIXEL_UNPACK_BUFFER,self.pixel_buffer)
        #glBufferData(GL_PIXEL_UNPACK_BUFFER,1100*700*16, None, GL_STREAM_DRAW)
        #glBindBuffer(GL_PIXEL_UNPACK_BUFFER,0)
        
        #starts a sub process that modifies textures 
        #implement the visual part of the interaction with the menu

        texture_modifying_process.start()
        time.sleep(3)

    def display_gl(self, modelview, projection):
        global shared_queue,menu_tex,texture_proc_generate,texture_proc_done,texture_is_loading
        

        status,selected_param=controlMod.menuControl()

        if(status['enabled']):
            #print("menu is visible",file=sys.stderr)
            glUseProgram(self.shader)
            glUniformMatrix4fv(0, 1, False, projection)
            glUniformMatrix4fv(4, 1, False, modelview)
            glBindVertexArray(self.vao)
            
            
            glBindTexture(GL_TEXTURE_2D, self.menu_texture)


           

            if(status['modified'] and texture_is_loading.value == False ):

                #print("sending menu status data and the selected menu parameter in the queue",file=sys.stderr)
               
                shared_queue.put([status,selected_param])
                
                texture_proc_generate.value=True
                #this variable will be modified once the sub process is done modifying the texture
                
                
            #load the texture once the subprocess signals that it's done with it
            if(texture_proc_done.value == True):
                print("sub-process is done modifying the texture",file=sys.stderr)
                self.tex=shared_queue.get()
                texture_is_loading.value = False
                glTexSubImage2D(GL_TEXTURE_2D, 0,0,0,self.width,self.height,GL_RGBA,GL_UNSIGNED_BYTE,self.tex)
                

                #glTexSubImage2D(GL_TEXTURE_2D, 0,0,0,self.width,self.height,GL_RED,GL_UNSIGNED_BYTE,self.tex)
                
                texture_proc_done.value=False

               

                
            


            glDrawArrays(GL_TRIANGLE_STRIP,0, 4);
            
            error=glGetError()
            if error != 0:
                print(error,file=sys.stderr)
            glBindTexture(GL_TEXTURE_2D, 0)

            

    
    def dispose_gl(self):
        global processOver
        processOver.value=True
        texture_modifying_process.join()
        glDeleteProgram(self.shader)
        #glUnmapBuffer(GL_PIXEL_UNPACK_BUFFER);
        self.shader = 0
        if self.vao:
            glDeleteVertexArrays(1, (self.vao,))
        self.vao = 0