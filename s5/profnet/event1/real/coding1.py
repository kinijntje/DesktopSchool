from ast import arguments
import sys

arguments = sys.argv
chal = open(arguments[1], 'r')
chaline = chal.readlines()
wcounter = 0
words = chaline[49:len(chaline)]
grid = chaline[1:46]

def rollhorfor(word, bina):
    foundindex = -1
    if bina == 1:
        count = 0
    else:
        count = len(grid[0])-1
    while foundindex == -1 and count < len(grid)-1 and count >= 0:
        x = grid[count].strip(' ')
        x = "".join(x.split())
        
        if bina == -1:
            x = x[:-1]

        if word in x:
            foundindex = x.index(word)
            count -= 1
        count += 1*bina

        if bina == -1:
            foundindex = len(x)-foundindex

    return [count, foundindex]

def horizontal(wurd):
    word = "".join(wurd.split())
    length = int(len(word))
    foundindex = -1
    count = 0

    res = rollhorfor(word, 1)
    print(res)
    if res[1] == -1:
        print(f"reverser: {res}")
        res = rollhorfor(word, -1)
    count = res[0]
    foundindex = res[1]

    if foundindex != -1:
        for y in range(foundindex-1, foundindex+length-1):
            editline = list(grid[count])
            editline[y] = "."
            grid[count] = "".join(editline)
        print(wurd)
        words.remove(wurd)


for word in words:
    horizontal(word)
    wcounter += 1

print(grid)

