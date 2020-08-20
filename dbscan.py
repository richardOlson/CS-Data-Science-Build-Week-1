# This is the file that is used to make the class 
# for the DBscan

import numpy as np



class DBSCAN:
    
    def __init__(self, eps, minNum):

        self.eps = eps
        self.minNum = minNum
        self.label = None # this will be the labels that are given to the data
        self.core_samples_indices = None # will take in a matrix with the shape of rows with number of samples
                         # columns with the number of features
        self.__groups = {} # is set to be a dictionary where the value will be a dictionary
                             # of each different cluster.  The first cluster will be the outliers
        self.components = None # This will end up being a numpy nd array that will have all the cores


    def predict(self, ):
        pass

    def fit(self, data):
        """
        This is the method that will accept that 
        data.  It will then create the clusters from  the data and 
        try to ignore the outliers by giving them the label of -1.

        Data: must be in the form of a numpy array. ndarray.
        """
        # check to see if the data is okay to be used in the function
        self.check_dataType(data)

        # initializing some of the things that are used for memory
        self.core_samples_indices = [] # used at the first as a list 
                                       # Will then change it to a ndarray
        self.components = [] # making a temporary list
        self.label = np.full(-1,data.shape[0]) # filling the label as all 
                                               # with if is outlier

        # first will loop through the data begining at one point and then 
        for i in range(data.shape[0]):
            point = data[i] # getting a point one by one and 
                            # then will check the distance between the point 
                            # and all other points to see if we make a 
                            # core point
            self.__find_core_points(point, data, i) # This will look if this point can be a core
                                                 # point
            

        


    def check_dataType(self, data):
        # is used to check the type of data that I passed in to 
        # the class
        if isinstance(data,np.ndarray):
            return 
        else:
            raise Exception("Wrong Data type")



    def __find_core_points(self, point, data, point_index):
        """ 
        This is the method that will find the core points.
        It will use the eps and the min points to find the core points.
        It will check the distance
        """
        
        # points that are in the radius
        within_radius = []
        groups_points_previous = set() # using a set to hold the groups seen 
        # will be looping through the data looking at each 
        # point and checking the distance. To see if less than or equal to eps
        for i in range(data.shape[0]):
            if np.linalg.norm(point - data[i]) <= self.eps: 
                # need to count number of points in the required distance
                within_radius.append(i)
                # putting the points into a group 
                if self.__groups != None:
                    # will loop through the dictionaries
                    for key in self.__groups:
                        val = self.__groups[key].get(i, -1)
                        if val != -1:
                            # this is adding the label to the list
                            # if the index of the point of the data if found in the 
                            # dictionary
                            # this if statement is to check if the label is 
                            # already there with the same points if it is 
                            groups_points_previous.add(key)
                        else:
                            groups_points_previous.add(-1) # If all the points have just
             #TODO   #else:
                    # if in here means the dictionary is empty and there are no groups that 
                    # have been made and therefore this will be first group
                 #   groups_points_previous.add(-1) # -1 means no group is found

        # after the full loop, Will then check to see if we have enough to 
        # label this point as a core point and then begin a label of the cluster
        if len(within_radius) >= self.minNum:
            # calling the method that will put the point in the array 
            # that contains the corepoints
            self.__add_core_point(data, point_index)

        # doing the grouping of the points putting in groups 
        # or possibly merging the groups
        self.__grouping(within_radius, groups_points_previous)




    def __add_core_point(self, data, index):
        """ 
        This is the method that will add a core point to the arrays
        It will add the index of the core point to the list that 
        will then become the core_samples_indices
        """
        if isinstance(self.core_samples_indices, list):
            self.core_samples_indices.append(index)
        else:
            raise Exception("wrong core Sample indices")
        # Adding the components to the 
        if isinstance(self.components, list):
            self.components.append(data[index])
        else:
            raise Exception("Wrong components type")



    def __grouping(self, thePoints,  groups_associated):
        """
        This is the method that will put the points into groups.
        The groups are other points that have a distance connection to them.
          
        """
        # checking to see the length of the set
