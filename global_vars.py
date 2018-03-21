from collections import defaultdict
from datetime import datetime
from geometry import Point

time = datetime(2000, 1, 1, 0, 0, 0)
direction = Point(0, 0, 1)
colors = defaultdict(lambda: (255, 255, 255))
labels = ['N', 'E', 'S', 'W']
MSecsSinceEpoh = 946684800000


colors = defaultdict(lambda: (255, 255, 255), {
    'O': (50, 100, 255),
    'B': (0, 191, 255),
    'A': (255, 255, 255),
    'F': (255, 255, 128),
    'G': (255, 255, 0),
    'K': (255, 160, 0),
    'M': (255, 50, 50)
})
