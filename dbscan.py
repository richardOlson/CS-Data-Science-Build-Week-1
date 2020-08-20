# This is the file that is used to make the class 
# for the DBscan

import numpy as np



class DBSCAN:
    
    def __init__(self, eps, minNum):

        self.eps = eps
        self.minNum = minNum
        self.label = None # this will be the labels that are given to the data
        self.data = None # will take in a matrix with the shape of rows with number of samples
                         # columns with the number of features
        self.clusters = None # is set to be a dictionary where the value will be a dictionary
                             # of each different cluster.  The first cluster will be the outliers


    def predict(self, ):
        pass

    def fit(self, data):
