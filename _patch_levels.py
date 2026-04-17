path = r'C:\Users\ZDominguez\code-explorer\public\index.html'
t = open(path, encoding='utf-8').read()

# Find LEVELS array
s = t.index('const LEVELS = [')
e = t.index('];', s) + 2

new_levels = r"""const LEVELS = [
  // ---- Phase 1: Basic forward + turns ----
  {
    id: 1, title: "First Steps",
    desc: "", grid: [
      [ 0, 0, 0, 2],
    ],
    player: [0,0], startDir: 1, cols: 4, rows: 1,
    functionsUnlocked: false, minSteps: null, maxSteps: null, collectibles: [],
  },
  {
    id: 2, title: "Turn the Corner",
    desc: "", grid: [
      [ 0, 0, 0, 0],
      [-1,-1,-1, 0],
      [-1,-1, 2, 0],
    ],
    player: [0,0], startDir: 1, cols: 4, rows: 3,
    functionsUnlocked: false, minSteps: null, maxSteps: null, collectibles: [],
  },
  // ---- Phase 2: Collectibles ----
  {
    id: 3, title: "Power Cells",
    desc: "", grid: [
      [ 0, 0, 0, 2],
      [ 0, 0, 0, 0],
    ],
    player: [0,0], startDir: 1, cols: 4, rows: 2,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[1,3],[1,2]],
  },
  {
    id: 4, title: "Criss-Cross",
    desc: "", grid: [
      [ 0, 0, 0, 0],
      [ 0, 0, 0, 0],
      [ 0, 0, 0, 0],
      [ 0, 0, 0, 2],
    ],
    player: [0,0], startDir: 1, cols: 4, rows: 4,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[1,3],[2,0]],
  },
  {
    id: 5, title: "Tight Squeeze",
    desc: "", grid: [
      [-1, 0, 2],
      [ 0, 0,-1],
    ],
    player: [0,1], startDir: 1, cols: 3, rows: 2,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[1,0]],
  },
  // ---- Phase 3: Portals ----
  {
    id: 6, title: "Portal Hop",
    desc: "", grid: [
      [ 0, 0, 0, 0],
      [ 0,-1,-1, 0],
      [ 0,-1,-1, 0],
      [ 0, 0, 0, 2],
    ],
    player: [0,0], startDir: 1, cols: 4, rows: 4,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[3,1],[3,2]],
    portals: [[[0,3],[3,0]]],
  },
  {
    id: 7, title: "Portal Path",
    desc: "", grid: [
      [ 0, 0, 0, 2],
      [ 0,-1,-1,-1],
      [ 0,-1,-1,-1],
      [ 0, 0,-1,-1],
    ],
    player: [0,0], startDir: 1, cols: 4, rows: 4,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [],
    portals: [[[0,2],[3,1]]],
  },
  {
    id: 8, title: "Portal Maze",
    desc: "", grid: [
      [ 0, 0, 0,-1],
      [ 0, 0,-1, 0],
      [-1, 0,-1, 0],
      [-1, 0,-1, 2],
    ],
    player: [0,0], startDir: 1, cols: 4, rows: 4,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[1,1],[2,1]],
    portals: [[[0,2],[1,0]],[[3,1],[1,3]]],
  },
  {
    id: 9, title: "Portal Chains",
    desc: "", grid: [
      [ 0, 0, 0, 0, 2],
      [-1,-1, 0,-1,-1],
      [ 0,-1,-1,-1,-1],
      [ 0, 0,-1,-1,-1],
    ],
    player: [0,0], startDir: 1, cols: 5, rows: 4,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [],
    portals: [[[0,3],[3,1]],[[2,0],[1,2]]],
  },
  // ---- Phase 4: Bigger grids ----
  {
    id: 10, title: "The Spiral",
    desc: "", grid: [
      [ 0, 0, 0, 0, 0],
      [ 0,-1, 0,-1, 0],
      [ 0, 0,-1, 0, 0],
      [ 0,-1, 0,-1, 0],
      [ 2, 0, 0, 0, 0],
    ],
    player: [0,0], startDir: 1, cols: 5, rows: 5,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[0,4],[4,4]],
  },
  {
    id: 11, title: "Zigzag",
    desc: "", grid: [
      [ 0, 0, 0],
      [-1,-1, 0],
      [ 0, 0, 0],
      [ 0,-1,-1],
      [ 2,-1,-1],
    ],
    player: [0,0], startDir: 1, cols: 3, rows: 5,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [],
  },
  {
    id: 12, title: "Four Corners",
    desc: "", grid: [
      [ 0, 0, 0,-1,-1],
      [ 0,-1, 2,-1,-1],
      [ 0,-1, 0, 0, 0],
      [ 0,-1,-1,-1, 0],
      [ 0, 0, 0, 0, 0],
    ],
    player: [2,2], startDir: 1, cols: 5, rows: 5,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[2,4],[4,0],[4,4],[0,0]],
  },
  // ---- Phase 5: Complex portals ----
  {
    id: 13, title: "Portal Bridge",
    desc: "", grid: [
      [ 0, 0, 0, 0, 0,-1,-1,-1],
      [-1,-1,-1,-1, 0,-1,-1,-1],
      [-1,-1, 2,-1, 0,-1,-1,-1],
      [-1,-1, 0,-1, 0,-1,-1,-1],
      [-1,-1, 0,-1, 0, 0, 0, 0],
      [ 0, 0, 0,-1,-1,-1,-1,-1],
    ],
    player: [0,0], startDir: 1, cols: 8, rows: 6,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[4,4]],
    portals: [[[4,7],[5,0]]],
  },
  {
    id: 14, title: "Around the Block",
    desc: "", grid: [
      [-1,-1,-1,-1,-1, 0],
      [-1,-1,-1,-1,-1, 0],
      [-1,-1,-1,-1,-1, 0],
      [ 0, 0, 0, 0, 0, 0],
      [ 0,-1,-1,-1,-1, 0],
      [ 0,-1,-1,-1,-1, 0],
      [ 0,-1,-1,-1,-1, 2],
    ],
    player: [3,1], startDir: 1, cols: 6, rows: 7,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[3,0]],
    portals: [[[6,0],[0,5]]],
  },
  {
    id: 15, title: "Portal Gauntlet",
    desc: "", grid: [
      [ 0, 0, 0, 0, 0,-1,-1],
      [-1, 0, 0, 0, 0,-1,-1],
      [-1, 0, 0, 0, 0,-1,-1],
      [-1, 0, 0, 0, 0, 0, 2],
    ],
    player: [0,0], startDir: 1, cols: 7, rows: 4,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[2,1],[1,1],[2,2],[1,2],[2,3],[1,3],[2,4],[1,4]],
    portals: [[[3,1],[0,2]],[[3,2],[0,3]],[[3,3],[0,4]]],
  },
  // ---- Phase 6: Path puzzles ----
  {
    id: 16, title: "Stairway",
    desc: "", grid: [
      [-1,-1,-1,-1, 2, 0, 0],
      [-1,-1,-1,-1,-1,-1, 0],
      [-1,-1,-1,-1, 0, 0, 0],
      [-1,-1,-1,-1, 0,-1,-1],
      [-1,-1, 0, 0, 0,-1,-1],
      [-1,-1, 0,-1,-1,-1,-1],
      [ 0, 0, 0,-1,-1,-1,-1],
    ],
    player: [6,0], startDir: 1, cols: 7, rows: 7,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [],
  },
  {
    id: 17, title: "Shortcut",
    desc: "", grid: [
      [ 0, 0, 0, 0,-1,-1,-1],
      [-1,-1,-1, 0,-1,-1,-1],
      [-1,-1,-1, 0, 2,-1,-1],
      [-1,-1, 0, 0, 0, 0, 0],
    ],
    player: [0,0], startDir: 1, cols: 7, rows: 4,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [],
    portals: [[[3,2],[3,6]]],
  },
  {
    id: 18, title: "Switchback",
    desc: "", grid: [
      [-1,-1, 0, 0],
      [-1,-1,-1, 0],
      [-1,-1, 0, 0],
      [-1,-1, 0,-1],
      [-1,-1, 0,-1],
      [-1, 0, 0,-1],
      [ 2, 0,-1,-1],
    ],
    player: [0,2], startDir: 1, cols: 4, rows: 7,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [],
  },
  {
    id: 19, title: "Portal Express",
    desc: "", grid: [
      [-1,-1,-1, 2],
      [-1,-1,-1, 0],
      [ 0, 0, 0, 0],
      [ 0,-1, 0, 0],
      [ 0, 0, 0, 0],
    ],
    player: [2,0], startDir: 1, cols: 4, rows: 5,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[4,2]],
    portals: [[[3,0],[4,3]]],
  },
  {
    id: 20, title: "Cascade",
    desc: "", grid: [
      [ 0, 0,-1,-1,-1,-1,-1],
      [-1, 0, 0,-1,-1,-1,-1],
      [-1,-1, 0, 0,-1,-1,-1],
      [-1,-1,-1, 0, 0,-1,-1],
      [-1,-1,-1,-1, 0, 0,-1],
      [-1,-1,-1,-1,-1, 0, 0],
      [-1,-1,-1,-1,-1,-1, 2],
    ],
    player: [0,0], startDir: 1, cols: 7, rows: 7,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [],
  },
  {
    id: 21, title: "Plus Sign",
    desc: "", grid: [
      [-1,-1, 2,-1,-1],
      [-1,-1, 0,-1,-1],
      [ 0, 0, 0, 0, 0],
      [-1,-1, 0,-1,-1],
      [-1,-1, 0,-1,-1],
    ],
    player: [2,2], startDir: 1, cols: 5, rows: 5,
    functionsUnlocked: false, minSteps: null, maxSteps: null,
    collectibles: [[2,4],[2,0],[4,2]],
  },
];"""

t = t[:s] + new_levels + t[e:]
open(path, 'w', encoding='utf-8', newline='\n').write(t)
print('OK')
