import pygame
import sys
from pygame.locals import *
from math import sin, cos, tan, pi
import numpy as np
from numpy.linalg import inv
from spring import spring


class Spring():
    def __init__(self, color, start, end, nodes, width, lead1, lead2):
        self.start = start
        self.end = end
        self.nodes = nodes
        self.width = width
        self.lead1 = lead1
        self.lead2 = lead2
        self.weight = 3
        self.color = color

    def update(self, start, end):
        self.start = start
        self.end = end

        self.x, self.y  = spring(self.start, self.end, self.nodes, self.width)

    def render(self):
        pygame.draw.lines(screen, self.color, False, list(zip(self.x, self.y)), self.weight)


def G(y, t):
    x_d, θ_d, x, θ = y[0], y[1], y[2], y[3]

    x_dd = (l0 + x) * θ_d ** 2 - k / m * x + g * cos(θ)
    θ_dd = -2.0 / (l0 + x) * x_d * θ_d - g / (l0 + x) * sin(θ)

    return np.array([x_dd, θ_dd, x_d, θ_d])


def update(x, θ):
    x_coord = (l0 + x) * sin(θ) + offset[0]
    y_coord = (l0 + x) * cos(θ) + offset[1]

    return (int(x_coord), int(y_coord))


def render(point):
    x, y = point[0], point[1]

    if prev_point:
        pygame.draw.line(trace, LT_BLUE, prev_point, (x, y), 5)

    screen.fill(WHITE)
    if is_tracing:
        screen.blit(trace, (0, 0))

    # pygame.draw.line(screen, BLACK, offset, (x,y), 5)
    s.update(offset, point)
    s.render()
    pygame.draw.circle(screen, BLACK, offset, 8)
    pygame.draw.circle(screen, BLUE, (x, y), int(m * 10))

    return (x, y)


w, h = 1024, 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LT_BLUE = (230, 230, 255)
offset = (w // 2, h // 4)
is_tracing = True

screen = pygame.display.set_mode((w, h))
screen.fill(WHITE)
trace = screen.copy()
pygame.display.update()
clock = pygame.time.Clock()

# parameters
m = 1.0
l0 = 400
g = 0.25
k = 0.0005

prev_point = None
t = 0.0
delta_t = 1
y = np.array([0.0, 0.0, 0.0, 2.0])

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 38)

s = Spring(BLACK, (0, 0), (0, 0), 25, 30, 90, 90)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_t:
                is_tracing = not (is_tracing)
            if event.key == K_c:
                trace.fill(WHITE)

    point = update(y[2], y[3])
    prev_point = render(point)

    t += 1

    clock.tick(60)
    pygame.display.update()
