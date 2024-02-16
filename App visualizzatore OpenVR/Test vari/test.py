import time
import sdl2
import openvr
import numpy

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from openvr.glframework import shader_string
from openvr.gl_renderer import OpenVrGlRenderer
from openvr.tracked_devices_actor import TrackedDevicesActor
from sdl2 import *

# see https://github.com/cmbruns/pyopenvr

from STLinto3DModel import STLloader
loader=STLloader()
loader.load_stl('C:\\Users\\mrapo\\AppData\\Local\\Temp\\MRI.stl')
model=loader.model 



class OpenVRTest(object):
  "Tiny OpenVR example with python (based on openvr example)"

  def __init__(s):
    s.vr_system = openvr.init(openvr.VRApplication_Scene)
    s.vr_compositor = openvr.VRCompositor()
    poses_t = openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount
    s.poses = poses_t()
    s.w, s.h = s.vr_system.getRecommendedRenderTargetSize()
    SDL_Init(SDL_INIT_VIDEO)
    s.window = SDL_CreateWindow (b"test",
      SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
      100, 100, SDL_WINDOW_SHOWN|SDL_WINDOW_OPENGL)
    s.context = SDL_GL_CreateContext(s.window)
    SDL_GL_MakeCurrent(s.window, s.context)
    
    # glNewList(1, GL_COMPILE) #glNewList è un comando che permette di caricare una lista comandi OPenGL in un intero,per poi farli eseguire dopo.
    # for m in model.meshes:
    #   print(dir(m))
    #   print("\n")
    #   print(m.num_vertices)
    #   print(len(m.indices))
    #   print(len(m.normals))
    #   print(len(m.colors))
    #   i=0
    #   print (min(m.vertices))
    #   print (max(m.vertices))
        
      
      
      

    #   glBegin(GL_TRIANGLES)
    #   glColor3f(0,0,0)

    #   for i in range(m.num_vertices):
    #     glNormal3f(m.normals[i][0],m.normals[i][1],m.normals[i][2])
    #     glVertex3f(m.vertices[i][0],m.vertices[i][1],m.vertices[i][2])
                
                
    #   glEnd()    

    # glEndList()
    s.depth_buffer = glGenRenderbuffers(1)
    s.frame_buffers = glGenFramebuffers(2)
    s.texture_ids = glGenTextures(2)
    s.textures = [None] * 2
    s.eyes = [openvr.Eye_Left, openvr.Eye_Right] 
    s.cameraToProjection = [None] * 2
    s.headToCamera = [None] * 2
    s.col3 = [0, 0, 0, 1]
    success=0
    vertexShader = compileShader(
      shader_string(
        """
          layout (location=0) uniform mat4 cameraToProjection;
          layout (location=1) uniform mat4 modelToCamera;
          in vec3 position;
          

          void main() {
            float angle = gl_VertexID * (3.14159*1/9);
            vec4 modelPos = vec4(position.x/100, position.y/100, position.z/100, 1);
            gl_Position = cameraToProjection * (modelToCamera * modelPos); 
  
          }
        """
      ),# gestisce anche la proiezione
      GL_VERTEX_SHADER
    )
    fragmentShader = compileShader(
      shader_string(
        """
          out vec4 colour;
          void main() {
            colour = vec4(1, 0.5, 0, 1);
          }
        """
      ),
      GL_FRAGMENT_SHADER
    )
    success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS);
    print(success)
    success = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS);
    print(success)
    s.program = compileProgram(fragmentShader,vertexShader)
    success = glGetProgramiv(s.program, GL_LINK_STATUS);
    print(success)
    error=glGetError()
    if error != 0:
      print(glGetError())
        
    s.vertexBuffer = glGenVertexArrays(1)
    glBindVertexArray(s.vertexBuffer)
    s.array_buffer=glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,s.array_buffer)
    glBufferData(GL_ARRAY_BUFFER, model.meshes[0].num_vertices * sizeof(GLfloat*3), numpy.array(model.meshes[0].vertices,numpy.float32), GL_STATIC_DRAW)

    posAttrib = glGetAttribLocation(s.program, "position")
    glEnableVertexAttribArray(posAttrib);
    glVertexAttribPointer(posAttrib, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), 0);
    

    for eye in range(2):
      glBindFramebuffer(GL_FRAMEBUFFER, s.frame_buffers[eye])
      glBindRenderbuffer(GL_RENDERBUFFER, s.depth_buffer)
      glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, s.w, s.h)
      glFramebufferRenderbuffer(
        GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER,
        s.depth_buffer)
      glBindTexture(GL_TEXTURE_2D, s.texture_ids[eye])
      glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA8, s.w, s.h, 0, GL_RGBA, GL_UNSIGNED_BYTE,
        None)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glFramebufferTexture2D(
        GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D,
        s.texture_ids[eye], 0)
      texture = openvr.Texture_t()
      texture.handle = int(s.texture_ids[eye])
      texture.eType = openvr.TextureType_OpenGL
      texture.eColorSpace = openvr.ColorSpace_Gamma
      s.textures[eye] = texture
      proj = s.vr_system.getProjectionMatrix(s.eyes[eye], 0.2, 500.0)
      s.cameraToProjection[eye] = numpy.matrix(
        [ [proj.m[i][j] for i in range(4)] for j in range(4) ],
        numpy.float32
      )
      camToHead = s.vr_system.getEyeToHeadTransform(s.eyes[eye])
      s.headToCamera[eye] = numpy.matrix(
        [ [camToHead.m[i][j] for i in range(3)] + [s.col3[j]] for j in range(4) ],
        numpy.float32
      ).I

  def draw(s):
    s.vr_compositor.waitGetPoses(s.poses, openvr.k_unMaxTrackedDeviceCount)
    headPose = s.poses[openvr.k_unTrackedDeviceIndex_Hmd]
    if not headPose.bPoseIsValid:
      return True

    headToWorld = headPose.mDeviceToAbsoluteTracking
    worldToHead =  numpy.matrix(
      [ [headToWorld.m[i][j] for i in range(3)] + [s.col3[j]] for j in range(4) ],
      numpy.float32
    ).I

    for eye in range(2):
      modelToCamera = s.headToCamera[eye] * worldToHead

      glBindFramebuffer(GL_FRAMEBUFFER, s.frame_buffers[eye])
      glClearColor(0.5, 0.5, 0.5, 0.0)
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glViewport(0, 0, s.w, s.h)
      
      
      
      glEnable(GL_DEPTH_TEST)
      
      glUseProgram(s.program)
      glUniformMatrix4fv(0, 1, False, numpy.asarray(s.cameraToProjection[eye])) #credo che queste due chiamate vogliano dati dagli shader
      glUniformMatrix4fv(1, 1, False, numpy.asarray(modelToCamera))
      # print("cameraToProjection:")
      # print(numpy.asarray(s.cameraToProjection[eye]))
      # print("modelToCamera:")
      # print(numpy.asarray(modelToCamera))
      error=glGetError()
      if error != 0:
        print(glGetError())
      #glDrawArrays(GL_TRIANGLES, 0, 15)
      
      glDrawArrays(GL_TRIANGLES, 0, model.meshes[0].num_vertices)
      #glCallList(1) 
      s.vr_compositor.submit(s.eyes[eye],s.textures[eye])
    return True

if __name__ == "__main__":
  print("kill with ctrl-C (no frills here!)")
  test = OpenVRTest()
  while test.draw():
    pass