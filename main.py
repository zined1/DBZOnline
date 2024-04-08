import numpy as np
import os
import keyboard
import pydirectinput
import pyfiglet
import move
import time
import sys
from process import Process
from extract_map import parse_map
from utils import print_styled, directions
from colorama import init, Fore, Style
np.set_printoptions(threshold=sys.maxsize)
init()

def baba_mode():
  while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    if keyboard.is_pressed('esc'): break       
    yPos, xPos, curLife, life, cardinal = process.getCharInfo
    numberOfPNJ = process.getnumberOfPNJ
    idx_map = process.getIdxMap
    name_map, map = parse_map(idx_map)
    print_styled(f"Position (Y,X): ({str(yPos)},{str(xPos)})", Fore.WHITE)
    print_styled(f"Cardinal: {cardinal}", Fore.WHITE)
    print_styled(f"Life: {str(curLife)}/{str(life)}", Fore.WHITE)
    print_styled(f"Map {str(idx_map)}: {name_map}", Fore.WHITE)
    try:
      view = np.copy(map[yPos-1:yPos+2, xPos:xPos+3])
      for direction, symbol in directions:
        dy, dx = direction
        if view[dy, dx] == "1":
          print_styled(symbol, Fore.GREEN)
        else:
          print_styled(symbol, Fore.RED)
    except IndexError:
      print("Out of map?")

    print("NPC:", numberOfPNJ, flush=True)        
    for i in range(1, numberOfPNJ+1):
      yPosPNJ, xPosPNJ, cardinalPNJ, lifePNJ = process.getPNJInfo(i)
      if yPosPNJ == 0 and xPosPNJ == 0: continue
      if lifePNJ != 0:
        print(f"\t{str(i)}) FIGHTER | Current (Y,X) pos: ({str(yPosPNJ)},{str(xPosPNJ)}) | Cardinal: {cardinalPNJ} | Life: {lifePNJ}", flush=True)
      else:
        print(f"\t{str(i)}) NON-FIGHTER | Current (Y,X) pos: ({str(yPosPNJ)},{str(xPosPNJ)}) | Cardinal: {cardinalPNJ}", flush=True)
    print("")
    time.sleep(0.5)

def farm_mode():
  while True:
    numberOfPNJ = process.getnumberOfPNJ
    idx_map = process.getIdxMap
    name_map, map = parse_map(idx_map)
    map_with_enemies = np.copy(map)
    index_with_min_life, min_life = 0, 65536
    for i in range(1, numberOfPNJ+1):
      yPosPNJ, xPosPNJ, cardinalPNJ, lifePNJ = process.getPNJInfo(i)
      if yPosPNJ == 0 and xPosPNJ == 0: continue
      if lifePNJ < min_life:
        index_with_min_life = i
        min_life = lifePNJ

    yPosPNJ, xPosPNJ, cardinalPNJ, lifePNJ = process.getPNJInfo(index_with_min_life)
    map_with_enemies[min(45,max(0, yPosPNJ)),min(45, max(0,xPosPNJ))] = "1"
    process.move(map_with_enemies, yPosPNJ, xPosPNJ)
    pydirectinput.press('ctrl')
    process.move(map_with_enemies, 30, 46)
    movements = [
        (move.w_right, 1, False),
        (move.w_up, 5, False),
        (move.w_left, 4, False),
        (move.right, process, 4),
        (move.down, process, 5),
        (move.left, process, 2),
        (move.down, process, 5),
    ]
    for move_func, *args in movements:
      move_func(*args)

if __name__ == '__main__':
  os.system('cls')
  process = Process("dbzonline.exe")
  while True:
    ascii_banner = pyfiglet.figlet_format("DBZ Online++")
    print_styled(ascii_banner, Fore.RED)
    print_styled('1) Baba Mode', Fore.YELLOW)
    print_styled('2) Farm Mode', Fore.YELLOW)
    mode = int(input("> "))
    if mode == 1:
      baba_mode()
    elif mode == 2:
      farm_mode()
