# this is the file to run dbscans and to show the differences between them

from first_dbscan import MY_DBSCAN
from finished_DBSCAN import MY_DBSCAN_2
# importing from sklearn the thing to make the blobs
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import matplotlib.colors
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import time


# making a blob
# X, y = make_blobs(n_samples=2000, centers=15, n_features=2, random_state=49)

# fig , ax = plt.subplots(figsize=(10,10))

# Mcolors = ["grey",  "blue", "red","black",  "violet", "green", "orange", "hotpink", "brown", "yellow", "purple", "magenta",]

# clr = matplotlib.colors.LinearSegmentedColormap.from_list("", Mcolors)


# making a blob
X, y = make_blobs(n_samples=1000, centers=50, n_features=2, random_state=49)

fig , ax = plt.subplots(figsize=(15,15))

Mcolors = ["grey",  "blue", "red","black",  "violet", "green", "orange", "hotpink", "brown", "yellow", "purple", "magenta",]

clr = matplotlib.colors.LinearSegmentedColormap.from_list("", Mcolors)
# instanciating the DBSCAN
# start = time.time()
# mDB = MY_DBSCAN(.5, 15)

# mDB.fit(X)



# end = time.time()
# print(f"Program took about {end - start}")

# plt.scatter(X[:,0], X[:, 1], c=mDB.label, cmap=clr, )

# plt.show()

# # running the second db scan

start = time.time()
mDB = MY_DBSCAN_2(eps=.5, minNum=10, algorithm="auto", )

mDB.fit(X)



end = time.time()

print(f"Program took about {end - start}")

# print(type(mDB.components))
print(mDB.components)
print(f"This is not using the kd_tree")

plt.scatter(X[:,0], X[:, 1], c=mDB.label, cmap=clr, )

plt.show()

print(f"The label for the point in the prediction is: {mDB.predict([2, 3])}")
print(f"The labels are: {mDB.label}")





# mDB = MY_DBSCAN_2(.6, 15)

# start = time.time()

# mDB.fit(X)

# end = time.time()

# print(f"Program took about {end-start}")

# print(type(mDB.components))
# print(len(mDB.components[0]))
# print(f"This is using the kd_tree")

# plt.scatter(X[:,0], X[:1], c=mDB.label, cmap=clr)

# plt.show()

# print(f"The label for the point in the prediction is: {mDB.predict([2, 3])}")
# print(f"The labels are: {mDB.label}")

# using the k means clustering
# kmeans = KMeans()
# kmeans.fit(X)

# plt.scatter(X[:,0], X[:,1], c=kmeans.labels_, cmap =clr, )
# plt.show()


# start = time.time()
# d = DBSCAN(.5, 15)
# d.fit(X)


# end = time.time()
# print(f"Program took about {end - start}")
# # printing the labels

# plt.scatter(X[:,0], X[:,1], c=d.labels_, cmap=clr)
# plt.show()

