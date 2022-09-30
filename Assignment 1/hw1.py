from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np


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
        glColor3f(0, 0, 1.0)
        glVertex3fv(M[0])
        glColor3f(0, 0, 1.0)
        glVertex3fv(M[1])
        glColor3f(0, 0, 1.0)
        glVertex3fv(M[2])
        glEnd()


class Rectangle(Polygon):
    def __init__(self):
        super().__init__()

    def draw(self):
        glBegin(GL_QUADS)
        glColor3f(0, 0, 1.0)
        glVertex3f(-0.1, 0.1, 0)
        glColor3f(0, 0, 1.0)
        glVertex3f(0.1, 0.1, 0)
        glColor3f(0, 0, 1.0)
        glVertex3f(0.1, -0.1, 0)
        glColor3f(0, 0, 1.0)
        glVertex3f(-0.1, -0.1, 0)
        glEnd()


class Ellipse(Polygon):
    def __init__(self):
        super().__init__()

    def draw(self):
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 0, 1.0)
        glVertex3f(0.05, 0, 0)
        glColor3f(0, 0, 1.0)
        glVertex3f(0, 0.1, 0)
        glColor3f(0, 0, 1.0)
        glVertex3f(-0.05, 0, 0)
        glColor3f(0, 0, 1.0)
        glVertex3f(0, -0.1, 0)
        glEnd()

# convert np.array to python list to handle np.float128 error on Windows
def to_list(M):
    R = []
    for i in range(M.shape[0]):
        T = []
        for j in range(M.shape[1]):
            T.append(M[i][j])
        R.append(T)
    return R

# TASK 2
# convert from left-top coordinate to [-1,1] X [-1, 1] coordinate
def convertXY(x, y, center_x = 400, center_y = 300):
    nx = (x - center_x) / center_x
    ny = (center_y - y) / center_y

    return nx, ny

# TASK 3-1
def scale(sx, sy):
    S = np.eye(4)
    S[0][0], S[1][1] = sx, sy

    return S

# TASK 3-2
def rotation(degree):
    degree = degree * np.pi / 180

    R = np.eye(4)
    R[0][0], R[1][1] = np.cos(degree), np.cos(degree) 
    R[0][1], R[1][0] = -np.sin(degree), np.sin(degree)

    return R

# TASK 3-3
def translation(dx, dy):
    T = np.eye(4)
    T[1][3], T[2][3] = dx, dy

    return T


class Viewer:
    def __init__(self):
        self.polygons = []
        
        self.key = b''

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        glMatrixMode(GL_MODELVIEW)

        # visualize your polygons here

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

        if key == b'\x1b': # ESC key
            self.key = b''
        elif key == b'1' or key == b'2' or key == b'3':
            self.key = key
    
        glutPostRedisplay()


    def special(self, key, x, y):
        print(f"special key event: key={key}, x={x}, y={y}")

        glutPostRedisplay()


    def mouse(self, button, state, x, y):
        # button macros: GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON
        print(f"mouse press event: button={button}, state={state}, x={x}, y={y}")

        # TASK 2
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

        glutPostRedisplay()


    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 600)
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
