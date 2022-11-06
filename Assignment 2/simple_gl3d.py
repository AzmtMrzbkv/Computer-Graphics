from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


# Task 1
def get_Tscene(p, at, up):
    z = p - at
    z /= np.linalg.norm(z)

    x = np.cross(up, z)
    x /= np.linalg.norm(x)

    y = np.cross(z, x)

    R = np.array([x,y,z]).T
    Tcam = np.zeros((4,4))
    Tcam[:3,:3] = R
    Tcam[:3,3] = p
    Tcam[3, 3] = 1

    # MR = np.eye(4)
    # MR[:3,:3] = R.T

    # MT = np.eye(4)
    # MT[:3,3] = -p
    # print(MR @ MT)

    # return MR @ MT
    return np.linalg.inv(Tcam)   
    


# Task 2
def get_Track_R(p1, p2):
    n = np.cross(p1, p2)
    theta = np.linalg.norm(n) / (np.linalg.norm(p1) * np.linalg.norm(p2))

    # https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula
    K = np.zeros((4,4))
    K[2,1], K[1,2] = n[0], -n[0]
    K[0,2], K[2,0] = n[1], -n[1]
    K[1,0], K[0,1] = n[2], -n[2]

    if np.linalg.norm(n) > 0:
        K /= np.linalg.norm(n)

    R = np.eye(4) + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
    return R

# Task 2 : scale down x and y, if x^2 + y^2 > r^2 and find z
def get_pos(x, y, r):
    if x ** 2 + y ** 2 > r ** 2:
        z = 0
        k = np.sqrt((x ** 2 + y ** 2) / r ** 2)
        x, y = x / k, y / k
    else:
        z = np.sqrt(r ** 2 - x ** 2 - y ** 2)

    return np.array([x, y, z])


###################################################################################
################################### From HW2 ######################################
###################################################################################

# convert np.array to python list to handle "np.float128 not found" error on Windows
def to_list(M):
    R = []
    for i in range(M.shape[0]):
        T = []
        for j in range(M.shape[1]):
            T.append(M[i][j])
        R.append(T)
    return R

# convert from left-top coordinate to [-1, 1] X [-1, 1] coordinate scaled to [w, h]
def convertXY(x, y, cx, cy):
    nx = (x - cx)
    ny = (cy - y)

    return nx, ny

def scale(sx, sy, sz):
    S = np.eye(4)
    S[0][0], S[1][1], S[2][2] = sx, sy, sz

    return S

def rotation(degree):
    rad = degree * np.pi / 180

    R = np.eye(4)
    R[0][0], R[1][1] = np.cos(rad), np.cos(rad) 
    R[0][1], R[1][0] = -np.sin(rad), np.sin(rad)

    return R

def translation(dx, dy, w, h):
    T = np.eye(4)
    T[0][3], T[1][3] = dx / w, dy / h

    return T

###################################################################################
###################################################################################


