def move_player(x, y, direction, map_size):
    # TODO 1: Update x or y based on 'direction'
    if direction == "RIGHT":
        x += 1
    elif direction == "LEFT":
        x -= 1
    elif direction == "UP":
        y += 1
    elif direction == "DOWN":
        y -= 1
    
    # TODO 2: Keep the player inside the walls (0 to map_size)
    if x < 0:
        x = 0
    if x > map_size:
        x = map_size
    if y < 0:
        y = 0
    if y > map_size:
        y = map_size
    
    # TODO 3: Return the new position as a tuple
    return (x, y)
