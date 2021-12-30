from posixpath import split
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os.path

from numpy.core.numeric import identity

azimuth = 1
elevation = 0.1
x_translate = 0
y_translate = 0
distance = 5
first_xpos = 0
first_ypos = 0
mode = 1

obj_input = False

file_name = ''
static_mode = True
animation_time = 0
max_offset = 1

channel_format = np.array([[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]], 'int32')

channel_list = np.array([0, 0, 0], 'int32')
root_channel_list = np.array([0, 0, 0], 'int32')


def create_vertex(splited):
    x = splited[1]
    y = splited[2]
    z = splited[3]
    vertex = np.array([x,y,z],'float64')
    return vertex
def create_column(splited):
    column = np.array([], 'float64')
    for value in splited:
        x = np.array([value], 'float64')
        column = np.append(column, x)
    return column
        

def create_channels(splited):
    rotation_channels = np.array([0, 0, 0], 'int32')
    index = 0
    for line in splited:
        if(line.upper() == 'XROTATION'):
            rotation_channels[index] = 0
            index += 1
        elif(line.upper() == 'YROTATION'):
            rotation_channels[index] = 1
            index += 1
        elif(line.upper() == 'ZROTATION'):
            rotation_channels[index] = 2
            index += 1
    return rotation_channels
def angle(t, angle):
    remainder = t
    scope = angle * 2
    while(remainder > scope):
        remainder =  t % scope 
        t /= scope
    t = remainder
    if(0 <= t and t <= angle):
        return t
    elif(angle < t and t <= scope):
        return scope - t 
def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def read(open_file):
    global frames, frame_time, channel_list, root_channel_list
    
    components_offset = np.array([0,0,0], 'float64')
    components_level = np.array([0], 'int64')
    components_rotation = np.array([],'float64')
    joint_list = np.array([], 'str')
    file = open(open_file, mode ='r')
    level = 1
    components_count = 0
    components_max_level = 0
    components_no_end = 0
    rotation_row = 0
    channel_check = False
    root_channel_check = False
    for line in file:
        splited = line.split()
        if(splited == []):
            continue
        first_letter = splited[0]
        # if(first_letter == "HIERARCHY"):
        if(first_letter == "ROOT"):
            root_name = splited[1]
            joint_list = np.append(joint_list, root_name)
            components_count += 1
            components_no_end +=1
            components_level = np.append(components_level, level)
        elif(first_letter == "JOINT"):
            joint_name = splited[1]
            joint_list = np.append(joint_list, joint_name)
            components_count += 1
            components_no_end +=1
            components_level = np.append(components_level, level)
        elif(first_letter == "End"):
            components_count += 1
            # End를 나타내는 -1을 넣어주어, 후에 for loop에서 탐지
            components_level = np.append(components_level, -1)
        elif(first_letter == "OFFSET"):
            vertex = create_vertex(splited)
            components_offset = np.append(components_offset, vertex)
        elif(first_letter == "CHANNELS"): 
            if(not root_channel_check):
                root_channel_list = create_channels(splited)
                root_channel_check = True
            elif(not channel_check):
                channel_list = create_channels(splited)
                channel_check = True
        elif(first_letter == "{"):
            level += 1
            if(components_max_level < level):
                components_max_level = level
        elif(first_letter == "}"):
            level -= 1
        elif(first_letter == "Frames:"):
            frames = int(splited[1])
        elif(first_letter == "Frame"):
            if(splited[1] == "Time:"):
                frame_time = float(splited[2])
        elif(is_float(first_letter)):
            rotation_row += 1
            column_value = create_column(splited)
            components_rotation = np.append(components_rotation, column_value)
    file.close()
    components_offset = components_offset.reshape(int(len(components_offset)/3) ,3)
    components_rotation = components_rotation.reshape(rotation_row, int(len(components_rotation)/(3*rotation_row)) ,3)
    components_offset[1] = [0,0,0]

    pre_level = 0
    # j array안에는 각 level에 해당하는 offsets들의 index를 넣는다.
    j = [0 for i in range(components_max_level)]
    index = 1
    vertex_list = [0]
    
    for level in components_level[1:]:
        if(pre_level == -1):
            # 0부터 시작
            for indexing in range(1, level):
                vertex_list.append(j[indexing])
            j[level] = index
            vertex_list.append(index)
        elif(level > pre_level):
            j[level] = index
            vertex_list.append(index)
        elif(level == -1):
            j[level] = index
            vertex_list.append(index)
        pre_level = level
        index += 1
    components_rotation_list = np.array([])
    count = 1
    for each_level in components_level:
        if each_level > 0:
            components_rotation_list = np.append(components_rotation_list, count)
            count += 1
        else:
            components_rotation_list = np.append(components_rotation_list, 0)
    return components_offset, components_rotation, components_level, components_max_level,vertex_list,components_rotation_list, rotation_row, joint_list

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
    global mode, static_mode, animation_time
    #change mode perspective or orthogonal
    if(key == glfw.KEY_V and action==glfw.PRESS):
        mode *= -1
    if(key == glfw.KEY_SPACE and action==glfw.PRESS):
        static_mode = not static_mode
        animation_time = glfw.get_time()
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
        distance -= 1
    #zoom out
    elif (yoffset < 0):
        distance += 1
