from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np


class Polygon:
    def __init__(self):
        self.mat = np.eye(4)
        self.x = 0
        self.y = 0

    def draw(self):
        raise NotImplementedError


# define your polygons here
class Triangle(Polygon):
    def __init__(self):
        super().__init__()

    def draw(self):
        glBegin(GL_TRIANGLES)
        glColor3f(0, 0, 1.0)
        glVertex3f(0, 0.1, 0)
        glColor3f(0, 0, 1.0)
        glVertex3f(-0.1, -0.1, 0)
        glColor3f(0, 0, 1.0)
        glVertex3f(0.1, -0.1, 0)
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


class Viewer:
    def __init__(self):
        self.polygons = []
        
        self.key = b''

        self.center_x= 800 / 2
        self.center_y = 600 / 2 

    def convertXY(self, x, y):
        nx = (x - self.center_x) / self.center_x
        ny = (self.center_y - y) / self.center_y

        return nx, ny


    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        glMatrixMode(GL_MODELVIEW)

        # visualize your polygons here

        for polygon in self.polygons:
            # glPushMatrix()
            # glTranslatef(dx, dy, 0)
            glMultMatrixf(polygon.mat.T)
            polygon.draw()
            glLoadIdentity()
            # glPopMatrix()

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

        if self.key == b'1':
            tr = Triangle()
            tr.mat[0][3], tr.mat[1][3] = self.convertXY(x, y)
            
            self.polygons.append(tr)
    
        elif self.key == b'2':
            rec = Rectangle()
            rec.mat[0][3], rec.mat[1][3] = self.convertXY(x, y)

            self.polygons.append(rec)

        elif self.key == b'3':
            ell = Ellipse()
            ell.mat[0][3], ell.mat[1][3] = self.convertXY(x, y)

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
