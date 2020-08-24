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
        self.core_samples_indices = [] # used at the first as a dictionary 
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
                                                 # Through this method we will group the points then
                                                 # they will be ready for labeling
            

        


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
        
        # boolean to tell in grouping function that 
        # this function has a core point
        hasCorePoint = False
        # points that are in the radius
        within_radius = []
        groups_points_previous = set() # using a set to hold the groups seen 
        # will be looping through the data looking at each 
        # point and checking the distance. To see if less than or equal to eps
        for i in range(data.shape[0]):
            if np.linalg.norm(point - data[i]) <= self.eps: 
                # need to count number of points in the required distance
                #within_radius.append(i)
                
                # putting the points into a group 
                if self.__groups != None:
                    # will loop through the dictionaries
                    for key in self.__groups:
                        val = self.__groups[key][0].get(i, -1) # The bracket is because the value is a list 
                                                               # where the 0 element is a dictionary--group, and 
                                                               # the second 1 element will contain either 
                                                               # 1 or a 0.  1 means has core point, 0 no.
                        if val != -1:
                            # this is adding the label to the list
                            # if the index of the point of the data if found in the 
                            # dictionary
                            # this if statement is to check if the label is 
                            # already there with the same points if it is 
                            groups_points_previous.add(key)
                            # putting a tuple in the list
                            within_radius.append((i, key))
                        else:
                            groups_points_previous.add(-1) # means this point is not asscociated with any group
                            within_radius.append((i, -1))
                else:
                    # if in here means the dictionary is empty and there are no groups that 
                    # have been made and therefore this will be first group
                    groups_points_previous.add(-1) # point is associated with no group 
                    within_radius.append((i,-1))

        # after the full loop, Will then check to see if we have enough to 
        # label this point as a core point and then begin a label of the cluster
        if len(within_radius) >= self.minNum:
            # calling the method that will put the point in the array 
            # that contains the corepoints
            self.__add_core_point(data, point_index)
            hasCorePoint = True

        # doing the grouping of the points putting in groups 
        # or possibly merging the groups
        self.__grouping(within_radius, groups_points_previous, hasCorePoint)




    def __add_core_point(self, data, index):
        """ 
        This is the method that will add a core point to the arrays
        It will add the index of the core point to the list that 
        will then become the core_samples_indices
        """
        if isinstance(self.core_samples_indices, list):
            self.core_samples_indices.append(index)
        else:
            raise Exception("Not a dictionary")
        # Adding the components to the 
        if isinstance(self.components, list):
            self.components.append(data[index])
        else:
            raise Exception("Wrong components type")



    def __grouping(self, thePoints,  groups_associated, hasCorePoint):
        """
        This is the method that will put the points into groups.
        The groups are other points that have a distance connection to them.
          
        """
        core = 1 if hasCorePoint else 0
        # if the set only contains -1 : then we need to make a new group.
        # New groups will just have a name --- (key) that is incremented from other keys

        # First need to check to see if the __groups is empty
        if not self.__groups: # should only get in here if there is only the -1 in set
            # will loop through the points and add them to the new group
            # groups are dictionary of groups which is also a dictionary.
            
            self.__groups[1] = [{}, core]  # making dictionary group and will have the key of 1 
            for i in range(len(thePoints)):
                self.__groups[1][thePoints[i][0]] = thePoints[i][0] # Adding the points to the group
            #self.__labeling(thePoints, groups_associated, hasCorePoint) # function to label points
            return

        # checking if we need to make a totally new group
        # will have just -1 in the set , so all the labels will be just with the group made
        if len(groups_associated) == 1 and -1 in groups_associated:
            # will iterate through the keys of the dictionary and make one larger than it
            val = 0
            for key in self.__groups:
                if val < key:
                    val = key
            val +=1
            self.__groups[val] = [{}, core]
            # adding the values to the new group
            for i in range(len(thePoints)):
                self.__groups[val][0][thePoints[i][0]] = thePoints[i][0] # putting in dictionary
            #self.__labeling(thePoints, groups_associated, hasCorePoint) # function to label points
            return

        # looping through and finding the dictionary that is the largest
        # so that we can merge into it (keeping the largest of the dictionaries).
        val = 0
        numPts = 0
        for key in groups_associated:
            if key != -1: # Won't look into the key with neg 1 becuse there is no
                          # dictionary with this key 

                if len(self.__groups[key][0]) > numPts:
                    val = key
                    numPts = len(self.__groups[key][0])
        
        # removing the val from the set
        groups_associated.discard(val)

        # if looking in here, all the points will need to be
        # assigned to the val group because it is the only one
        if not groups_associated:
            isCore = False
            # all the points will need to be grouped to the val
            for i in range(len(thePoints)):
                self.__groups[val][0] = thePoints[i][0]
            if core:
                self.__groups[val][1] = 1 # stating that this group has a core in it and therefore is not outlier 
            self.__labeling(dict_belong_to, thePoints, dicts_come_from=None, hasCorePoint) # function to label points
            return 
        else:
            self.__merge(val, groups_associated, thePoints, hasCorePoint)

        # if ((-1 in groups_associated and len(groups_associated) ==2) or (len(groups_associated) == 1) ):
        #     # If in here will just group with one group type
        #     group_to_add_to = groups_associated[0]

        #     if 
        # Getting the lowest number group that is in the dictionary


    def __merge(self, merge_to_dict_key, merge_from_set, thePoints_index, hasCorePoint):
        """
        This is the method that will do the merging of different groups together.
        The calling of this method means that more than one group needs to be grouped/merged
        """
        isCore = False
        # Looping through the merge from set
        for i in range(len(merge_from_set)):
            # Will merge the other dictionaries to the biggest dictionary
            self.__groups[merge_to_dict_key][0].update(self.__groups[merge_from_set[i]][0])
            # checking to see if any of the dictionaries has a core point
            if self.__groups[merge_from_set[i]][1] == 1:
                isCore = True
            # removing the dictionary now that it has been merged
            self.__groups.pop(merge_from_set[i])
        # then doing a for loop that will add the points in thePoints_index that have
        # -1 as the point they are linked to
        for i in range(len(thePoints_index)):
            if thePoints_index[i][1] == -1:
                # add the point to the dictionary
                self.__groups[merge_to_dict_key][thePoints_index[i][0]] = thePoints_index[i[0]]
        # setting the group to say it has a core point if the group of points or a merged dictionary 
        # has a core point
        if hasCorePoint == True or isCore == True:
            self.__groups[merge_to_dict_key][1] = 1

    
    # TODO finish this method

    def __labeling(self, dict_belong_to, thePoints, dicts_come_from=None, hasCorePoint):
        """
        This method will will label the each of the points.
        If the group does not have a core point in it it will be labeled with a -1.
        """
        # will need to loop through the dictionaries.  If they have a core point in them then the 
        # whole group will be labeled.  It will then move to the next dictionary and check to see if 
        # it has a core point and if it does it will be labeled also with the next label.(incremented)

        # Looping through the dictionaries
        for key in self.__groups:
            # start looking through the core points to see if any of them are in 
            # the dictionary
            for i in self.
            if val != -1: # This means that the key is in 


