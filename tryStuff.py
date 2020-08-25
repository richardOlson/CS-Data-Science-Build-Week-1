# this is the file where we will just try things to 
# see how it works

import numpy as np

arr = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]])


theSet = {1,2,3,4,5}

# removing something from the set
theSet.discard(1)
print(theSet)
theSet.discard(2)
theSet.discard(3)
theSet.discard(4)
theSet.discard(5)

if not theSet:
    print("The set is empty")
else:
    print("The set is not empty")

# trying to merge two different 
# dictionaries

fisrt = {1:1, 2:2, 3:3}
second = {4:4, 5:5, 6:6}

fisrt.update(second)

print(fisrt)


print(f"This the value of the key 5: {fisrt[5]}")


print(f"This is what the second dictionary is {second}")

# creating a np array
arr = np.array([1,2,3,4])

arr[1] = 100



class Parent:
    def fun(self):
        print("Hi")

class Child(Parent):
    def fun(self):
        print("Bye")

p = Parent

p.fun()