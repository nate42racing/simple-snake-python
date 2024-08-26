# simple-snake-python
A simple game I built in a few hours over the weekend because I was bored. There is room for plenty of refactoring and improvements to be made, which I might do down the road.

## theory

### snake array
The "snake" is built from an array of pygame rect objects that basically just cotain the coordinates of the snake squares. The first in the list is head, and the last is the tail. The graphics are rendered from this list, and the collision detectors are also made functional using this list.

## next steps
- better food spawner to not slow down at long snake
- high score tracker
- smoother snake
- faster input to render
- background and border
- Improved logical updates regardless of render
