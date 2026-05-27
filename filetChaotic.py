import pygame as pg
import math
import random

pg.init()
info = pg.display.Info()
W, H = info.current_w, info.current_h
screen = pg.display.set_mode((W, H), pg.FULLSCREEN | pg.DOUBLEBUF)
clock = pg.time.Clock()

RES_X, RES_Y = 40, 30
GAP = 22
ITERATIONS = 4  
sticks = []

class Node:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.px, self.py = x, y
        self.base_x, self.base_y = x, y 

start_x = W // 2 - (RES_X * GAP) // 2
start_y = H // 2 - (RES_Y * GAP) // 2

nodes = []
for y in range(RES_Y):
    row = []
    for x in range(RES_X):
        row.append(Node(x * GAP + start_x, y * GAP + start_y))
    nodes.append(row)

for y in range(RES_Y):
    for x in range(RES_X):
        if x < RES_X - 1:
            sticks.append([nodes[y][x], nodes[y][x+1], GAP, True])
        if y < RES_Y - 1:
            sticks.append([nodes[y][x], nodes[y+1][x], GAP, True])

running = True
t = 0  
while running:
    overlay = pg.Surface((W, H))
    overlay.set_alpha(60) 
    overlay.fill((5, 5, 15))
    screen.blit(overlay, (0, 0))

    t += 0.05
    m_pos = pg.mouse.get_pos()
    m_down = pg.mouse.get_pressed()

    for e in pg.event.get():
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_ESCAPE:
                running = False
            
            if e.key == pg.K_SPACE:
                for row in nodes:
                    for n in row:
                        d = math.hypot(n.x - W//2, n.y - H//2)
                        n.x += (n.x - W//2) / (d + 1) * 50
                        n.y += (n.y - H//2) / (d + 1) * 50

    for row in nodes:
        for n in row:
            vx, vy = (n.x - n.px) * 0.98, (n.y - n.py) * 0.98
            n.px, n.py = n.x, n.y

            drift = math.sin(t + n.base_x * 0.01) * 0.2
            n.x += vx + drift
            n.y += vy + math.cos(t + n.base_y * 0.01) * 0.2

            if m_down[0]:
                dx, dy = n.x - m_pos[0], n.y - m_pos[1]
                dist = math.hypot(dx, dy)
                if dist < 150:
                    force = (150 - dist) * 0.02
                    n.x -= (dx / (dist + 1)) * force
                    n.y -= (dy / (dist + 1)) * force

    for _ in range(ITERATIONS):
        for s in sticks:
            if not s[3]: continue 
            p1, p2, length, _ = s
            dx, dy = p2.x - p1.x, p2.y - p1.y
            dist = math.hypot(dx, dy)
            if dist == 0: dist = 0.1

            if m_down[2] and dist < 30 and math.hypot(p1.x - m_pos[0], p1.y - m_pos[1]) < 30:
                s[3] = False
                continue
            
            if dist > length * 4:
                s[3] = False
                continue

            diff = (length - dist) / dist * 0.5
            p1.x -= dx * diff
            p1.y -= dy * diff
            p2.x += dx * diff
            p2.y += dy * diff

    
    for s in sticks:
        if s[3]: 
            dist = math.hypot(s[0].x - s[1].x, s[0].y - s[1].y)
            pulse = (math.sin(t * 2) + 1) * 50
            


            
            r = min(255, int(dist * 5))
            g = min(255, int(100 + pulse + dist * 2))
            b = 255
            
            pg.draw.aaline(screen, (r, g, b), (s[0].x, s[0].y), (s[1].x, s[1].y))

    pg.display.flip()
    clock.tick(60)

pg.quit()