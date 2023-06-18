from collections import namedtuple

#constants
TIME_STEP = 64
TILE_LENGTH = 0.12 #tile length
AXLE = 0.0568 #axle length 0.0568
WHEEL = 0.02002 #wheel radius 0.02002
SPEED = 6

#Walls values according to  direction (NORTH is not always forward etc.)
WEST =      1    #  00000001 
SOUTH =     2    #  00000010 
EAST =      4    #  00000100 
NORTH =     8    #  00001000

ROWS =  16
COLUMNS = 16
MAZE_SIZE = ROWS * COLUMNS      #16x16
VISITED = 64
MODE = 3                       # 1- keyboard, 2- search, 3 - speeedrun
TESTING = 0  # 1- print sensors values etc. for testing, 0 - no prints
    
#Sets correct target for used mode
if MODE == 3:
    TARGET_CELL = 136
elif MODE == 2:
    TARGET_CELL = 1
else:
    TARGET_CELL = 0

#named tuples for more readable code
Direction = namedtuple("direction", " WEST SOUTH EAST NORTH")
direction = Direction(WEST, SOUTH, EAST, NORTH)

Robot_parameters = namedtuple('robot_parameters','AXLE WHEEL SPEED MODE')
robot_parameters = Robot_parameters(AXLE, WHEEL, SPEED, MODE)

Maze_parameters = namedtuple('maze_parameters',
                              'ROWS COLUMNS MAZE_SIZE VISITED TARGET_CELL TILE_LENGTH')
maze_parameters = Maze_parameters(ROWS, COLUMNS, MAZE_SIZE, VISITED, TARGET_CELL, TILE_LENGTH)

Keys = namedtuple("keys", "forward left back right")
keys = Keys('W', 'A', 'S', 'D')