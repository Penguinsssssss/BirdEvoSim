# bird evo sim

import pygame

# --- CONSTANTS ---

# board init
BOARDX = 128 # -128 -> 128
BOARDY = 128

# audio params
AUDIO_CREATURE_RANGE = 8
AUDIO_PREDATOR_RANGE = 15

# temp/placeholder
squaresize = 40

# --- CONSTANTS ---

# pygame init
scX, scY = 1280 * 0.75, 720 * 0.75
screen = pygame.display.set_mode((scX, scY))
pygame.display.set_caption("Bird Evo")
clock = pygame.time.Clock()

class Creature:

    def __init__(self):

        self.pos = (0, 0)
        self.brain = []

class Visualm:

    def __init__(self, screen, globals):
        self.screen = screen
        self.globals = globals

    def tick(self):
        self.screen.fill("#332244")
        self.drawGrid()
        self.drawCreatures()
        pygame.display.flip()

    def drawGrid(self):
        cellsize = squaresize * self.globals.zoom

        for x in range(BOARDX * 2 + 1):
            lx = scX / 2 + (x - BOARDX) * cellsize - self.globals.cpos[0]
            pygame.draw.line(self.screen, "#9988aa", (lx, 0), (lx, scY), 1)

        for y in range(BOARDY * 2 + 1):
            ly = scY / 2 + (y - BOARDY) * cellsize - self.globals.cpos[1]
            pygame.draw.line(self.screen, "#9988aa", (0, ly), (scX, ly), 1)

    def drawCreatures(self):
        cellsize = squaresize * self.globals.zoom

        for creature in self.globals.creatures:
            cx = scX / 2 + (creature.pos[0] - BOARDX) * cellsize - self.globals.cpos[0]
            cy = scY / 2 + (creature.pos[1] - BOARDY) * cellsize - self.globals.cpos[1]
            pygame.draw.circle(self.screen, "#663333", (cx, cy), 10)

class Globals: pass

def main():

    globals = Globals()
    globals.zoom = 1
    globals.cpos = [0, 0]
    globals.creatures = [Creature()]
    visualm = Visualm(screen, globals)

    running = True
    mx, my, pmx, pmy = 0, 0, 0, 0

    while running:

        clock.tick(60)

        visualm.tick()

        mx, my = pygame.mouse.get_pos()
        lc, mc, rc = pygame.mouse.get_pressed()
        if lc:
            globals.cpos[0] += pmx - mx
            globals.cpos[1] += pmy - my
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEWHEEL:
                globals.zoom += event.y * 0.01

        pmx, pmy = mx, my
    

if __name__ == "__main__":
    main()