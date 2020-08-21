# This is the file that is used to make the class 
# for the DBscan

import numpy as np



class DBSCAN:
    
    def __init__(self, eps, minNum):

        self.eps = eps
        self.minNum = minNum
        self.label = None # this will be the labels that are given to the data

        self.core_samples_indices = None # Become a ndarray that will have the indexes of the core 
                                         # that are found in the data
        
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
        self.core_samples_indices = {} # used at the first as a dictionary 
                                       # Will then change it to a ndarray
                                       # when the fit is finished
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
                            groups_points_previous.add(-1) # means this point is not asscociated with any group
                else:
                    # if in here means the dictionary is empty and there are no groups that 
                    # have been made and therefore this will be first group
                    groups_points_previous.add(-1) # point is associated with no group 

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
        if isinstance(self.core_samples_indices, dict):
            self.core_samples_indices[index] = index
        else:
            raise Exception("Not a dictionary")
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
        # if the set only contains -1 : then we need to make a new group.
        # New groups will just have a name --- (key) that is incremented from other keys

        # First need to check to see if the __groups is empty
        if not self.__groups: # should only get in here if there is only the -1 in set
            # will loop through the points and add them to the new group
            # groups are dictionary of groups which is also a dictionary.
            
            self.__groups[1] = {}  # making the first dictionary group and will have the key of 1
            for i in range(len(thePoints)):
                self.__groups[1][thePoints[i]] = thePoints[i]
            return

        # checking if we need to make a totally new group
        # will have just -1 in the set 
        if len(groups_associated) == 1 and -1 in groups_associated:
            # will iterate through the keys of the dictionary and make one larger than it
            val = 0
            for key in self.__groups:
                if val < key:
                    val = key
            val +=1
            self.__groups[val] = {}
            # adding the values to the new group
            for i in range(len(thePoints)):
                self.__groups[val][thePoints[i]] = thePoints[i]
            return

        # looping throug and finding the smallest key for the dictionary
        
        val = 10000000
        for key in groups_associated:
            if key < val and key != -1:
                val = key
        
        # removing the val from the set
        groups_associated.discard(val)

        if not groups_associated:
            # all the points will need to be grouped to the val
            for i in range(len(thePoints)):
                self.__groups[val] = thePoints[i]
            return 
        else:
            self.__merge(val, groups_associated, thePoints)

        # if ((-1 in groups_associated and len(groups_associated) ==2) or (len(groups_associated) == 1) ):
        #     # If in here will just group with one group type
        #     group_to_add_to = groups_associated[0]

        #     if 
        # Getting the lowest number group that is in the dictionary


    def __merge(self, merge_to_dict_key, merge_from_set, thPoints_index ):
        """
        This is the method that will do the merging of different groups together.
        The calling of this method means that more than one group needs to be grouped/merged
        """
        # TODO need to work on this
        pass
        
