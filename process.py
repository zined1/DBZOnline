import pymem
import pymem.process
from utils import Cardinal, get_ptr_address, create_moves, get_farthest_point
from bfs import get_path
import move
from extract_map import parse_map


class Process:
  def __init__(self, process_name):
    self.pm = pymem.Pymem(process_name)
    self.PID = self.pm.process_id
    self.base = self.pm.base_address + 0x00086448
    self.xAddr, self.yAddr = (None, None)
    self.idx_map = None

  def getCharPosAddr(self):
    a1 = self.pm.read_int(0x0048723C)
    print(self.base)
    base_12 = self.pm.read_int(get_ptr_address(self.pm, self.base, [], 0xc))
    base_20 = self.pm.read_int(get_ptr_address(self.pm, self.base, [], 0x14))
    
    self.xAddr = 176*(a1 - base_20) + base_12 + 30
    self.yAddr = 176*(a1 - base_20) + base_12 + 32
    self.cardinalAddr = 176*(a1 - base_20) + base_12 + 34
    self.lifeAddr = 176*(a1 - base_20) + base_12 + 36
    self.curLifeAddr = 176*(a1 - base_20) + base_12 + 20
    #return yAddr, xAddr, cardinalAddr, lifeAddr

  @property
  def getCharInfo(self):
    if self.xAddr is None and self.yAddr is None: self.getCharPosAddr()

    self.xPos = self.pm.read_uchar(self.xAddr)
    self.yPos = self.pm.read_uchar(self.yAddr)
    self.life = self.pm.read_int(self.lifeAddr)
    self.curLife = self.pm.read_int(self.curLifeAddr)
    self.cardinal = Cardinal(self.pm.read_uchar(self.cardinalAddr)).name
    
    return self.yPos, self.xPos, self.curLife, self.life, self.cardinal

  @property
  def getnumberOfPNJ(self):
    self.numberOfPNJ = self.pm.read_int(0x487078)
    return self.numberOfPNJ

  @property
  def getIdxMap(self):
    self.idx_map = self.pm.read_int(self.pm.base_address+0x86064)
    return self.idx_map

  @property
  def currentMap(self):
    if self.idx_map is None: self.getIdxMap
    self.name_map, self.map = parse_map(self.idx_map)
    return self.name_map, self.map

  def getPNJInfo(self, nth):
    offset = 96 * nth - 84
    offsetLife = 96 * nth - 88
    xPos = self.pm.read_uchar(get_ptr_address(self.pm, 0x48706C, [], offset))
    yPos = self.pm.read_uchar(get_ptr_address(self.pm, 0x48706C, [], offset+0x2))
    cardinal = Cardinal(self.pm.read_uchar(get_ptr_address(self.pm, 0x48706C, [], offset+0x4))).name
    life = self.pm.read_int(get_ptr_address(self.pm, 0x48706C, [], offsetLife))
    return yPos, xPos, cardinal, life

  def move(self, map, yDest, xDest):
    path, cost = get_path(map[:,1:], (self.yPos,self.xPos), (yDest,xDest)) #farthest_point)
    moves = create_moves(path)
    
    for m in moves:
      side, n = m
      if side == "LEFT": move.left(self, n)
      if side == "RIGHT": move.right(self, n)
      if side == "UP": move.up(self, n)
      if side == "DOWN": move.down(self, n)

    return cost
