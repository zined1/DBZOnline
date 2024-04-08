import pydirectinput
import time


LATENCY = 0
SHIFT_KEY = 'shift'

def walk(direction, n, run):
  if run: pydirectinput.keyDown(SHIFT_KEY)
  for _ in range(n):
    pydirectinput.press([direction]); time.sleep(LATENCY)
  if run: pydirectinput.keyUp(SHIFT_KEY)

def run(process,direction, xDest, yDest):
  pydirectinput.keyDown(SHIFT_KEY)
  freeze = 0
  while freeze <= 3:
    yPos, xPos = process.getCharInfo[:2]
    if xPos == xDest and yPos == yDest: 
      break
    pydirectinput.keyDown(direction); time.sleep(LATENCY)
    yPosTmp, xPosTmp = process.getCharInfo[:2]
    if yPos == yPosTmp and xPos == xPosTmp: 
      freeze += 1
    else:
      freeze = 0
    
  pydirectinput.keyUp(direction)
  pydirectinput.keyUp(SHIFT_KEY)

def up(process, n=1):
  yPos, xPos = process.getCharInfo[:2]
  yDest = max(0, yPos - n)
  xDest = xPos
  run(process, "up", xDest, yDest)

def down(process, n=1):
  map = process.currentMap[1]
  yPos, xPos = process.getCharInfo[:2]
  run(process, "down", xPos, min(map.shape[0] - 1, yPos + n))

def left(process, n=1):
  yPos, xPos = process.getCharInfo[:2]
  run(process, "left", max(0, xPos - n), yPos)

def right(process, n=1):
  map = process.currentMap[1]
  yPos, xPos = process.getCharInfo[:2]
  run(process, "right", min(map.shape[1] - 1, xPos + n), yPos)

#walk
def w_up(n=1, run=False):
  walk("up", n, run)

def w_down(n=1, run=False):
  walk("down", n, run)

def w_left(n=1, run=False):
  walk("left", n, run)

def w_right(n=1, run=False):
  walk("right", n, run)