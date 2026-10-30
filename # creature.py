# creature

import random
import numpy as np
import copy

EPISODES = 100
POPULATION = 1000

def htr(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rtx(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def sig(input): return 1 / (1 + np.exp(-input)) # sigmoid function

class Creature:

    def __init__(self, board, pos, brain=None):
        self.board = board

        self.pos = pos

        self.visionRadius = 5

        self.r = 30
        self.g = 80
        self.b = 175

        if brain is None:

            self.brainlayers = 1
            self.layersize = 16

            self.brain = [] # [(weights), (biases)]
            self.createBrain(4, 4)

        else:

            self.brainlayers = brain[0]
            self.layersize = brain[1]
            self.brain = brain[2]

    def returnRandomPos(self):
        #return [random.randint(28, 36), random.randint(28, 36)]
        return [random.randint(0, self.board.sx - 1), random.randint(0, self.board.sy - 1)]

    def scatter(self):
        self.pos = self.returnRandomPos()

    def clone(self, mutationRate=0.1, mutationStrength=0.1):
        brain = copy.deepcopy(self.brain)
        for weights, biases in brain:
            for neuron in range(len(weights)):
                for w in range(len(weights[neuron])):
                    if random.random() < mutationRate:
                        weights[neuron][w] += random.gauss(0, mutationStrength)

                if random.random() < mutationRate:
                    biases[neuron] += random.gauss(0, mutationStrength)
        
        c = Creature(
            self.board,
            self.returnRandomPos(),
            [self.brainlayers, self.layersize, brain]
        )
        return c

    def createBrain(self, inputSize, outputSize):
        self.brain = []

        sizes = ([inputSize] + [self.layersize] * self.brainlayers + [outputSize])

        for i in range(len(sizes) - 1):
            weights = []
            biases = []

            for neuron in range(sizes[i + 1]):
                neuronWeights = [
                    random.uniform(-0.5, 0.5)
                    for _ in range(sizes[i])
                ]

                weights.append(neuronWeights)
                biases.append(random.uniform(-0.5, 0.5))

            self.brain.append((weights, biases))

    def act(self):
        x, y = self.returnPos()

        inputs = [
            x / self.board.sx - 1,
            y / self.board.sy - 1,
            self.returnTime() / self.board.daylength,
            self.board.moon
        ]

        outputs = self.forward(inputs)

        u, d, l, r = outputs[0], outputs[1], outputs[2], outputs[3]
        if u > 0.5: self.move([0, 1])
        if d > 0.5: self.move([0, -1])
        if l > 0.5: self.move([-1, 0])
        if r > 0.5: self.move([1, 0])

    def forwardLayer(self, inputs, weights, biases):
        outputs = []

        for neuronWeights, bias in zip(weights, biases):
            total = bias

            for inp, weight in zip(inputs, neuronWeights):
                total += inp * weight

            output = sig(total)
            outputs.append(output)

        return outputs

    def forward(self, inputs):
        for weights, biases in self.brain:
            inputs = self.forwardLayer(inputs, weights, biases)

        return inputs

    def returnVision(self):
        vision = {}

        for dx in range(-self.visionRadius, self.visionRadius + 1):
            for dy in range(-self.visionRadius, self.visionRadius + 1):

                if abs(dx) + abs(dy) > self.visionRadius:
                    continue

                x = self.pos[0] + dx
                y = self.pos[1] + dy

                if 0 <= x < self.board.sx and 0 <= y < self.board.sy:
                    vision[(x, y)] = self.board.board[x][y]

        return vision

    def returnSound(self):
        sounds = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x = self.pos[0] + dx
            y = self.pos[1] + dy

            if 0 <= x < self.board.sx and 0 <= y < self.board.sy:
                sounds.append(self.board.sounds[x][y])
            else:
                sounds.append((0, 0, 0))

        return sounds

    def returnTime(self):
        return self.board.time

    def returnRandom(self):
        return random.random()

    def returnPos(self):
        return self.pos

    def move(self, dir): # dir = [0, 1]
        self.pos[0] += dir[0]
        self.pos[1] += dir[1]
        self.pos[0] = max(0, min(self.pos[0], self.board.sx - 1))
        self.pos[1] = max(0, min(self.pos[1], self.board.sy - 1))

    def setR(self, val): self.r = val
    def setG(self, val): self.g = val
    def setB(self, val): self.b = val
    def chirp(self): self.board.addSound(self.pos, (self.r, self.g, self.b))

class Board:

    def __init__(self):
        self.sx = 64
        self.sy = 64
        self.daylength = 100
        self.moonphase = False

        # self.reset()

    def reset(self):
        self.board = []
        for i in range(self.sx):
            row = []
            for j in range(self.sy):
                row.append(random.choice([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0.0, 0.5, 1.0]))
            self.board.append(row)
        self.sounds = []
        for i in range(self.sx):
            row = []
            for j in range(self.sy):
                r = int(min((i+1)/(j+1) * 255, 255))
                g = int(min((i+j)/2 * 4, 255))
                b = int(min((j+1)/(i+1) * 255, 255))
                row.append((r, g, b))
            self.sounds.append(row)
        self.time = 0
        self.moonphase = not self.moonphase
        self.moon = 1 if self.moonphase else 0

    def addSound(self, pos, rgb):
        pass

    def victoryCondition(self, creatures):
        survived = []
        for i in creatures:
            if self.moon == 0:
                if i.pos[0] < 8: survived.append(i)
            else:
                if i.pos[0] > 56: survived.append(i)
        return survived

def main():

    # create initial generation
    b = Board()
    creatures = []
    for _ in range(POPULATION): creatures.append(Creature(b, [random.randint(0, b.sx - 1), random.randint(0, b.sy - 1)]))

    # over number of episodes
    for e in range(EPISODES):

        # reset day
        b.reset()
        for c in creatures: c.scatter()

        # run day
        for t in range(b.daylength):

            # creatures act
            for c in creatures: c.act()
            b.time += 1

        # collect winning creatures
        survived = b.victoryCondition(creatures)
        print(len(survived), b.moon)

        # repopulate
        creatures = []
        for c in survived: creatures.append(c.clone())
        while len(creatures) < POPULATION:
            creatures.append(random.choice(survived).clone())

if __name__ == "__main__":
    main()