from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import random
import time


def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def FindZone(dx, dy):
    zone = 0
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy > 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx > 0 and dy < 0:
            zone = 7
    elif abs(dx) <= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy > 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx > 0 and dy < 0:
            zone = 6
    return zone


def OriginalZone(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def ConvertToZone0(x1, y1, x2, y2, zone):
    if zone == 0:
        return x1, y1, x2, y2
    elif zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x1
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2
    return x1, y1, x2, y2


def MidPointLine(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = FindZone(dx, dy)
    x1, y1, x2, y2 = ConvertToZone0(x1, y1, x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d_init = 2 * dy - dx
    del_ne = 2 * dy - 2 * dx
    del_e = 2 * dy
    x = x1
    y = y1
    while x <= x2:
        new_x, new_y = OriginalZone(x, y, zone)
        draw_points(new_x, new_y)
        x += 1
        if d_init > 0:
            y += 1
            d_init = d_init + del_ne
        else:
            d_init = d_init + del_e


def circlepoints(center_x, center_y, x, y):
    draw_points(x + center_x, y + center_y)
    draw_points(x + center_x, -y + center_y)
    draw_points(-x + center_x, -y + center_y)
    draw_points(-x + center_x, y + center_y)
    draw_points(y + center_x, x + center_y)
    draw_points(-y + center_x, x + center_y)
    draw_points(-y + center_x, -x + center_y)
    draw_points(y + center_x, -x + center_y)


def MidPointcircle(center_x, center_y, radius):
    x = 0
    y = radius
    d = 1 - radius
    circlepoints(center_x, center_y, x, y)
    while x < y:
        if d >= 0:
            d += (2 * x) - (2 * y) + 5
            x += 1
            y -= 1
        else:
            d += (2 * x) + 3
            x += 1
        circlepoints(center_x, center_y, x, y)


#scalling function
def scaling(x1, y1, x2, y2, sc=0):
    v1 = np.array([[x1], [y1], [1]])
    v2 = np.array([[x2], [y2], [1]])

    s = np.array([[sc, 0, 0],
                  [0, sc, 0],  # scaling
                  [0, 0, 1]])

    t1 = np.array([[1, 0, -v1[0][0]],
                   [0, 1, -v1[1][0]],  # origin
                   [0, 0, 1]])

    v11 = np.matmul(s, np.matmul(t1, v1))
    v22 = np.matmul(s, np.matmul(t1, v2))


    return (v11[0][0], v11[1][0], v22[0][0], v22[1][0])



def drawCar(x, y):
    # Car body
    MidPointLine(x, y, x + 80, y)
    for i in range(35):
        glColor3f(1, 0, 0)
        MidPointLine(x, y+i, x + 80, y+i)

    # Wheels
    MidPointcircle(x + 20, y - 10, 10)
    MidPointcircle(x + 60, y - 10, 10)

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Set background color to black
    glEnable(GL_DEPTH_TEST)

def sprayWater(x, y, targetX, targetY):
    glColor3f(0, 1, 0.95)
    for i in range(5, 20):
        MidPointLine(x + 40, y + 30 + i, targetX+i, targetY)

def timer(value):
    global id
    if id in ['1', '2', '3']:
        driveToBuilding(id)
    glutPostRedisplay()  
    glutTimerFunc(1000//60, timer, 0)  # 60 FPS



def driveToBuilding(building_number):
    if building_number == '1':
        drawCar(100, 50)
        sprayWater(100, 50, 100, 300)
        flame(250)
    elif building_number == '2':
        drawCar(350, 50)
        sprayWater(350, 50, 350, 320)
        flame(500)
    elif building_number == '3':
        drawCar(600, 50)
        sprayWater(600, 50, 600, 380)
        flame(700)





def buildings():
    glColor3f(1.0, 1.0, 1.0)
    # road
    MidPointLine(0, 70, 250 + 520 , 337 + 85)

    # building -1
    MidPointLine(90, 115, 90, 360)
    MidPointLine(90, 360, 240, 400)
    MidPointLine(240, 185, 240, 400)


    #window1
    MidPointLine(120, 300, 120, 350)
    MidPointLine(120, 350, 160, 360)
    MidPointLine(160, 310, 160, 360)
    MidPointLine(120, 300, 160, 310)

    # Scaling kore choto window1 kora hoise
    s_x1,s_y1,s_x2,s_y2=scaling(120,300,120,350,.5)
    for i in range(30):
        MidPointLine(s_x1+120+i,s_y1+200+i*.3,s_x2+120+i,s_y2+200+i*.3)


    #window2
    MidPointLine(180, 320, 180, 368)
    MidPointLine(180, 368, 220, 380)
    MidPointLine(220, 332, 220, 380)
    MidPointLine(180, 320, 220, 332)

    #Scaling kore choto window2 kora hoise
    s_x1, s_y1, s_x2, s_y2 = scaling(180, 320, 180, 368, .5)
    for i in range(30):
        MidPointLine(s_x1+180+i, s_y1+220+i*.3, s_x2+180+i, s_y2+220+i*.3)


    #window color fillup
    for i in range(40):
        MidPointLine(120 + i, 300 + i * .3, 120 + i, 350 + i * .3)
    for i in range(40):
        MidPointLine(180 + i, 320 + i * .3, 180 + i, 368 + i * .3)





    # building -2
    MidPointLine(330, 220, 330, 380)
    MidPointLine(330, 380, 450, 410)
    MidPointLine(450, 280, 450, 410)
    #window fillup color
    for i in range(40):
        MidPointLine(350 + i, 310 + i * .3, 350 + i, 360 + i * .3)
    for i in range(40):
        MidPointLine(400 + i, 325 + i * .3, 400 + i, 375 + i * .3)


    # building -3
    MidPointLine(100 + 450, 320, 100 + 450, 430)
    MidPointLine(100 + 450, 430, 250 + 380, 450)
    MidPointLine(250 + 380, 360, 250 + 380, 450)
    #window color fillup
    for i in range(25):
        MidPointLine(565 + i, 370 + i * .3, 565 + i, 400 + i * .3)
    for i in range(25):
        MidPointLine(600 + i, 382 + i * .3, 600 + i, 410 + i * .3)




#agun dhorar funtion
def flame(pixel):
    glColor3f(1.0, 0, 0.0) #red color
    if pixel == 250:
        #from where to where line flame will fill up
        for i in range(90, 241, 1):
            MidPointLine(i, 330 + random.randint(-100, 100), i, 450 + random.randint(-100, 100))
    elif pixel == 500:
        for i in range(330, 451, 3):
            MidPointLine(i, 350 + random.randint(-30, 30), i, 450 + random.randint(-30, 30))
    elif pixel == 700:
        for i in range(550, 631, 3):
            MidPointLine(i, 380 + random.randint(-20, 20), i, 480 + random.randint(-20, 20))



def iterate():
    glViewport(0, 0, 1000, 1000)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 1000, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


global id
id = input('Enter Building Number: ')


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 0, 0)

    #function call hocche
    buildings()
    driveToBuilding(id)

    glutSwapBuffers()




glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Project Using Midpoint")
glutDisplayFunc(showScreen)
glutTimerFunc(0, timer, 0)  
init()
glutMainLoop()



