from collections import deque

def create_grid_distance(grid, source):
  travels = {source: [None, 0]}
  queue = deque([source])

  while queue:
    y, x = queue.popleft()
    for X, Y in ([x, y + 1], [x - 1, y], [x, y - 1], [x + 1, y]):
      current_cost_from_s = travels[(y, x)][1]
      if 0 <= X < grid.shape[1] and 0 <= Y < grid.shape[0] and (grid[Y][X] == '1'):
        if (Y, X) not in travels or travels[(Y, X)][1] > current_cost_from_s + 1:
          travels[(Y, X)] = [(y, x), current_cost_from_s + 1]
          queue.append((Y, X))

  return travels

def get_path(grid, source, dest):
  travels = create_grid_distance(grid, source)
  if dest not in travels:
    return [], -1
  
  cur = dest
  shortest_path = [cur]
  cost = travels[cur][1]
  while cur:
    cur = travels[cur][0]
    if cur is not None:
      shortest_path.append(cur)

  return shortest_path[::-1], cost


