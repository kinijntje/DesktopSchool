from ast import arguments
import sys

arguments = sys.argv
map = open(arguments[1], 'r')
maze = open(arguments[2], 'r')
maplines = map.read().split('\n\n')
mazelines = maze.readlines()
resolution = ""

def search(striong, down, right):
    count = 0
    targetline = -1
    while targetline == -1 and count < len(mazelines):
        line = mazelines[count]
        if striong in line:
            ind = line.index(striong) + right
            targetline = count + down
        count += 1
    return mazelines[targetline][ind]

def blocker(block):
    striong = block[0]
    down = int(block[1])
    right = int(block[2])
    return search(striong, down, right)




for line in maplines:
    res = blocker(line.split('\n'))
    resolution += res

print(resolution)



    
