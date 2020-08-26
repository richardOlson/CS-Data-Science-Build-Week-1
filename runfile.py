# this is the file to run dbscan

from dbscan import MY_DBSCAN
# importing from sklearn the thing to make the blobs
from sklearn.datasets import make_blobs



# making a blob
X, y = make_blobs(n_samples=10, centers=3, n_features=2, random_state=49)

# instanciating the DBSCAN
mDB = MY_DBSCAN(3, 2)

mDB.fit(X)