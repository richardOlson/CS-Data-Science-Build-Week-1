import numpy as np
    
class MY_DBSCAN_2:

    def __init__(self, eps, minNum):
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
        self.label = [-1] * data.shape[0]
        self.__neighbors = [None] * data.shape[0]
        # setting up the seen 
        self.__seen = [0] * data.shape[0]
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
            # passing in to the find the neighbors
            neigbors = self.__findNeighbors(data=data, point=data[i], point_index=i)
            
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
                if self.__cluster_border_noise[point] == -1:
                    self.__seen[point] = 1
                    self.__cluster_border_noise[point] = 0
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
        label_counter = 1

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
