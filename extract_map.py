import cv2
import numpy as np
import binascii
import os

PATH_MAP = os.getenv('LOCALAPPDATA') + "/DBZOnline/local/maps/"
PATH_TILES = "./tiles/"
EXTRACT_TILES = False
TYPE_COLOR = {i:(5-i)*50 for i in range(0,6)}

def read(hex_array, idx, n=1):
  if n == -1: 
    return hex_array[idx*2:]
  return hex_array[idx*2:idx*2+(n*2)]


def hex_to_string(hex):
  if hex[:2] == '0x': 
    hex = hex[2:]
  return bytes.fromhex(hex).decode('utf-8')


def extract_information_from_map(hexa_map, debug=False):
  idx_len_name_map = 6
  idx_name_map = idx_len_name_map + 2  
  
  len_name_map = int(read(hexa_map, idx_len_name_map), 16)
  name_map = binascii.unhexlify(read(hexa_map, idx_name_map, len_name_map)).decode('latin-1')
  
  idx_len_name_mp3 = idx_name_map + len_name_map + 32
  idx_name_mp3 = idx_len_name_mp3 + 2

  
  len_name_mp3 = int(read(hexa_map, idx_len_name_mp3), 16)
  name_mp3 = "_".join(binascii.unhexlify(read(hexa_map, idx_name_mp3, len_name_mp3)).decode('latin-1').split())

  idx_dimension_y = idx_name_mp3 + len_name_mp3 + 2
  idx_dimension_x = idx_dimension_y + 8
  dimension_y = int(read(hexa_map, idx_dimension_y), 16)
  dimension_x = int(read(hexa_map, idx_dimension_x), 16)
  if debug:
    print("===== DEBUG =====")
    print("\tIndex du nom de la map:", idx_name_map)
    print("\tTaille du nom de la map:", len_name_map)
    print("\tNom de la map:", name_map)
    print("\tIndex du nom du mp3:", idx_name_mp3)
    print("\tTaille du mp3:", len_name_mp3)
    print("\tNom de la mp3:", name_mp3)
    print("\tDimension de la map:("+str(dimension_y)+","+str(dimension_x)+")")
  return name_map, name_mp3, dimension_x, dimension_y, idx_dimension_x

def get_tiles(id, x, y):
  tiles = cv2.imread(PATH_TILES+str(id)+".png", 0)
  output = tiles[y*32:y*32 + 32,(x)*32:(x)*32 + 32]
  return output

def parse_map(id, debug=False):
  filename = PATH_MAP+str(id)+".zm"
  with open(filename, 'rb') as f:
      content = f.read()
  hexa_map = binascii.hexlify(content)

  name_map, name_mp3, dimension_x, dimension_y, start =  extract_information_from_map(hexa_map, debug)
  
  png_map = np.full((dimension_y*32,dimension_x*32), 127)
  block_map = np.full((dimension_y*32,dimension_x*32), 127)
  map = np.full((dimension_y, dimension_x), "_")
  for i in range(0, (dimension_x*dimension_y)):
    if i == 0:
      idx_x_frame = start + 8
      type_pixel = 1
      idx_pixel_map = start + 120
    else:        
      type_pixel = int(read(hexa_map, idx_pixel_map), 16)
      idx_x_frame = idx_pixel_map + 15
    
    idx_y_frame = idx_x_frame + 4
    idx_n_frame = idx_y_frame + 4

    x_frame = int(read(hexa_map, idx_x_frame), 16)
    y_frame = int(read(hexa_map, idx_y_frame), 16)
    n_frame = int(read(hexa_map, idx_n_frame), 16)
    if n_frame != 0:
      map[(i//dimension_x):(i//dimension_x + 1), (i%dimension_x):(i%dimension_x + 1)] = '1' if type_pixel == 0 else '0'

      if debug:        
        print(str(i)+")", "Type:", type_pixel, "| Coords: ("+str(x_frame*32)+","+str(y_frame*32)+")", "| Frame n°:", n_frame, "| Index:", hex(idx_pixel_map))
        color = TYPE_COLOR[type_pixel] if type_pixel in TYPE_COLOR else 127
        block_map[32*(i//dimension_x):32*(i//dimension_x + 1), 32*(i%dimension_x):32*(i%dimension_x + 1)] = np.full((32, 32), color)
        if EXTRACT_TILES:
          tiles = get_tiles(n_frame, x_frame, y_frame)
          png_map[32*(i//dimension_x):32*(i//dimension_x + 1), 32*(i%dimension_x):32*(i%dimension_x + 1)] = tiles
      

    idx_pixel_map = idx_n_frame + 104

  if debug:
    if EXTRACT_TILES:
      cv2.imwrite("./output_map/"+str(id)+"_map.png", png_map)
    cv2.imwrite("./output_map/"+str(id)+"_block.png", block_map)
  return name_map, map
