# this is the file to run dbscan

from dbscan import MY_DBSCAN
# importing from sklearn the thing to make the blobs
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import matplotlib.colors



# making a blob
X, y = make_blobs(n_samples=1500, centers=17, n_features=2, random_state=49)

# instanciating the DBSCAN
mDB = MY_DBSCAN(.8, 6)

mDB.fit(X)

print(f"These are the labels")
for label in set(mDB.label):
    print(label)

print("these are the core points")
for i in mDB.components:
    print(i)

fig , ax = plt.subplots(figsize=(10,10))

Mcolors = ["grey",  "blue", "red","black",  "green", "orange", "hotpink", "brown", "yellow", "purple",]

c = matplotlib.colors.LinearSegmentedColormap.from_list("", Mcolors)
plt.scatter(X[:,0], X[:, 1], c=mDB.label, cmap=c, label=mDB.label)
plt.legend()
plt.show()

