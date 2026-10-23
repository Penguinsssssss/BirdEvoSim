# BirdEvoSim
Benjamin Sullivan Flex Friday project 2026-2027

## 9/25/26
Today I added sound visualization
- emitSound() function
- uses additive blending on squares with more than one color

I also added dummy variables for the brain wiring of a creature

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