# bird evo sim

import pygame
import random

# --- CONSTANTS ---

# board init
BOARDX = 64 # -128 -> 128
BOARDY = 64

# audio params
AUDIO_CREATURE_RANGE = 15
AUDIO_PREDATOR_RANGE = 22

# temp/placeholder
squaresize = 40
gridlinewidth = 1

# --- CONSTANTS ---

# pygame init
scX, scY = 1280, 720
screen = pygame.display.set_mode((scX, scY))
pygame.display.set_caption("Bird Evo")
clock = pygame.time.Clock()

def htr(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rtx(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

class Creature:

    def __init__(self, board):

        self.pos = (random.randint(-10, 10), random.randint(-10, 10))
        self.color = [random.randint(0, 255)] * 3
        self.brain = []
        self.board = board

    def act(self):
        actions = []
        return actions

    def returnVision(self):
        return [random.randint(0, 1)] * 40

    def returnAudio(self):
        return ["#1eaf00", "#ffd900", "#ff0000", "#502eaf"]

    def returnTime(self):
        return self.board.time

    def returnPos(self):
        return self.pos

class Boardm:
    
    def __init__(self):
        self.creatures = [Creature(self)]

class Visualm:

    def __init__(self, screen, board):
        
        self.board = board
        
        self.screen = screen
        self.zoom = 1
        self.cpos = [0, 0]

    def tick(self):
        self.screen.fill("#000000")

        for c in self.board.creatures:
            self.colorSquare([c.pos[0], c.pos[1]], c.color, mode="circle")

        sounds = {}
        sounds = self.emitSound(sounds, (10, 15), "#1eaf50", AUDIO_CREATURE_RANGE)
        sounds = self.emitSound(sounds, (13, 13), "#f00ba6", AUDIO_CREATURE_RANGE)
        sounds = self.emitSound(sounds, (7, 9), "#ff0000", AUDIO_PREDATOR_RANGE)
        sounds = self.emitSound(sounds, (5, 18), "#ffd700", AUDIO_CREATURE_RANGE)
        sounds = self.emitSound(sounds, (22, 19), "#00d7ff", AUDIO_CREATURE_RANGE)

        for pos, colors in sounds.items():

            r = sum(color[0] for color in colors)
            g = sum(color[1] for color in colors)
            b = sum(color[2] for color in colors)

            color = (
                min(255, r),
                min(255, g),
                min(255, b)
            )

            self.colorSquare(pos, color)

        self.colorSquare([0, 0], "#0000ff")
        
        self.drawGrid()
        pygame.display.flip()

    def colorSquare(self, pos, color, mode=None):
        cellsize = squaresize * self.zoom

        wx = pos[0] * squaresize
        wy = pos[1] * squaresize

        cx = scX / 2 + (wx - self.cpos[0]) * self.zoom
        cy = scY / 2 + (wy - self.cpos[1]) * self.zoom

        if not mode:
            rect = (
                    cx + gridlinewidth,
                    cy + gridlinewidth,
                    cellsize - gridlinewidth * 0,
                    cellsize - gridlinewidth * 0
                )

            pygame.draw.rect(self.screen, color, rect)

        elif mode == "circle":
            centre = (
                cx, cy
            )

    def emitSound(self, totalsounds, pos, hex, volume):
        sounds = []
        r, g, b = htr(hex)

        sounds.append((pos, (r, g, b)))

        for i in range(1, volume + 1):

            strength = (volume - i) / volume
            color = (
                r * strength,
                g * strength,
                b * strength
            )

            # tr -> tl
            for j in range(i):
                x = i - j
                y = -j
                sounds.append(((pos[0] + x, pos[1] + y), color))

            # tl -> bl
            for j in range(i):
                x = -j
                y = -i + j
                sounds.append(((pos[0] + x, pos[1] + y), color))

            # bl -> br
            for j in range(i):
                x = -i + j
                y = j
                sounds.append(((pos[0] + x, pos[1] + y), color))

            # br -> tr
            for j in range(i):
                x = j
                y = i - j
                sounds.append(((pos[0] + x, pos[1] + y), color))

        for i in sounds:
            pos, color = i
            totalsounds.setdefault(pos, []).append(color)

        return totalsounds

    def drawGrid(self):
        for x in range(BOARDX * 2 + 1):
            wx = (x - BOARDX) * squaresize
            sx = (scX / 2 + (wx - self.cpos[0]) * self.zoom)
            pygame.draw.line(self.screen, "#99ffaa", (sx, 0), (sx, scY), 1)

        for y in range(BOARDY * 2 + 1):
            wy = (y - BOARDY) * squaresize
            sy = (scY / 2 + (wy - self.cpos[1]) * self.zoom)
            pygame.draw.line(self.screen, "#99ffaa", (0, sy), (scX, sy), 1)
    
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