from pattern_generator import *
from graphics_tk import draw_tiles

SCALAR = 10
ITERATIONS = 5

for i in range(ITERATIONS):
    next_generation()

s = draw_tiles(vertices_to_draw, width=1000, height=1000,
               scalar=SCALAR)

print(s)
