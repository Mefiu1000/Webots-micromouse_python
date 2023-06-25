"""flood_fill_py controller."""

from controller import Robot, Keyboard
from collections import namedtuple
from threading import Thread

#my modules
from Constants import *
import map_functions
import move_functions
import algorythm_functions
import draw_maze
import var


def run_robot(robot):
 
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')

    left_motor.setVelocity(robot_parameters.SPEED)
    right_motor.setVelocity(robot_parameters.SPEED)

    ps_left = robot.getDevice("left wheel sensor")
    ps_left.enable(TIME_STEP)
    ps_right = robot.getDevice("right wheel sensor")
    ps_right.enable(TIME_STEP)

    maze_map = [0] * maze_parameters.MAZE_SIZE
    distance = [255] * maze_parameters.MAZE_SIZE
    
    target = maze_parameters.TARGET_CELL            # robot start target
    robot_position  = maze_parameters.START_CELL    # robot start position
    move_direction = direction.NORTH                # where robot wants to move on start
    mode = mode_params.MODE                         # 1- keyboard, 2- search, 3 - speeedrun
    start = 1                                       # to open file 1 time
    robot_orientation = direction.NORTH             # robot start orientation
    maze_map = map_functions.init_maze_map(maze_map)
    var.maze_map_global = maze_map
    if mode_params.MODE == mode_params.KEYBOARD:
        keyboard = Keyboard()
        keyboard.enable(TIME_STEP)

    ps = [''] * 8
    ps_names = (
        "ps0", "ps1", "ps2", "ps3",
          "ps4", "ps5", "ps6", "ps7"
    )
    for i in range(len(ps_names)):
        ps[i] = robot.getDevice(ps_names[i])
        ps[i].enable(TIME_STEP)
    
    tof = robot.getDevice('tof')
    tof.enable(TIME_STEP)

    while robot.step(TIME_STEP) != -1:
        if mode_params.TESTING:
            print('sensor tof %.2f'% tof.getValue()) #do usuniecia

        if mode_params.TESTING:
            print('sensor ps6 left %.2f'% ps[6].getValue()) #do usuniecia
        
        if mode_params.TESTING:
            print('sensor ps1 right %.2f'% ps[1].getValue()) #do usuniecia

        match mode:
            case 1: #keyboard
                key = keyboard.get_key()
                if key in keys:
                    match key:
                        case keys.forward:
                            print(key)
                            move_functions.move_1_tile(robot, left_motor, right_motor, ps_left, ps_right, ps)
                        case keys.right | keys.left | keys.back:
                            print(key)
                            move_functions.turn(robot, key, left_motor, right_motor, ps_left, ps_right)

            case 2: #search
                
                if start:
                    #run in another thread to make it possible to look on it during robot run
                    Maze_thread = Thread(target = draw_maze.draw_maze, args = (var.maze_map_global, var.distance_global), daemon = True)
                    Maze_thread.start()
                    
                    start = 0
                if mode_params.TESTING:
                    timer = robot.getTime()

                left_wall, front_wall, right_wall, back_wall, avg5_left_sensor, avg2_right_sensor = map_functions.detect_walls(robot, ps, 5)

                if left_wall:
                    maze_map = map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.WEST)
                
                if front_wall:
                    maze_map = map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.NORTH)
                
                if right_wall:
                    maze_map = map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.EAST)

                if back_wall:
                    maze_map = map_functions.add_wall(maze_map, robot_position, robot_orientation, direction.SOUTH)

                # print('MAZE MAP')
                # map_functions.print_array(maze_map, 0)
                # print('MAZE MAP')


                distance = map_functions.init_distance_map(distance, target) #reset path

                distance = algorythm_functions.floodfill(maze_map, distance) #path

                var.robot_pos = robot_position

                var.maze_map_global = maze_map

                if var.distance_global != distance:
                    var.distance_global = distance
                    var.distance_update = True

                var.target_global = target
                var.drawing_event.set()
                
                if var.searching_end:
                    print('Target reached')
                    print('Searching time: %.2f'% robot.getTime(),'s')
                    input("press any key to end")
                    exit(0)

                move_direction = algorythm_functions.where_to_move(maze_map, robot_position, distance, robot_orientation)

                robot_orientation =  move_functions.move(robot_orientation, move_direction,\
                                                        robot, left_motor, right_motor, ps_left, ps_right, ps)
                
                if mode_params.TESTING:
                    timer = robot.getTime() - timer
                    print('Move time: %.2f'% timer,'s')

                robot_position = algorythm_functions.change_position(robot_position, robot_orientation)
                
                maze_map[robot_position] = maze_map[robot_position] | maze_parameters.VISITED   #mark visited tile

                if robot_position == target:
                    target = algorythm_functions.change_target(maze_map, robot_position, distance, target)
                
                var.main_event.wait()
                var.main_event.clear()

            case 3: #speedrun

                if start:
                    distance = algorythm_functions.read_file('path.txt')
                    maze_map = algorythm_functions.read_file('maze.txt')

                    #run in another thread to make it possible to look on it during robot run
                    Maze_thread = Thread(target = draw_maze.draw_maze, args = (maze_map, distance), daemon = True)
                    Maze_thread.start()
                    
                    start = 0

                move_direction = algorythm_functions.where_to_move(maze_map, robot_position, distance, robot_orientation)

                robot_orientation =  move_functions.move(robot_orientation, move_direction,\
                                                        robot, left_motor, right_motor, ps_left, ps_right, ps)
                
                robot_position = algorythm_functions.change_position(robot_position, robot_orientation)
                
                var.robot_pos = robot_position

                var.drawing_event.set()
                
                var.main_event.wait()
                var.main_event.clear()

                if robot_position == target:
                    print('Target reached')
                    print('Speedrun time: %.2f'% robot.getTime(),'s')
                    input("press any key to end")
                    exit(0)
                    
if __name__ == "__main__":
    
    robot = Robot()
    
    run_robot(robot)

    Robot_thread = Thread(target = run_robot, args = robot, daemon = True)
    Robot_thread.start()