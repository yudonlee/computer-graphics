import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

azimuth = 1
elevation = 0.1
x_translate = 0
y_translate = 0
distance = 3
first_xpos = 0
first_ypos = 0
mode = 1
# draw a cube of side 1, centered at the origin.
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glColor3ub(255, 255, 255)

    #draw grid on xz plane
    for i in range(-100, 100):
        glVertex3fv(np.array([i, 0.,-1000]))
        glVertex3fv(np.array([i,0.,1000]))
    for i in range(-100, 100):
        glVertex3fv(np.array([-1000,0,i]))
        glVertex3fv(np.array([1000,0,i]))
        
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global mode
    #change mode perspective or orthogonal
    if(key == glfw.KEY_V and action==glfw.PRESS):
        mode *= -1

def cursor_callback(window, xpos, ypos):
    global first_ypos, first_xpos, y_translate, x_translate, azimuth, elevation
    #orbit
    if (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS):
        elevation += np.radians(((ypos - first_ypos) / (30)))
        azimuth += np.radians((xpos - first_xpos) / (30))
        first_ypos = ypos
        first_xpos = xpos
    #panning
    elif (glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS):
        y_translate += (ypos- first_ypos) / 480 
        x_translate += (xpos- first_xpos) / 480 
        first_ypos = ypos
        first_xpos = xpos    

def button_callback(window, button, action, mod):
    global y_translate, first_xpos, first_ypos
    #when mouse button is clicked, calculate diffrence from lotation of first cursor to lotation of last cursor released in button
    #orbit 
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            first_xpos, first_ypos = glfw.get_cursor_pos(window)
        elif action==glfw.RELEASE:
            first_xpos = 0
            first_ypos = 0 
    #panning
    elif button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            first_xpos, first_ypos = glfw.get_cursor_pos(window)
        elif action==glfw.RELEASE:
            first_xpos = 0
            first_ypos = 0

def scroll_callback(window, xoffset, yoffset):
    #zoom in 
    # limit the distance from target bigger than 0.1.
    global distance
    if (yoffset > 0):
        if(distance > 0.2):
            distance -= 0.1
    #zoom out
    elif (yoffset < 0):
        distance += 0.1

def render():
    global gCamAng, gCamHeight, azimuth, t
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()

    #perspective projection mode or orthogonal projection mode    
    if (mode == 1):
        gluPerspective(45, 1, 1, 100)
    elif (mode == -1):
        glOrtho(-1, 1, -1, 1, -8, 8)
    

    gluLookAt(distance * np.cos(azimuth) * np.cos(elevation) + x_translate, distance * np.sin(elevation)  + y_translate , 
    distance * np.cos(elevation) * np.sin(azimuth), x_translate, y_translate, 0, 0, 1, 0)
   
        
    drawFrame()
    glColor3ub(255, 255, 255)
    drawUnitCube()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(720,720,'ClassAssignment1', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
