from ast import arguments
import sys

arguments = sys.argv
puzzle = open(arguments[1], 'r')
puzzlelines = puzzle.readlines()
puzzlelines = puzzlelines[-len(puzzlelines)+7:]
print(len(puzzlelines))
res = []
count = 7

def findline(string, piece):
    resline = ""
    counting = 0
    while resline == "" and counting < len(puzzlelines):
        line = puzzlelines[counting]
        if string in line and line != piece:
            ind = line.index(string)
            if ind == 0 or line[ind-1] == ' ':
                resline = line
                puzzlelines[counting] = ""
                return line
        counting += 1
    return 'stop'

def rightfill(piece, row, list):
    right = piece.split(' ')[3]
    newpiece = findline(right, piece)
    if (newpiece == 'stop'):
        res.append(list)
    else:
        list.append(newpiece)
        
        rightfill(newpiece, row, list)


def leftfill(piece, row, list):
    left = piece.split(' ')[2]
    newpiece = findline(left, piece)
    if (newpiece == 'stop'):
        res.append(list)
    else:
        list.append(newpiece)
        
        rightfill(newpiece, row, list)
        

while len(res) < 200 and count < len(puzzlelines):
    if (puzzlelines[count] != ''):
        piece = puzzlelines[count]
        print(piece)
        rightfill(piece, count, [])
    count += 1

print(len(res))
print(len(res[0]))