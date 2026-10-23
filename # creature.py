# creature

import random
import numpy as np

def htr(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rtx(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def sig(input): return 1 / (1 + np.exp(-input)) # sigmoid function

class Creature:

    def __init__(self, board, pos):
        self.board = board

        self.pos = pos.copy()
        self.startingpos = pos.copy()

        self.visionRadius = 5

        self.r = 30
        self.g = 80
        self.b = 175

        self.brainlayers = 1
        self.layersize = 16

        self.brain = [] # [(weights), (biases)]
        self.createBrain(3, 2)

    def end(self):
        if 0 not in self.pos and 65 not in self.pos and self.startingpos != self.pos:
            print(f"Starting pos {self.startingpos} | Ending pos {self.pos}")

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
            x / self.board.sx,
            y / self.board.sy,
            self.returnTime() / self.board.daylength
        ]

        outputs = self.forward(inputs)

        dx = round(outputs[0] * 2) - 1
        dy = round(outputs[1] * 2) - 1

        #dx = max(min(dx, -1), 1)
        #dy = max(min(dy, -1), 1)

        self.move((dx, dy))

        #print("Movement outputs:", dx, dy, "Location:", self.pos, "Time", self.board.time)

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
        visionSquares = []
        for i in range(self.visionRadius):
            for j in range(i):
                x, y = i - j, -j
                visionSquares.append((self.pos[0] + x, self.pos[1] + y))
            for j in range(i):
                x, y = i - j, j
                visionSquares.append((self.pos[0] + x, self.pos[1] + y))
            for j in range(i):
                x, y = -i + j, -j
                visionSquares.append((self.pos[0] + x, self.pos[1] + y))
            for j in range(i):
                x, y = -i + j, j
                visionSquares.append((self.pos[0] + x, self.pos[1] + y))
        vision = {}
        for i in visionSquares:
            vision[i] = (self.board.board[i[0]][i[1]])
        return vision

    def returnSound(self):
        sounds = []
        sounds.append(self.board.sounds[self.pos[0] + 1][self.pos[1]])
        sounds.append(self.board.sounds[self.pos[0] - 1][self.pos[1]])
        sounds.append(self.board.sounds[self.pos[0]][self.pos[1] + 1])
        sounds.append(self.board.sounds[self.pos[0]][self.pos[1] - 1])
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
        self.pos[0] = max(0, min(self.pos[0], self.board.sx))
        self.pos[1] = max(0, min(self.pos[1], self.board.sy))

    def setR(self, val): self.r = val
    def setG(self, val): self.g = val
    def setB(self, val): self.b = val
    def chirp(self): self.board.addSound(self.pos, (self.r, self.g, self.b))

class Board:

    def __init__(self):
        self.sx = 65
        self.sy = 65
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
        self.daylength = 100

    def addSound(self, pos, rgb):
        pass

def main():
    b = Board()
    creatures = []
    for _ in range(1000): creatures.append(Creature(b, [random.randint(0, b.sx - 1), random.randint(0, b.sy - 1)]))
    for t in range(b.daylength):
        for i in creatures: i.act()
        b.time += 1
        print(t)
    for i in creatures: i.end()

if __name__ == "__main__":
    main()