def drop_callback(window, filenames):
    global filepaths, obj_input
    global offsets, rotations, levels, max_level, vertex_lists, rotation_lists, rotations_count, max_offset
    filepaths = filenames[0]
    
    obj_input = True
    offsets, rotations, levels, max_level, vertex_lists,rotation_lists, rotations_count, joint_list = read(filepaths)
    print("File name:", os.path.basename(filepaths))
    print("Number of frames:", frames)
    print("FPS:", 1/frame_time)
    print('Number of joints:', len(joint_list))
    print('List of all joints:', joint_list)

    if(abs(np.max(offsets)) > 1):
        max_offset = abs(np.max(offsets))
    else:
        max_offset = 1
    offsets = offsets / max_offset
def draw_lines(offset):
    glBegin(GL_LINES)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(offset)
    glEnd()

def draw_cubes(offset):
    y_axis = np.array((0,1,0))
    normal = np.cross(y_axis,offset)
    product = np.dot(offset,y_axis)
    nor_v1 = np.linalg.norm(offset)
    nor_v2 = np.linalg.norm(y_axis)
    
    angle = np.degrees(np.arccos(product / (nor_v1 *nor_v2)))
    glPushMatrix()
    glRotatef(angle, normal[0], normal[1], normal[2])
    glPushMatrix()
    glScalef(.02, 0.5 * nor_v1 ,.02)
    glPushMatrix()
    glTranslatef(0, 1, 0)
    drawCube_glVertex()
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

def drawCube_glVertex():
    glBegin(GL_TRIANGLES)
    glNormal3f(0,0,1) # v0, v2, v1, v0, v3, v2 normal
    glVertex3f( -1 ,  1 ,  1 ) # v0 position
    glVertex3f(  1 , -1 ,  1 ) # v2 position
    glVertex3f(  1 ,  1 ,  1 ) # v1 position

    glVertex3f( -1 ,  1 ,  1 ) # v0 position
    glVertex3f( -1 , -1 ,  1 ) # v3 position
    glVertex3f(  1 , -1 ,  1 ) # v2 position

    glNormal3f(0,0,-1)
    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f(  1 ,  1 , -1 ) # v5
    glVertex3f(  1 , -1 , -1 ) # v6

    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f(  1 , -1 , -1 ) # v6
    glVertex3f( -1 , -1 , -1 ) # v7

    glNormal3f(0,1,0)
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 ,  1 , -1 ) # v5

    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f(  1 ,  1 , -1 ) # v5
    glVertex3f( -1 ,  1 , -1 ) # v4

    glNormal3f(0,-1,0)
    glVertex3f( -1 , -1 ,  1 ) # v3
    glVertex3f(  1 , -1 , -1 ) # v6
    glVertex3f(  1 , -1 ,  1 ) # v2

    glVertex3f( -1 , -1 ,  1 ) # v3
    glVertex3f( -1 , -1 , -1 ) # v7
    glVertex3f(  1 , -1 , -1 ) # v6

    glNormal3f(1,0,0)
    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 , -1 ,  1 ) # v2
    glVertex3f(  1 , -1 , -1 ) # v6

    glVertex3f(  1 ,  1 ,  1 ) # v1
    glVertex3f(  1 , -1 , -1 ) # v6
    glVertex3f(  1 ,  1 , -1 ) # v5

    glNormal3f(-1,0,0)
    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f( -1 , -1 , -1 ) # v7
    glVertex3f( -1 , -1 ,  1 ) # v3

    glVertex3f( -1 ,  1 ,  1 ) # v0
    glVertex3f( -1 ,  1 , -1 ) # v4
    glVertex3f( -1 , -1 , -1 ) # v7
    glEnd()

