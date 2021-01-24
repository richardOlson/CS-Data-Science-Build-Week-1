import numpy as np
    
class MY_DBSCAN_2:

    def __init__(self, eps, minNum, algorithm="auto", leaf_size=25):
        """
        eps: this is the distance that two points must be equal to or less than to be considered neighbors

        minNum: This is the minimum number of neighors a point must have to be considered a core point.

        algorithm:  This can be "auto", "brute", or "kd_tree".  This determines the way the dbscan function will
        look for its neighbors.

        leaf_size:  This is passed into the kd_tree if it is used. Changing this amount will alter the memory 
        consumption and will also change speed of finding neighbors.
        """
        self.algorithm = algorithm
        self.leaf_size = leaf_size
        self.eps = eps
        self.minNum = minNum
        self.label = [] # this will be the labels that are given to the data

        self.core_samples_indices =[] # Become a ndarray that will have the indexes of the core 
                                         # that are found in the data
        
        
        self.components = [] 
        self.__cluster_border_noise = []
        self.__neighbors = []
        self.__seen = None


    def fit(self, data):
        """
        This is the second try for the clustering 
        algorithm
        """
        # sizing the labeling 
        # a label is put at the index of the data point.  If no label will remain as -1, which is noise
        self.label = [-1] * data.shape[0]
        # the self._neighbors contains the index of the points in the data that are the neighbor
        # indexes neighbors
        self.__neighbors = [None] * data.shape[0]  
        # setting up the seen.  Also the index of the data is the same as the seen list
        self.__seen = [0] * data.shape[0] # 0 means not seen and 1 means the point has been visited
        # the index equal to the data-- contains 0 == border, 1 == core, and -1 == cluster
        # all indexes are initialized as noise
        self.__cluster_border_noise = [-1] * data.shape[0]
        


        # Need to label as clusters or noise
        self.__label_as_cluster_noise(data)
        # starting cluster
        self.__startCluster()
        # now need to go through the starting with one cluster
        # and build 

        # Will now let garbage collect data that
        # don't need
        self.__seen = None
        self.__neighbors = None
        self.__cluster_border_noise = None

       


    def __label_as_cluster_noise(self, data):
        # will loop through the points and will try 
        # to find those that form a cluster or will 
        # be noise
        neigbors = None
        for i in range(len(data)):
            # passing in to the find the neighbors for "point"
            neigbors = self.__findNeighbors(data=data, point=data[i], point_index=i)
            
            # adding all the indexes of the the point's neighbors
            self.__neighbors[i] = neigbors # indexes of all the neigbors
            # finding if to label as noise or core
            if len(neigbors) >= self.minNum:
                # cluster (core) is 1,  noise = -1, border = 0
                self.__cluster_border_noise[i] = 1
                self.core_samples_indices.append(i)
                self.components.append(data[i])
            # if doesn't get labeled will be seen as noise
            # at this point

    

    def __findNeighbors(self, data, point, point_index):
        neigbors = []
        for i in range(len(data)):
            if i != point_index:
                if np.linalg.norm(point - data[i]) <= self.eps:
                    # adding to the neighbors
                    neigbors.append(i) 
        return neigbors

    

    def __makeClusters(self, pointChosen, label):
        
        # add the points to the label chosen
        for point in self.__neighbors[pointChosen]:
            if self.__seen[point] == 0:
            # if not seen 
                if self.__cluster_border_noise[point] == -1: # if was still seen as noise but is a border point
                    self.__seen[point] = 1 
                    self.__cluster_border_noise[point] = 0 # change to a border point
                    # add to label
                    self.label[point] = label
            
                if self.__cluster_border_noise[point] == 1:
                    # will go recursively through this
                    # marking as seen 
                    self.__seen[point] = 1
                    self.label[point] = label
                    # doing the recursive call
                    self.__makeClusters(pointChosen=point, label=label)
        return

    

    def __startCluster(self):
        # will loop through the cluster list
        # if core has not been seen then will use it to call the 
        # recursive method.
        # Will start the label will count with a counter
        label_counter = 1 # This is the label for the cluster that is being built

        for index in self.core_samples_indices:
            if self.__seen[index] == 0:
                self.label[index] = label_counter
                self.__seen[index] = 1
                # calling the recursive method
                self.__makeClusters(index, label_counter)
                label_counter +=1

    def showN(self):
        return self.__neighbors

    
    

    def predict(self, point):
        # Will loop through the core points and find the one that is most 
        # close and then return the label of that core
        if len(point) == len(self.components[0]):
            theDist = 10000000
            val = 0
            theCount = 0
            for i, core in enumerate(self.components):
                val = np.linalg.norm(point - core)
                if  val < theDist:
                    theDist = val
                    theCount = i
            # getting the label from the list
            return self.label[theCount]
        else:
            raise Exception("The point doesn't match the fitted data dimensions")
