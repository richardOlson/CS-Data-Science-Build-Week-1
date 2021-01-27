import numpy as np
from kd_tree import KD_tree
    
class MY_DBSCAN_2:

    def __init__(self, eps, minNum, algorithm="auto", leaf_size=15):
        """
        eps: this is the distance that two points must be equal to or less than to be considered neighbors

        minNum: This is the minimum number of neighors a point must have to be considered a core point.

        algorithm:  This can be "auto", "brute", or "kd_tree".  This determines the way the dbscan function will
        look for its neighbors.

        leaf_size:  This is passed into the kd_tree if it is used. Changing this amount will alter the memory 
        consumption and will also change speed of finding neighbors.
        """

        
        self.algorithm = algorithm
        # the Tree is the holder of the KD_tree is there is one to be used
        self.tree = None
        self.leaf_size = leaf_size
        self.eps = eps
        self.minNum = minNum -1
        self.label = [] # this will be the labels that are given to the data

        self.core_samples_indices =[] # Become a ndarray that will have the indexes of the core 
                                         # that are found in the data
        
        
        


        self.components = [] 
        self.__cluster_border_noise = []
        self.__neighbors = []
        self.__seen = None

    
    def __choose_neighbor_algo(self, data):
        """
        This is the function that will set the algorithm to be used. This function will 
        instanciate the kd_tree and put the tree value on the attribute self.tree.
        If "auto" is passed in on DBSCAN this function will decide if a tree or brute force is used.

        self.algorithm will be changed to the end result of what this function causes, ie.
        It will be "brute" if brute is determined to be more efficient and will be "kd_tree" 
        if this is determined to be more efficient.

        Returns the attribute for self.algorithm
        """
        if self.algorithm == "auto":
            # calling the function to return if should
            # be a brute or a kd-tree
            self.algorithm = self.__brute_kd(data)
                        

        # if is kd will then make the tree
        if self.algorithm == "kd_tree":
            # making the tree
            self.tree = KD_tree(data=data, max_leaf_nodes=self.leaf_size)
            




    def __brute_kd(self, data):
        """
        Returns "brute" or "kd_tree"
        Looks at the size of the data to determine which
        type should be done.
        """
        if len(data) > 30:
            return "kd_tree"
        else:
            return "brute"

    
    

    def fit(self, data):
        """
        This is the second try for the clustering 
        algorithm
        """


        # sizing the labeling 
        # a label is put at the index of the data point.  If no label will remain as -1, which is noise
        self.label = [-1] * data.shape[0]

        
        # calling the fuction to determine the algorithm
        # This is used if not "brute"
        if self.algorithm == "kd_tree" or self.algorithm == "auto":
            # calling the function to choose and then set up the
            # kd_tree if necessary
            self.__choose_neighbor_algo(data)
        
        

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
            if self.algorithm == "kd_tree":
                # will be doing the kd_tree here to get the neighbors
                # finding the neighbor of the point
                neigbors = self.tree.find_kd_tree_neighbors(eps=self.eps, point=data[i], point_index=i)
            
            # Using the brute fore manner of finding the neighbors
            else:    
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
            if index == 31:
                breakpoint()
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


    def get_neighbors(self, index):
        """
        Function to get the neighbors at the index passed in.
        """
        return self.__neighbors[index]


    def get_cluster_border_val(self, index):
        """
        Function to get wether a value is marked as a cluster or border or noise
        """
        return self.__cluster_border_noise[index]