def root_rotate_format(rx,ry,rz):

    glRotatef(rx,channel_format[root_channel_list[0]][0],channel_format[root_channel_list[0]][1],channel_format[root_channel_list[0]][2])
    glRotatef(ry,channel_format[root_channel_list[1]][0],channel_format[root_channel_list[1]][1],channel_format[root_channel_list[1]][2])
    glRotatef(rz,channel_format[root_channel_list[2]][0],channel_format[root_channel_list[2]][1],channel_format[root_channel_list[2]][2])

def rotate_format(rx,ry,rz):

    glRotatef(rx,channel_format[channel_list[0]][0],channel_format[channel_list[0]][1],channel_format[channel_list[0]][2])
    glRotatef(ry,channel_format[channel_list[1]][0],channel_format[channel_list[1]][1],channel_format[channel_list[1]][2])
    glRotatef(rz,channel_format[channel_list[2]][0],channel_format[channel_list[2]][1],channel_format[channel_list[2]][2])
    
def draw():
    t = glfw.get_time() - animation_time
    parameter = int((1 / frame_time) * t) % (rotations_count-1)
    if(static_mode):
        glBegin(GL_LINES)
        parents_offset = np.array([0,0,0])
        parents_offset = np.array([0,0,0])
        for index in range(1, len(vertex_lists) - 1):
            if(vertex_lists[index] == 1):
                parents_offset = np.array([0,0,0])
        
            if(vertex_lists[index] < vertex_lists[index+1]): 
                glVertex3fv(parents_offset+ offsets[vertex_lists[index]])
                parents_offset = parents_offset + offsets[vertex_lists[index]]
                glVertex3fv(parents_offset + offsets[vertex_lists[index+1]])
        glEnd()
    else:
        for rotation in rotations[parameter:parameter+1]:
            glPushMatrix()
            glTranslatef(rotation[0][0]/max_offset,rotation[0][1]/max_offset,rotation[0][2]/max_offset)
 
            push_lists = 0
            for index in range(1, len(levels) - 1):
                if(levels[index] == -1):
                    diff = levels[index - 1] - levels[index + 1] + 1
                    for i in  range(0,diff):
                        push_lists -= 1
                        glPopMatrix()
                else:   
                    r = rotation[int(rotation_lists[[index]])]
                    push_lists += 1
                    if(levels[index - 1] == -1):
                        draw_cubes(offsets[index])
                    glPushMatrix()
                    glTranslatef(offsets[index][0],offsets[index][1],offsets[index][2])
                    if(levels[index] == 1):
                        root_rotate_format(r[0],r[1], r[2])
                    else:
                        rotate_format(r[0],r[1],r[2])
                    draw_cubes(offsets[index+1])
            for i in range(0, push_lists):
                glPopMatrix()

            glPopMatrix()
def render():
    global gCamAng, gCamHeight, azimuth, t
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glLoadIdentity()

    ###lightning
    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    lightPos = ()

    glPushMatrix()
    
    lightPos = (0,5,0.,1.)    # try to change 4th element to 0. or 1.
    
    lightPos_1 = (-0.5,-0.5, -1)
    
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos_1)
    
    glPopMatrix()
    # light intensity for each color channel
    lightColor = np.array([1, 1, 0,1 ])
    lightColor_1 = np.array([116/255, 73/255, 108/255, 0])
    
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor_1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor_1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)



    material = np.array([0, 0, 1, 1])
    objectColor = (material[0], material[1], material[2],1.)
    specularObjectColor = (1.,1,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()

    ##lightning

    #perspective projection mode or orthogonal projection mode    
    if (mode == 1):
        gluPerspective(45, 1, 1, 100)
    elif (mode == -1):
        glOrtho(-1, 1, -1, 1, -8, 8)
    

    gluLookAt(distance * np.cos(azimuth) * np.cos(elevation) + x_translate , distance * np.sin(elevation) + y_translate , 
    distance * np.cos(elevation) * np.sin(azimuth), x_translate,y_translate,0, 0, 1, 0)

        
    drawFrame()
    glColor3ub(255, 255, 255)
    
    material = np.array([1,127/255,0])
    objectColor = (material[0], material[1], material[2],1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)


    glPushMatrix()
    
    
    if(obj_input):
        draw()
    glPopMatrix()

    glPopMatrix()
    ##lightning
    glDisable(GL_LIGHTING)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(1280,720,'ClassAssignment3', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)
    
    
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
