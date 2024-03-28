#6,4,6

#

incr = 4

nums = [1, 2, 3, 4]

for num in nums:
    count = 0
    init = num
    sum = num
    add = -2

    while count < 150:
        num = num + add
        add = add + incr
        sum += num
        count += 1
        
    print(f"{init}: " + f"{sum}")
        
