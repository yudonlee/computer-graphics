import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os.path

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
hierarchical = False
wireframe = True
smooth_shading = False

total_faces = 0
tri_faces = 0
quad_faces = 0
poly_faces = 0

def createVertex(splited, size):
    ##size is scaling rendering file
    global vertex_arr, normal_vertex_avg
    x = float(splited[1])
    y = float(splited[2])
    z = float(splited[3])
    vertex_list = np.array([x,y,z],'float32')/size
    vertex_arr = np.append(vertex_arr, vertex_list)
    normal_vertex_avg = np.append(normal_vertex_arr, normal_vertex_avg)

def createVertexNormal(splited,size):
    global normal_vertex_arr
    x = float(splited[1])
    y = float(splited[2])
    z = float(splited[3])
    normal_vertex_arr = np.append(normal_vertex_arr, np.array([x, y, z]))

def drawVertex(splited):
    global draw_vertex_list,total_faces, tri_faces, quad_faces, poly_faces, normal_vertex_avg, draw_normal_vertex_list
    line_list = np.empty(0)
    normal_line_list = np.empty(0)
    count = 0
    for face in splited[1:]:
        
        splitted_letter = '/'
        first_slash = face.find('/')
        if(face[first_slash + 1] == '/'):
            splitted_letter = '//'
        
        format_vertex = face.split(splitted_letter)

        vertex_num = int(format_vertex[0])
        line_list = np.append(line_list, np.array([vertex_num]))
        
        normal_vertex_num = int(format_vertex[-1])
        normal_line_list = np.append(normal_line_list, np.array([normal_vertex_num]))

        ## smooth shading for Extra credit in ClassAssignment 4-A
        if (smooth_shading):
            normal_vertex_avg[3 * vertex_num ] += normal_vertex_arr[ 3 *normal_vertex_num]
            normal_vertex_avg[3 * vertex_num + 1] += normal_vertex_arr[ 3 *normal_vertex_num + 1]
            normal_vertex_avg[3 * vertex_num + 2] += normal_vertex_arr[ 3 *normal_vertex_num + 2]
        ##############################################################
        count += 1
        
    
    ## Triangluation algorithm for Extra credit in ClassAssignment 4-B ##
    if count >= 4:
        new_line_list = np.empty(0)
        new_normal_line_list = np.empty(0)
        for i in range(1, count - 1):
            x = line_list[0]
            y = line_list[i]
            z = line_list[i+1]
            new_line_list = np.append(new_line_list, np.array([x,y,z])) 

            normal_x = normal_line_list[0]
            normal_y = normal_line_list[i]
            normal_z = normal_line_list[i+1]

            new_normal_line_list = np.append(new_normal_line_list, np.array([normal_x,normal_y,normal_z])) 
        
        line_list = new_line_list
        normal_line_list = new_normal_line_list
        if count == 4:
            quad_faces += 1
        else :
            poly_faces += 1
    else :
        tri_faces += 1
    #################################################################

    draw_vertex_list = np.append(draw_vertex_list, line_list)
    draw_normal_vertex_list = np.append(draw_normal_vertex_list, normal_line_list)

def drawHierarchical(filenames, size):
    global vertex_arr, normal_vertex_arr, draw_vertex_list, normal_vertex_avg, draw_normal_vertex_list
    
    vertex_arr = np.array([0, 0, 0],'float32')
    normal_vertex_arr = np.array([0, 0, 0],'float32')
    normal_vertex_avg = np.array([0, 0, 0],'float32')
    draw_normal_vertex_list = np.array([], 'float32')
    draw_vertex_list = np.array([], 'float32')
    file = open(str(filenames), 'r')
    for line in file:
        if(line[:2] == 'v '):
            createVertex(line.split(), size)
        elif(line[:2] == 'vn'):
            createVertexNormal(line.split(),size)
        elif(line[:2] == 'f '):
            drawVertex(line.split())

    for i in range (1, int(len(normal_vertex_avg)/3)):
        length = normal_vertex_avg[3 * i] * normal_vertex_avg[3 * i] + normal_vertex_avg[3 * i + 1] * normal_vertex_avg[3 * i + 1] 
        length += normal_vertex_avg[3 * i + 2] * normal_vertex_avg[3 * i + 2]
        if (length != 0):
            normal_vertex_avg[3 * i] /= length
            normal_vertex_avg[3 * i + 1] /= length 
            normal_vertex_avg[3 * i + 2] /= length

    file.close()

    draw()

def draw():
    global vertex_arr, normal_vertex_arr, draw_vertex_list,draw_normal_vertex_list
    glEnableClientState(GL_VERTEX_ARRAY)
    varr = vertex_arr
    narr = normal_vertex_arr
    
    iarr = draw_vertex_list
    inarr = draw_normal_vertex_list

    if(smooth_shading):
        normal = normal_vertex_avg
        glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointer(GL_FLOAT, 3 * normal.itemsize, normal)
        glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)
        glDisableClientState(GL_NORMAL_ARRAY)
    
    else:
        varr = np.array([],'float32')
        normal = np.array([], 'float32')

        for x in iarr:
            index = int(x)
            vertex = np.array([vertex_arr[3 * index], vertex_arr[3 * index + 1],vertex_arr[3 * index + 2]], 'float32' )
            varr = np.append(varr, vertex)
        
        for x in inarr:
            index = int(x)
            vertex = np.array([ narr[3 * index] , narr[3 * index + 1] , narr[3 * index + 2] ], 'float32' )
            normal = np.append(normal, vertex)

        glEnableClientState(GL_NORMAL_ARRAY)
        glNormalPointer(GL_FLOAT, 3 * normal.itemsize, normal)
        glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
        glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 3))
        glDisableClientState(GL_NORMAL_ARRAY)

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

