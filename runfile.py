# this is the file to run dbscan

from dbscan import MY_DBSCAN
# importing from sklearn the thing to make the blobs
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import matplotlib.colors
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN


# making a blob
X, y = make_blobs(n_samples=2000, centers=15, n_features=2, random_state=49)

fig , ax = plt.subplots(figsize=(10,10))

Mcolors = ["grey",  "blue", "red","black",  "violet", "green", "orange", "hotpink", "brown", "yellow", "purple",]

clr = matplotlib.colors.LinearSegmentedColormap.from_list("", Mcolors)

# instanciating the DBSCAN
mDB = MY_DBSCAN(.5, 15)

mDB.fit_(X)

print(f"These are the labels")
for label in set(mDB.label):
    print(label)

# print("these are the core points")
# for i in mDB.components:
#     print(i)


plt.scatter(X[:,0], X[:, 1], c=mDB.label, cmap=clr, )

plt.show()

# using the k means clustering
# kmeans = KMeans()
# kmeans.fit(X)

# plt.scatter(X[:,0], X[:,1], c=kmeans.labels_, cmap =clr, )
# plt.show()


# d = DBSCAN(.5, 6)
# d.fit(X)

# # printing the labels

# plt.scatter(X[:,0], X[:,1], c=d.labels_, cmap=clr)
# plt.show()
