import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
display = (WIDTH, HEIGHT)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glTranslatef(0.0, 0.0, -20)
glEnable(GL_DEPTH_TEST)

cube_vertices = [
    (5, -5, -5), (5, 5, -5), (-5, 5, -5), (-5, -5, -5),
    (5, -5, 5), (5, 5, 5), (-5, -5, 5), (-5, 5, 5)
]
cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 7), (7, 6), (6, 4),
    (0, 4), (1, 5), (2, 7), (3, 6)
]

class Particle:
    def __init__(self):
        self.x = random.uniform(-4, 4)
        self.y = random.uniform(-4, 4)
        self.z = random.uniform(-4, 4)
        self.radius = 0.2
        self.vx = random.uniform(-0.1, 0.1)
        self.vy = random.uniform(-0.1, 0.1)
        self.vz = random.uniform(-0.1, 0.1)
        self.mass = 1
        self.color = (random.random(), random.random(), random.random())

    def update(self):
        self.vy -= 0.005
        self.vx *= 0.99
        self.vy *= 0.99
        self.vz *= 0.99
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        if self.x - self.radius < -5:
            self.x = -5 + self.radius
            self.vx = -self.vx
        elif self.x + self.radius > 5:
            self.x = 5 - self.radius
            self.vx = -self.vx
        if self.y - self.radius < -5:
            self.y = -5 + self.radius
            self.vy = -self.vy
        elif self.y + self.radius > 5:
            self.y = 5 - self.radius
            self.vy = -self.vy
        if self.z - self.radius < -5:
            self.z = -5 + self.radius
            self.vz = -self.vz
        elif self.z + self.radius > 5:
            self.z = 5 - self.radius
            self.vz = -self.vz

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(*self.color)
        quad = gluNewQuadric()
        gluSphere(quad, self.radius, 16, 16)
        glPopMatrix()

def collide(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dz = p2.z - p1.z
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    if distance < p1.radius + p2.radius:
        nx = dx / distance if distance != 0 else 0
        ny = dy / distance if distance != 0 else 0
        nz = dz / distance if distance != 0 else 0
        relative_vx = p1.vx - p2.vx
        relative_vy = p1.vy - p2.vy
        relative_vz = p1.vz - p2.vz
        impulse = 2 * (relative_vx * nx + relative_vy * ny + relative_vz * nz) / (p1.mass + p2.mass)
        p1.vx -= impulse * p2.mass * nx
        p1.vy -= impulse * p2.mass * ny
        p1.vz -= impulse * p2.mass * nz
        p2.vx += impulse * p1.mass * nx
        p2.vy += impulse * p1.mass * ny
        p2.vz += impulse * p1.mass * nz
        overlap = (p1.radius + p2.radius - distance) / 2
        p1.x -= overlap * nx
        p1.y -= overlap * ny
        p1.z -= overlap * nz
        p2.x += overlap * nx
        p2.y += overlap * ny
        p2.z += overlap * nz

def draw_cube():
    glBegin(GL_LINES)
    glColor3f(1, 1, 1)
    for edge in cube_edges:
        for vertex in edge:
            glVertex3fv(cube_vertices[vertex])
    glEnd()

particles = [Particle() for _ in range(25)]
angle = 0

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)
    glRotatef(angle, 1, 1, 1)
    angle += 1
    draw_cube()
    for particle in particles:
        particle.update()
        particle.draw()
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            collide(particles[i], particles[j])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()