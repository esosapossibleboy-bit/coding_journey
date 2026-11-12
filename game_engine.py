import random

def move_player(x, y, direction, map_size):
    if direction == "RIGHT":
        x = x + 1
    elif direction == "LEFT":
        x = x - 1
    elif direction == "UP":
        y = y + 1
    elif direction == "DOWN":
        y = y - 1

    if x < 0:
        x = 0
    if x > map_size:
        x = map_size
    if y < 0:
        y = 0
    if y > map_size:
        y = map_size

    return (x, y)

def check_treasure(player_pos, treasure_pos, score):
    if player_pos == treasure_pos:
        return (True, score + 10)
    else:
        return (False, score)

def play_treasure_hunt():
    map_size = 5
    px, py = 0, 0
    tx, ty = random.randint(1, map_size), random.randint(1, map_size)
    score = 0
    
    print("💎 WELCOME TO 2D TREASURE HUNT! (5x5 Map)")
    print("Type UP, DOWN, LEFT, RIGHT (or QUIT to stop)")
    
    while True:
        print(f"\n📍 You are at: ({px}, {py}) | 💎 Treasure is at: ({tx}, {ty}) | 🏆 Score: {score}")
        move = input("Move: ").upper().strip()
        
        if move == "QUIT":
            print("👋 Final Score:", score)
            break
            
        px, py = move_player(px, py, move, map_size)
        collected, score = check_treasure((px, py), (tx, ty), score)
        
        if collected:
            print("🎉 YOU FOUND THE TREASURE! +10 Points!")
            tx, ty = random.randint(0, map_size), random.randint(0, map_size)

if __name__ == "__main__":
    play_treasure_hunt()
