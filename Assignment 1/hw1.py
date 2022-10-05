'''
Myrzabekov Azamat
20192022

Implemented strictly by assignment instructions thus I did not include manual.
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

#########################################################################################

CENTER_X, CENTER_Y = 800 // 2, 800 // 2


# Create list of vertices for ellipse
ellipseVs = []
dtheta, a, b = 1, 0.1, 0.05
for i in range(45 // dtheta + 1):
    theta = i * dtheta
    r = (a * b) / np.sqrt((a * np.sin(theta)) ** 2 + (b * np.cos(theta)) ** 2)
    x, y = r * np.cos(theta), r * np.sin(theta)
    ellipseVs.append([x, y, 0])
    ellipseVs.append([-x, -y, 0])
    ellipseVs.append([-x, y, 0])
    ellipseVs.append([x, -y, 0])

#########################################################################################

class Polygon:
    def __init__(self):
        self.mat = np.eye(4)

    def draw(self):
        raise NotImplementedError

# TASK 1
# define your polygons here
class Triangle(Polygon):
    def __init__(self):
        super().__init__()
        self.vertices = np.array([[0, 0.1, 0], [-0.1, -0.1, 0], [0.1, -0.1, 0]], dtype = float)

    def draw(self):
        M = to_list(self.vertices)

        glBegin(GL_TRIANGLES)
        for i in range(3):
            glColor3f(0, 0, 1.0)
            glVertex3fv(M[i])
        glEnd()


class Rectangle(Polygon):
    def __init__(self):
        super().__init__()
        self.vertices = np.array([[-0.1, 0.1, 0], [0.1, 0.1, 0], [0.1, -0.1, 0], [-0.1, -0.1, 0]], dtype = float)

    def draw(self):
        M = to_list(self.vertices)

        glBegin(GL_QUADS)
        for i in range(4):
            glColor3f(0, 0, 1.0)
            glVertex3fv(M[i])
        glEnd()


class Ellipse(Polygon):
    def __init__(self):
        super().__init__()
        self.vertices = np.array(ellipseVs, dtype = float)

    def draw(self):
        M = to_list(self.vertices)

        glBegin(GL_TRIANGLE_FAN)
        for i in range(len(M)):
            glColor3f(0, 0, 1.0)
            glVertex3fv(M[i])
        glEnd()

# convert np.array to python list to handle "np.float128 not found" error on Windows
def to_list(M):
    R = []
    for i in range(M.shape[0]):
        T = []
        for j in range(M.shape[1]):
            T.append(M[i][j])
        R.append(T)
    return R

# TASK 2
# convert from left-top coordinate to [-1, 1] X [-1, 1] coordinate
def convertXY(x, y):
    nx = (x - CENTER_X) / CENTER_X
    ny = (CENTER_Y - y) / CENTER_Y

    return nx, ny

# TASK 3-1
def scale(sx, sy):
    S = np.eye(4)
    S[0][0], S[1][1] = sx, sy

    return S

# TASK 3-2
def rotation(degree):
    rad = degree * np.pi / 180

    R = np.eye(4)
    R[0][0], R[1][1] = np.cos(rad), np.cos(rad) 
    R[0][1], R[1][0] = -np.sin(rad), np.sin(rad)

    return R

# TASK 3-3
def translation(dx, dy):
    T = np.eye(4)
    T[0][3], T[1][3] = dx / (2 * CENTER_X), dy / (2 * CENTER_Y)

    return T


class Viewer:
    def __init__(self):
        self.polygons = [] # list of all accumulated polygons

        self.key = b''
        self.global_flag = True # flag for differentiating the global and local manipulations
        self.ctrl_flag = False # True while Ctrl key is pressed

        self.mouse_x = 0
        self.mouse_y = 0


    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        glMatrixMode(GL_MODELVIEW)

        # visualize your polygons here

        # TASK 5
        # draw all polygons 
        for polygon in self.polygons:
            M = to_list(polygon.mat.T)
            glMultMatrixf(M)
            polygon.draw()
            glLoadIdentity()

        glutSwapBuffers()


    def keyboard(self, key, x, y):
        print(f"keyboard event: key={key}, x={x}, y={y}")
        if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
            print("shift pressed")
        if glutGetModifiers() & GLUT_ACTIVE_ALT:
            print("alt pressed")
        if glutGetModifiers() & GLUT_ACTIVE_CTRL:
            print("ctrl pressed")
        #     self.ctrl_flag = True
        # else:
        #     self.ctrl_flag = False

        # TASK 2
        # store the last pressed key
        if key == b'\x1b': # ESC key
            self.key = b''
        elif key == b'1' or key == b'2' or key == b'3':
            self.key = key
        # TASK 4
        # toggle between the global and local
        elif key == b'g':
            self.global_flag = not self.global_flag
            print(f"global_flag is {self.global_flag}")
    
        glutPostRedisplay()


    def special(self, key, x, y):
        print(f"special key event: key={key}, x={x}, y={y}")

        # TASK 4
        # translation
        dx, dy = 10, 10
        T = np.eye(4)

        if key == 100:
            T = translation(-10, 0)
        elif key == 101:
            T = translation(0, 10)
        elif key == 102:
            T = translation(10, 0)
        elif key == 103:
            T = translation(0, -10)

        for polygon in self.polygons:
            polygon.mat = T @ polygon.mat

        glutPostRedisplay()


    def mouse(self, button, state, x, y):
        # button macros: GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON
        print(f"mouse press event: button={button}, state={state}, x={x}, y={y}")

        self.mouse_x, self.mouse_y = x, y

        # TASK 2
        # create and accumulate polygons with proper coordinates 
        if self.key == b'1':
            tr = Triangle()
            tr.mat[0][3], tr.mat[1][3] = convertXY(x, y)
            
            self.polygons.append(tr)
    
        elif self.key == b'2':
            rec = Rectangle()
            rec.mat[0][3], rec.mat[1][3] = convertXY(x, y)

            self.polygons.append(rec)

        elif self.key == b'3':
            ell = Ellipse()
            ell.mat[0][3], ell.mat[1][3] = convertXY(x, y)

            self.polygons.append(ell)

        glutPostRedisplay()


    def motion(self, x, y):
        print(f"mouse move event: x={x}, y={y}")

        # TASK 4
        # scaling
        if glutGetModifiers() & GLUT_ACTIVE_CTRL:
            print("ctrl pressed")
            self.ctrl_flag = True

        dx, dy = x - self.mouse_x, y - self.mouse_y

        TR = np.eye(4)
        if self.ctrl_flag: 
            if dy == 0 and dx > 0:
                TR = scale(1.1, 1)
            elif dy == 0 and dx < 0:
                TR = scale(0.9, 1)
            elif dx == 0 and dy > 0:
                TR = scale(1, 0.9)
            elif dx == 0 and dy < 0:
                TR = scale(1, 1.1) 

        else:
            # rotate
            if (dx > 0 and dy == 0) or (dx == 0 and dy < 0): # counterclockwise
                TR = rotation( -3 )
            elif (dx < 0 and dy == 0) or (dx == 0 and dy > 0): # clockwise
                TR = rotation( 3 )

        for polygon in self.polygons:
            if self.global_flag:
                # global transforamtion
                polygon.mat = TR @ polygon.mat
            else:
                # local transforamtion
                polygon.mat = polygon.mat @ TR

        # save mouse coordinate to detect the directin of scrolling
        self.mouse_x, self.mouse_y = x, y

        self.ctrl_flag = False

        glutPostRedisplay()


    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(2 * CENTER_X, 2 * CENTER_Y)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"CS471 Computer Graphics #1")

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)

        glutMainLoop()


if __name__ == "__main__":
    viewer = Viewer()
    viewer.run()
