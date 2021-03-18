import numpy as np

pos = 38
op = open("1.txt", 'r')
a = np.array(eval(op.read()))
print(a[1])
# for hang in a[pos - 1]:
#     for number in hang:
#         a = number if number == 1 or number == 0 else 2
#         print(a, end='')
#     print()
