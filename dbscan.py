# This is the file that is used to make the class 
# for the DBscan

import numpy as np



class MY_DBSCAN:
    
    def __init__(self, eps, minNum):

        self.eps = eps
        self.minNum = minNum
        self.label = [] # this will be the labels that are given to the data

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
        self.components = [] # making a temporary listipdb.set_trace()
        
        self.label = self.__return_label_arr(data=data)

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
        #breakpoint()

            

        


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
                foundDict = False
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
                            # if the index of the point of the data is found in the 
                            # dictionary
                            # this if statement is to check if the label is 
                            # already there with the same points if it is 
                            groups_points_previous.add(key)
                            # putting a tuple in the list
                            within_radius.append((i, key))
                            foundDict = True
                            break # need to break out of the loop
                    if foundDict == False:
                        #groups_points_previous.add(-1) # means this point is not asscociated with any group
                        within_radius.append((i, -1))
                else:
                    # if in here means the dictionary is empty and there are no groups that 
                    # have been made and therefore this will be first group
                    #groups_points_previous.add(-1) # point is associated with no group 
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
        
    #     """
    #     This is the method that will put the points into groups.
    #     The groups are other points that have a distance connection to them.
          
    #     """
        core = 1 if hasCorePoint else 0
        isCore = 0 # This is for passing into the labeling function
    #     # if the set only contains -1 : then we need to make a new group.
    #     # New groups will just have a name --- (key) that is incremented from other keys

    #     # First need to check to see if the __groups is empty
        if not self.__groups: # should only get in here if there is only the -1 in set
    #         # will loop through the points and add them to the new group
    #         # groups are dictionary of groups which is also a dictionary.
            
            self.__groups[1] = [{}, core]  # making dictionary group and will have the key of 1 
            for i in range(len(thePoints)):
               
                self.__groups[1][0][thePoints[i][0]] = thePoints[i][0] # Adding the points to the group
            self.__labeling(dict_belong_to_key=1, thePoints=thePoints, dicts_come_from=None, is_a_core_point=core) # function to label points
            return

        # checking if we need to make a totally new group
        # will have just -1 in the set , so all the labels will be just with the group made
        if len(groups_associated) == 0:
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
            self.__labeling(dict_belong_to_key=val, thePoints=thePoints, dicts_come_from=None, is_a_core_point=core) # function to label points
            return

        # looping through and finding the dictionary that is the largest
        # so that we can merge into it (keeping the largest of the dictionaries).
        # also will check to see if any of the dictionaries has marked as a core
        val = 0
        numPts = 0
        for key in groups_associated:
            
            if len(self.__groups[key][0]) > numPts:
                val = key
                numPts = len(self.__groups[key][0])
            # checking all dictionaries if they have a core point
            if self.__groups[key][1] == 1:
                hasCorePoint = True # It is set to that becuase one of the dictionaries has a core point
                core = 1
        
        # removing the val from the set
        groups_associated.discard(val)

        # if looking in here, all the points will need to be
        # assigned to the val group because it is the only one
        if not groups_associated:
            # all the points will need to be grouped to the val
            for i in range(len(thePoints)):
                self.__groups[val][0][thePoints[i][0]] = thePoints[i][0]
            
            self.__labeling(dict_belong_to_key=val, thePoints=thePoints, dicts_come_from=None, is_a_core_point=core) # function to label points
            return 
        else:
            self.__merge(val, groups_associated, thePoints, hasCorePoint) # will call the other labeling function call from inside here

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
        
        isCore = 0
        beenLabeled = False # This is to keep track of if the large 
        #                                      # dictionary has been labeled or not
        if self.__groups[merge_to_dict_key][1] == 1:
            beenLabeled = True # if it has a 1 means that it has been labeled
        
        if hasCorePoint == True: # This is to say that there is a core point
            isCore = 1           # either in the points or the dictionary

        # making the set into a list
        merge_from_list = list(merge_from_set)
        # # Looping through the merge from set
        for i in range(len(merge_from_list)):
            # Checking to see if we need to label the large Dictionary
            if ((beenLabeled == False) and (hasCorePoint == True)):    
                # if in here need to label the large dictionary
                self.__labeling(dict_belong_to_key=merge_to_dict_key, thePoints=thePoints_index, dicts_come_from=None, 
                                is_a_core_point=isCore, label_merge_to_dict=True) 
                beenLabeled = True
                # setting the value of the large dictionary to be a 1 in the list -- means it will have a core within it
                self.__groups[merge_to_dict_key][1] = 1
            # before merging them we will label the merge -- this will only happen when there are core points 
            # checking to see if we 
            
                
            # Labeling the contents of the dictionary merge from
            self.__labeling(dict_belong_to_key=merge_to_dict_key, thePoints=thePoints_index, 
                            dicts_come_from=self.__groups[merge_from_list[i]][0], is_a_core_point=isCore)

            
                # Will merge the other dictionaries to the biggest dictionary
            self.__groups[merge_to_dict_key][0].update(self.__groups[merge_from_list[i]][0])

            # removing the dictionary now that it has been merged
            self.__groups.pop(merge_from_list[i])
        
        # then doing a for loop that will add the points in thePoints_index that have
        # -1 as the point they are linked to
        for i in range(len(thePoints_index)):
            if thePoints_index[i][1] == -1:
                # add the point to the dictionary
                self.__groups[merge_to_dict_key][0][thePoints_index[i][0]] = thePoints_index[i][0]
                # checking to see if the is a core point to make it so that we should label them
                if hasCorePoint:
                    # will label these as they go through this loop
                    self.label[thePoints_index[i][0]] = merge_to_dict_key
        
    
    

    def __labeling(self, dict_belong_to_key, thePoints, dicts_come_from=None, is_a_core_point=1, label_merge_to_dict=False):
        
        """
        This method will will label the each of the points.
        If the group does not have a core point in it it will be labeled with a -1.
        """
        # will need to loop through the dictionaries.  If they have a core point in them then the 
        # whole group will be labeled.  It will then move to the next dictionary and check to see if 
        # it has a core point and if it does it will be labeled also with the next label.(incremented)

        # in here if we are to just label the dictionary that we are merging into
        if label_merge_to_dict == True and is_a_core_point == 1:
            # need to loop through the keys in the dictionary
            for key in self.__groups[dict_belong_to_key][0]:
                self.label[key] = dict_belong_to_key
            return

        if dicts_come_from == None and is_a_core_point == 1:
            # checking to see if there was a core point
            
            # looping through the points and labeling them
            for i in range(len(thePoints)):
                # if the point is not associated with the dict_to_belong to 
                # and becuase there was a core point will label them to the dictiornary
                if thePoints[i][1] != dict_belong_to_key:
                    self.label[thePoints[i][0]] = dict_belong_to_key # This will label the points 
            return

        # This code below is what will be run when we need to label the contents of one dictionary to match the
        # other dictionary because there is a core point somewhere in there
        if is_a_core_point == 1 and dicts_come_from != None:
            # looping through one dictionary and labeling its points to the other dictionary
            for key in dicts_come_from: # this is a list
                self.label[key] = dict_belong_to_key
            return



    def __return_label_arr(self, data):
        """ 
        Method to make the label array acorrding to the 
        size of the data that will come in.
        """
        theSize = data.shape[0]

        # making a list
        theList = [-1] * theSize
        
        # making the numpy array
        arr = np.array(theList)
        return arr

    def ggroups(self):
        return self.__groups
