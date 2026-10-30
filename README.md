# BirdEvoSim
Benjamin Sullivan Flex Friday project 2026-2027


## 10/30/26 1
So far today I've added two things
Mutations
- Surviving creatures make copies of themselves with slight mutations to brain wiring
- Mutated creatures are scattered into the next generation
Moons
- As a simple first criteria, this simulation is a 64x64 grid with two possible scenarios
    - Moon 0
    - Moon 1
- Creatures observe the moon
- If Moon 0
    - Creatures must end day in 8 leftmost tiles to survive
- If Moon 1
    - Creatures must end day in 8 rightmost tiles to survive
- Results
    - 75 surviving creatures after day 2
    - 361 surviving creatures after day 10
    - 725 surviving creatures after day 50
    - 860 surviving creatures after day 100 (final day of sim)

## 10/23/26
Today I worked on adding basic brain wiring
Creatures can now
- See nearby tiles
- Hear each tile within one orthoganal direction
- Know global pos
- See time of day
- Get a random output
- Move to any nearby tile (includes diagonals)
- Make a sound

Creatures currently have a brain with 16 internal neurons and one layer (customizable by variable)
Creatures can recieve input and give output during a second
No evolution yet, but that's my goal for next week

## 9/25/26
Today I added sound visualization
- emitSound() function
- uses additive blending on squares with more than one color

I also added dummy variables for the brain wiring of a creature