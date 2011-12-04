 # ############################################################################
 #
 # Copyright (c) Microsoft Corporation. 
 #
 # Available under the Microsoft PyKinect 1.0 Alpha license.  See LICENSE.txt
 # for more information.
 #
 # ###########################################################################
 # Simple kinect game.
 # Use right hand skeleton input to and bring it closer to the yellow circle.
 ############################################################################

import thread
import itertools
import ctypes

import pykinect
from pykinect import nui
from pykinect.nui import JointId

import pygame
from pygame.color import THECOLORS
from pygame.locals import *

import random
import datetime

KINECTEVENT = pygame.USEREVENT
DRAWRANDOMCIRCLEEVENT = pygame.USEREVENT +1
ENDGAMEEVENT = pygame.USEREVENT + 2
DISPLAYSCOREEVENT = pygame.USEREVENT + 3
DEPTH_WINSIZE = 320,240
VIDEO_WINSIZE = 640,480
pygame.init()

SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)
RIGHT_WRIST = (JointId.WristRight,JointId.HandRight)
LEFT_WRIST = (JointId.WristLeft,JointId.HandLeft)

score = 0

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

def draw_skeleton_data(pSkelton, index, positions, width = 4):
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

# recipe to get address of surface: http://archives.seul.org/pygame/users/Apr-2008/msg00218.html
if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
   Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
   Py_ssize_t = ctypes.c_int64
else:
   raise TypeError("Cannot determine type of Py_ssize_t")

_PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
_PyObject_AsWriteBuffer.restype = ctypes.c_int
_PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                  ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.POINTER(Py_ssize_t)]

def surface_to_array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   _PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes

def draw_skeletons(skeletons):
 
    for index, data in enumerate(skeletons):
        # draw the Head
        HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
        #draw_skeleton_data(data, index, SPINE, 10)
       # pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
        #HandLeft = skeleton_to_depth_image(data.SkeletonPositions[JointId.HandLeft], dispInfo.current_w, dispInfo.current_h)
        HandRight = skeleton_to_depth_image(data.SkeletonPositions[JointId.HandRight], dispInfo.current_w, dispInfo.current_h)
        #pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HandLeft[0]), int(HandLeft[1])), 20, 0)    
        pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HandRight[0]), int(HandRight[1])), 20, 0)

        update_score()

        return int(HandRight[0]),int(HandRight[1])
            
        # drawing the limbs
        #draw_skeleton_data(data, index, LEFT_ARM)
        #draw_skeleton_data(data, index, RIGHT_ARM)
        #draw_skeleton_data(data, index, LEFT_LEG)
        #draw_skeleton_data(data, index, RIGHT_LEG)
        #draw_skeleton_data(data, index, RIGHT_WRIST)
        #draw_skeleton_data(data, index, LEFT_WRIST)


def depth_frame_ready(frame):
    if video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        ctypes.memmove(address, frame.image.contents.bits, len(address))
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()    


def video_frame_ready(frame):
    if not video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        ctypes.memmove(address, frame.image.contents.bits, len(address))
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()

def draw_random_circle(x,y,rhx,rhy):
    global score
    if(abs(rhx - x) < 20 & abs(rhy-y) < 20):
        score += 100
        print "Score:", score
        x = random.randint(100,600)
        y = random.randint(100,450)
    with screen_lock:
        pygame.draw.circle(screen, SKELETON_COLORS[5], (x,y), 20, 0)
    return x,y

def update_score():
    global score
    font = pygame.font.Font(None,36)
    text = font.render("SCORE:"+str(score) ,1,(244,243,123))
    try:
        screen.blit(text,(500,440))
    except:
        pass
def draw_end_game():
    global score
    font = pygame.font.Font(None,36)
    text = font.render("GAME OVER !!" ,1,(244,143,123))
    done = False
    while(not done):
        e = pygame.event.wait()
        try:
            screen.blit(text,(320,240))
            pygame.display.flip()
            pygame.display_update()
        except:
            pass
        if e.type == KEYDOWN:
            done = True
            break
        elif e.type == pygame.QUIT:
            done = True
            break
    
if __name__ == '__main__':
    full_screen = False
    draw_skeleton = True
    video_display = True

    screen_lock = thread.allocate()

    #screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)
    screen = pygame.display.set_mode(VIDEO_WINSIZE,0,32)    
    pygame.display.set_caption('Python Kinect Demo')
    skeletons = None
    screen.fill(THECOLORS["black"])

    kinect = nui.Runtime()
    kinect.skeleton_engine.enabled = True
    
    def post_frame(frame):
        try:
            pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
        except:
            # event queue full
            pass

    kinect.skeleton_frame_ready += post_frame
    
    kinect.depth_frame_ready += depth_frame_ready    
    kinect.video_frame_ready += video_frame_ready    
    
    kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
    kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)

    print('Controls: ')
    print('     d - Switch to depth view')
    print('     v - Switch to video view')
    print('     s - Toggle displaing of the skeleton')
    print('     u - Increase elevation angle')
    print('     j - Decrease elevation angle')

    # main game loop
    done = False

    x = random.randint(100,640)
    y = random.randint(50,480)

    #randomize the circle every 5 seconds
    pygame.time.set_timer(DRAWRANDOMCIRCLEEVENT,5000)
    #end game after 30 seconds
    pygame.time.set_timer(ENDGAMEEVENT,10000)
    #update score every 5 seconds
    #pygame.time.set_timer(DISPLAYSCOREEVENT,1)
    while not done:
        e = pygame.event.wait()
       
        dispInfo = pygame.display.Info()
        if e.type == pygame.QUIT:
            done = True
            break
        elif e.type == KINECTEVENT:
            skeletons = e.skeletons
            if draw_skeleton:
                rhx,rhy=draw_skeletons(skeletons)
                x,y=draw_random_circle(x,y,rhx,rhy)
                pygame.display.update()

        elif e.type == DRAWRANDOMCIRCLEEVENT:
            x = random.randint(100,600)
            y = random.randint(50,400)
            draw_random_circle(x,y,0,0)
        elif e.type == DISPLAYSCOREEVENT:
            update_score()
            pygame.display.update()
        elif e.type == ENDGAMEEVENT:
            draw_end_game()
            done = True
            break
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                done = True
                break
            elif e.key == K_d:
                with screen_lock:
                    screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)
                    video_display = False
            elif e.key == K_v:
                with screen_lock:
                    screen = pygame.display.set_mode(VIDEO_WINSIZE,0,32)    
                    video_display = True
            elif e.key == K_s:
                draw_skeleton = not draw_skeleton
            elif e.key == K_u:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
            elif e.key == K_j:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
            elif e.key == K_x:
                kinect.camera.elevation_angle = 2

    print "###################"
    print "FINAL SCORE:",score
    print "###################"