class Viewer:
    def __init__(self):
        self.screen_width = 800;
        self.screen_height = 800;
        self.radius = min(self.screen_width, self.screen_height)
        self.scale = 1
        self.R = np.eye(4)
        self.T = np.eye(4)
        self.S = np.eye(4)
        self.Trans = np.eye(4)

        # Task 5
        self.FoV = 0
        self.Tscene = get_Tscene(np.array([0.,0.,1.]), np.array([0.,0.,0.]), np.array([0.,1.,0.]))

    def light(self):
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

        # feel free to adjust light colors
        lightAmbient = [0.5, 0.5, 0.5, 1.0]
        lightDiffuse = [0.5, 0.5, 0.5, 1.0]
        lightSpecular = [0.5, 0.5, 0.5, 1.0]
        lightPosition = [1, 1, -1, 0]    # vector: point at infinity
        glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
        glEnable(GL_LIGHT0)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        # projection matrix
        # use glOrtho and glFrustum (or gluPerspective) here
        
        # Task 3
        if self.FoV == 0:
            glOrtho(-1, 1, -1, 1, -100, 100)
        else:
            # zNear = 1 / (2 * np.tan((self.FoV / 2) * (np.pi / 180)))
            gluPerspective(self.FoV, self.screen_width / self.screen_height, 1.0, 10000.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # do some transformations using camera view
        # glMultMatrixf(to_list(self.Trans.T))
        glMultMatrixf(to_list(self.Trans.T))
        glutSolidTeapot(0.5)
        
        glLoadIdentity()
        glMultMatrixf(to_list(self.Tscene.T))

        glutSwapBuffers()

    def keyboard(self, key, x, y):
        print(f"keyboard event: key={key}, x={x}, y={y}")
        if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
            print("shift pressed")
        if glutGetModifiers() & GLUT_ACTIVE_ALT:
            print("alt pressed")
        if glutGetModifiers() & GLUT_ACTIVE_CTRL:
            print("ctrl pressed")

        # Task 4 : reset to default
        if key == b'd':
            self.Tscene = np.eye(4)

        if key == b'0':
            self.FoV = 0

        glutPostRedisplay()

        # Task 4 : close window
        if key == b'\x1b':
            glutDestroyWindow(glutGetWindow())

    def special(self, key, x, y):
        print(f"special key event: key={key}, x={x}, y={y}")

        # Task 4 : FoV change
        if key == 101:
            self.FoV += 5
            if self.FoV > 90:
                self.FoV = 90

        if key == 103:
            self.FoV -= 5
            if self.FoV < 0:
                self.FoV = 0

        glutPostRedisplay()

    def mouse(self, button, state, x, y):
        # button macros: GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON
        print(f"mouse press event: button={button}, state={state}, x={x}, y={y}")

        self.mouse_x, self.mouse_y = convertXY(x, y, self.screen_width, self.screen_height)
        self.mouse_button = button

        # Task 4 : zoom in/out
        if self.mouse_button == 3:
            # zoom in
            if self.scale < 1:
                self.scale += 0.1
                tscale = scale(1.1, 1.1, 1.1)
            else:
                self.scale += 1
                if self.scale > 5:
                    self.scale = 5
                
                sc = self.scale / (self.scale - 1)
                tscale = scale(sc, sc, sc)
            print(self.scale)
            self.Trans = self.Trans @ tscale

        elif self.mouse_button == 4:
            # zoom out
            if self.scale > 1:
                self.scale -= 1
                sc = self.scale / (self.scale + 1)
                tscale = scale(sc, sc, sc)
            else:
                self.scale -= 0.1
                if self.scale < 0.1:
                    self.scale = 0.1
                    tscale = np.eye(4)
                else:
                    tscale = scale(0.1, 0.1, 0.1)
            print(self.scale)    
            self.Trans = self.Trans @ tscale

        glutPostRedisplay()

    def motion(self, x, y):
        print(f"mouse move event: x={x}, y={y}")

        # Task 4 rotation/translation of the scene
        x, y = convertXY(x, y, self.screen_width, self.screen_height)
        if self.mouse_button == 0:
            p1, p2 = get_pos(self.mouse_x, self.mouse_y, self.radius), get_pos(x, y, self.radius)
            self.R = self.R @ get_Track_R(p1, p2)
            self.Trans =  self.Trans @ get_Track_R(p1, p2)

        elif self.mouse_button == 2:
            # self.T = translation(x - self.mouse_x, y - self.mouse_y, self.screen_width, self.screen_height) @ self.T
            self.Trans = translation(x - self.mouse_x, y - self.mouse_y, self.screen_width, self.screen_height) @ self.Trans

        self.mouse_x, self.mouse_y = x, y
        glutPostRedisplay()

    # Task 4 : resize window
    def reshape(self, w, h):
        # implement here
        print(f"window size: {w} x {h}")

        # TODO adjust necessary changes to projection and ratio
        self.Trans = self.Trans @ scale(1, -1, 1)

        self.screen_width, self.screen_height = w, h
        self.radius = min(self.screen_width, self.screen_height)

        glViewport(0, 0, w, h)
        glutPostRedisplay()

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"CS471 Computer Graphics #2")

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutReshapeFunc(self.reshape)

        self.light()

        glutMainLoop()


if __name__ == "__main__":
    viewer = Viewer()
    viewer.run()
