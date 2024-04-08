from enum import Enum
from colorama import Fore, Style

directions = [
    ((0, 1), "\t^"),  # Up
    ((1, 0), "<"),    # Left
    ((1, 2), "\t\t>"),# Right
    ((2, 1), "\tv")   # Down
]

class Cardinal(Enum):
  NORTH = 0
  SUD = 1
  WEST = 2 
  EAST = 3

def print_styled(text, color=Fore.WHITE, bright=True, reset=True):
    style_start = Style.BRIGHT if bright else ''
    style_end = Style.RESET_ALL if reset else ''
    print(f"{style_start}{color}{text}{style_end}")

def get_ptr_address(pm, base, jumps, offset):
  addr = pm.read_int(base)
  for jump in jumps:
    addr = pm.read_int(addr + jump)
  return addr + offset

def get_farthest_point(map, yPos, xPos):
  farthest_point, dist = (0, 0), 0
  for y_ in range(15, 31):
    for x_ in range(10, 35):
      if map[y_][x_] == "1":
        cur_dist = (y_ - yPos)**2 + (x_ - xPos)**2
        if cur_dist > dist:
          dist = cur_dist
          farthest_point = (y_, x_)
  
  return farthest_point
  

def create_moves(path):
  if not path:
    return []

  moves = []
  direction = None
  count = 1

  for i in range(1, len(path)):
    current_move = None
    if path[i][0] == path[i-1][0] + 1:
      current_move = "DOWN"
    elif path[i][0] == path[i-1][0] - 1:
      current_move = "UP"
    elif path[i][1] == path[i-1][1] + 1:
      current_move = "RIGHT"
    elif path[i][1] == path[i-1][1] - 1:
      current_move = "LEFT"

    if current_move != direction:
      if direction is not None:
        moves.append((direction, count))
      direction = current_move
      count = 1
    else:
      count += 1

  if direction:
    moves.append((direction, count))

  return moves