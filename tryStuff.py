# this is the file where we will just try things to 
# see how it works

import numpy as np

arr = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]])


print(arr.shape) # the rows is the fist part of the tuple
# now trying to loop through the aray
width = arr.shape
print(type(width))
print("This is the width ", width[0])

for i in range(arr.shape[0]):
    # print out the first row
   print("This is the fist line")
   print(arr[i])