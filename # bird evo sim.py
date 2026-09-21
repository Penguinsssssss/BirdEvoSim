# bird evo sim

import pygame
import random

# --- CONSTANTS ---

# board init
BOARDX = 32 # -128 -> 128
BOARDY = 32

# audio params
AUDIO_CREATURE_RANGE = 8
AUDIO_PREDATOR_RANGE = 15

# temp/placeholder
squaresize = 40
gridlinewidth = 1

# --- CONSTANTS ---

# pygame init
scX, scY = 1280, 720
screen = pygame.display.set_mode((scX, scY))
pygame.display.set_caption("Bird Evo")
clock = pygame.time.Clock()

class Creature:

    def __init__(self):

        self.pos = (random.randint(-10, 10), random.randint(-10, 10))
        self.color = [random.randint(0, 255)] * 3
        self.brain = []

class Boardm:
    
    def __init__(self):
        self.creatures = [Creature()]

class Visualm:

    def __init__(self, screen, board):
        
        self.board = board
        
        self.screen = screen
        self.zoom = 1
        self.cpos = [0, 0]

    def tick(self):
        self.screen.fill("#332244")
        self.drawGrid()
        for c in self.board.creatures:
            self.colorSquare([c.pos[0], c.pos[1]], c.color)
        self.colorSquare([0, 0], "#0000ff")
        pygame.display.flip()

    def drawGrid(self):
        for x in range(BOARDX * 2 + 1):
            wx = (x - BOARDX) * squaresize
            sx = (scX / 2 + (wx - self.cpos[0]) * self.zoom)
            pygame.draw.line(self.screen, "#99ffaa", (sx, 0), (sx, scY), 1)

        for y in range(BOARDY * 2 + 1):
            wy = (y - BOARDY) * squaresize
            sy = (scY / 2 + (wy - self.cpos[1]) * self.zoom)

            pygame.draw.line(self.screen, "#99ffaa", (0, sy), (scX, sy), 1)

    def colorSquare(self, pos, color):
        cellsize = squaresize * self.zoom

        wx = pos[0] * squaresize
        wy = pos[1] * squaresize

        cx = scX / 2 + (wx - self.cpos[0]) * self.zoom
        cy = scY / 2 + (wy - self.cpos[1]) * self.zoom
        
        rect = (
                cx + gridlinewidth,
                cy + gridlinewidth,
                cellsize - gridlinewidth,
                cellsize - gridlinewidth
            )

        pygame.draw.rect(self.screen, color, rect)
    
    def deltazoom(self, zm):
        mx, my = pygame.mouse.get_pos()

        oz = self.zoom
        cx, cy = self.cpos

        wx = cx + (mx - scX / 2) / oz
        wy = cy + (my - scY / 2) / oz

        nz = oz * zm
        nz = max(0.1, min(nz, 10))

        cx = wx - (mx - scX / 2) / nz
        cy = wy - (my - scY / 2) / nz

        self.zoom = nz
        self.cpos = [cx, cy]

def main():

    boardm = Boardm()
    visualm = Visualm(screen, boardm)

    running = True
    mx, my, pmx, pmy = 0, 0, 0, 0

    while running:

        clock.tick(60)

        visualm.tick()

        mx, my = pygame.mouse.get_pos()
        lc, mc, rc = pygame.mouse.get_pressed()
        if lc:
            visualm.cpos[0] += (pmx - mx) / visualm.zoom
            visualm.cpos[1] += (pmy - my) / visualm.zoom
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    visualm.deltazoom(1.05)
                elif event.y < 0:
                    visualm.deltazoom(1 / 1.05)

        pmx, pmy = mx, my

if __name__ == "__main__":
    main()