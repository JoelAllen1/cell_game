### planning ###
# all cells will be movable before play starts including walls but the editing area will not include walls i dont want the player to move




import pygame as py
import random

py.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = py.display.set_mode((WIDTH, HEIGHT))

clock = py.time.Clock()

def wall_cell():
    cell_id = 0
    movable_x = False
    movable_y = False
    rotatable = False
    return(movable_x, movable_y, rotatable)

def blank_cell():
    cell_id = 1
    movable_x = True
    movable_y = True
    rotatable = False
    return(movable_x, movable_y, rotatable)

def blank_x_cell():
    cell_id = 2
    movable_x = True
    movable_y = False
    rotatable = True
    return(movable_x, movable_y, rotatable)

def blank_y_cell():
    cell_id = 3
    movable_x = False
    movable_y = True
    rotatable = True
    return(movable_x, movable_y, rotatable)

def pusher_up_cell():
    cell_id = 4
    movable_x = True
    movable_y = True
    rotatable = True
    return(movable_x, movable_y, rotatable)

def pusher_down_cell():
    cell_id = 5
    movable_x = True
    movable_y = True
    rotatable = True
    return(movable_x, movable_y, rotatable)

def pusher_left_cell():
    cell_id = 6
    movable_x = True
    movable_y = True
    rotatable = True
    return(movable_x, movable_y, rotatable)

def pusher_right_cell():
    cell_id = 7
    movable_x = True
    movable_y = True
    rotatable = True
    return(movable_x, movable_y, rotatable)

def rotator_clockwise_cell():
    cell_id = 8
    movable_x = True
    movable_y = True
    rotatable = False
    return(movable_x, movable_y, rotatable)

def rotator_anitclockwise_cell():
    cell_id = 9
    movable_x = True
    movable_y = True
    rotatable = False
    return(movable_x, movable_y, rotatable)

def generator_up_cell():
    cell_id = 10
    movable_x = True
    movable_y = True
    rotatable = True
    return(movable_x, movable_y, rotatable)

def generator_down_cell():
    cell_id = 11
    movable_x = True
    movable_y = True
    rotatable = True
    return(movable_x, movable_y, rotatable)

def generator_left_cell():
    cell_id = 12
    movable_x = True
    movable_y = True
    rotatable = True
    return(movable_x, movable_y, rotatable)

def generator_right_cell():
    cell_id = 13
    movable_x = True
    movable_y = True
    rotatable = True
    return(movable_x, movable_y, rotatable)


def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        py.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        py.draw.line(screen, GREY, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        py.draw.line(screen, GREY, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def adjust_grid(positions):
    all_neighbors = set()
    new_positions = set()

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 2 or len(neighbors) == 3:
            new_positions.add(position)
    
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue
            
            neighbors.append((x + dx, y + dy))

    return neighbors

def main():
    window_running = True
    sim_running = False
    count = 0
    update_freq = FPS * 0.1

    positions = set()

    while window_running:
        clock.tick(FPS)

        if sim_running:
            count += 1

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        py.display.set_caption("Playing" if sim_running else "Paused")

        for event in py.event.get():
            if event.type == py.QUIT:
                window_running = False
            
            if event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                x, y = py.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    sim_running = not sim_running
                
                if event.key == py.K_c:
                    positions = set()
                    sim_running = False
                    count = 0
                
                if event.key == py.K_g:
                    positions = gen(random.randrange(2, 20) * GRID_WIDTH)
                

    
        screen.fill(BLACK)
        draw_grid(positions)
        py.display.update()   
   
    py.quit()

if __name__ == "__main__":
    main()