def hieraMesh():
    global vertx_arr, normal_vertex_arr, draw_vertex_list
    t = glfw.get_time()
    glPushMatrix()
    # glRotatef((20/t), 0, -1, 0)   #배와 모든것들 돌면서 이동


    glTranslatef(np.cos(t/20), 0, np.sin(t/20))  #배 이동
    
    #brown material for motor_fan and boat#
    material = np.array([0.627, 0.321 , 0.176, 1])
    objectColor = (material[0], material[1], material[2],1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    glPushMatrix()
    #######################################
    
    glPushMatrix()
    # glRotatef((20/t), 0, -1, 0)   #배와 모든것들 돌면서 이동

    glPushMatrix()
    glRotatef(180 + t * 3, 0, -1, 0)  #boat.obj, motor fan 180도 돌리기 
    
    glPushMatrix()
    glRotatef(45, 0, -1, 0,)   #boat.obj 45도 돌리기 
    
    # glPushMatrix()
    drawHierarchical("boat.obj", 3)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(0, 0.05, 0.35)   # 모터 배뒤에 안착
    glPushMatrix() 
    glRotatef(t * 45, 0, 0, 1)   #모터 회전
    
    drawHierarchical("motor_fan.obj", 200)
    
    # glPushMatrix() # color pop


    glPopMatrix() 
    glPopMatrix()

    glPopMatrix()
    
    
    glPopMatrix() #brown material
    
    #blue mateiral for grid, rope , anchor
    material = np.array([0, 0, 1, 1])
    objectColor = (material[0], material[1], material[2],1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    #
    glPushMatrix()
    glRotatef(angle(t * 10, 45), 1, 0, 0) #rope anchor 물살에 의해 흔들림.
    glPushMatrix()  
    glTranslatef(0, -0.4, 0) #rope, anchor 원점으로 이동
    glPushMatrix()
    glScalef(1, 0.5,1) #밧줄 y축기준 축소
    drawHierarchical("rope.obj", 10)
    
    glPopMatrix()

    glPushMatrix()
    glRotatef(angle(t, 10), 1, 0, 0) #anchor 만 흔들림
    drawHierarchical("anchor.obj", 200)
    glPopMatrix()

    glPopMatrix()  
    glPopMatrix()
    
    glPopMatrix()
    
    glPopMatrix()
    
    #lighting
    glPopMatrix()
def singleMesh():
    global normal_vertex_arr, vertex_arr, draw_vertex_list, total_faces, normal_vertex_avg, draw_normal_vertex_list
    
    open_file = str(filepaths[0]) #convert list of filepaths to string of file paths
    
    file = open(open_file, mode ='r')

    vertex_arr = np.array([0, 0, 0],'float32')
    normal_vertex_arr = np.array([0, 0, 0],'float32')
    normal_vertex_avg = np.array([0, 0, 0],'float32')
    draw_normal_vertex_list = np.array([], 'float32')
    draw_vertex_list = np.array([], 'float32')

    for line in file:
        if(line[:2] == 'v '):
            createVertex(line.split(),3)
        elif(line[:2] == 'vn'):
            createVertexNormal(line.split(), 3)
        elif(line[:2] == 'f '):
            drawVertex(line.split())


    file.close()

    for i in range (1, int(len(normal_vertex_avg)/3)):
        length = normal_vertex_avg[3 * i] * normal_vertex_avg[3 * i] + normal_vertex_avg[3 * i + 1] * normal_vertex_avg[3 * i + 1] 
        length += normal_vertex_avg[3 * i + 2] * normal_vertex_avg[3 * i + 2]
        if (length != 0):
            normal_vertex_avg[3 * i] /= length
            normal_vertex_avg[3 * i + 1] /= length 
            normal_vertex_avg[3 * i + 2] /= length

    material = np.array([0.627, 0.321 , 0.176, 1])
    objectColor = (material[0], material[1], material[2],1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()
    
    draw()
    glPopMatrix()

    if(total_faces == 0):
        total_faces = tri_faces + quad_faces + poly_faces
        print("file name: ", os.path.basename(open_file))
        print("Total number of faces: ",total_faces)
        print("Number of faces with 3 vertices: ",tri_faces)
        print("Number of faces with 4 vertices: ",quad_faces)
        print("Number of faces with more than 4 faces:",poly_faces)


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
    global mode, hierarchical, wireframe, smooth_shading
    #change mode perspective or orthogonal
    if(key == glfw.KEY_V and action==glfw.PRESS):
        mode *= -1
    if(key == glfw.KEY_H and action==glfw.PRESS):
        hierarchical = not hierarchical
    if(key == glfw.KEY_Z and action==glfw.PRESS):
        wireframe = not wireframe
    if(key == glfw.KEY_S and action==glfw.PRESS):
        smooth_shading = not smooth_shading
    
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
def drop_callback(window, filenames):
    global filepaths, obj_input, total_faces, tri_faces, quad_faces, poly_faces
    filepaths = filenames
    
    obj_input = True
    total_faces = 0
    tri_faces = 0
    quad_faces = 0
    poly_faces = 0

def render():
    global gCamAng, gCamHeight, azimuth, t
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    if (wireframe):
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    else :
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
    

    gluLookAt(distance * np.cos(azimuth) * np.cos(elevation) + x_translate, distance * np.sin(elevation)  + y_translate , 
    distance * np.cos(elevation) * np.sin(azimuth), x_translate, y_translate, 0, 0, 1, 0)
   
        
    drawFrame()
    glColor3ub(255, 255, 255)
    
    
    if obj_input and (not hierarchical):
        singleMesh()
    elif hierarchical:
        hieraMesh()
    
    glPopMatrix()
    ##lightning
    glDisable(GL_LIGHTING)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(1280,720,'ClassAssignment2', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
