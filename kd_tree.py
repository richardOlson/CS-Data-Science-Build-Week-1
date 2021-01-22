# my implementation of the kd_tree

class Node:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None
        self.median_point = None
        self.dimension = None # This will tell the dimension that the 
                              # cut is found at


class KD_tree:
    """
    data: the data that will be passed in
    depth:  this is how much that the data will be broken down
    """
    def __init__(self, data, depth=-1, max_leaf_nodes=None):

        # Making sure the data is the correct form
        if not isinstance(data, list):
            raise Exception("Data is not in correct format, must be a list or list of lists")

        self.num_axis = len(data[0]) # Finding the number axis to which cut the data
        self.head = Node(data)
        

        # Creating depth attribute for the class
        if depth == "full":
            self.depth = -1 # when neg 1 (-1) breaks down the data fully
        else:
            self.depth = depth
        self.num_of_axis = len(data[0])

        
        self.__dimen = []


        if max_leaf_nodes == None:
            self.max_leaf_nodes = 0
        else:
            self.max_leaf_nodes = max_leaf_nodes

        self.max_leaf_nodes = max_leaf_nodes
        self.__build(data, at_depth=0, axis=0)
    


    def __build(self, data, at_depth, axis):
        """
        This is the method that will build the 
        tree.  This function  is recursive and will continue to be called
        while building the tree.
        
        data:  the data that is to be split and put into nodes

        at_depth: this is the current depth that the function is at 
        on the tree.  This is used to compare with the tree instance depth so as
        to not pass it.

        axis: this is the current axis that the cut should be done on
        """

        
        # when to stop the building of the tree
        # if have reach the required depth or the nodes are 
        # less than the max_leaf_nodes
        if self.max_leaf_nodes <= len(data):
            return  
        if self.depth < at_depth and self.depth != -1:
            return
        # checking to see if there are no more to split
        if len(data) == 1 or len(data) == 0:
            return
        
        # below here still building the tree
        
        # will get the median of the data from the dimension --- this returning data sorted
        median, data = self.__get_median(data, axis=axis-1) # axis minus 1 is to have the correct element

        # doing the split of the data along the median.
        # the median will go to the left side
        self.__build(data[:median], at_depth=at_depth + 1, axis=)
        # building the tree
        self.__build_tree(data, self.depth, Node(data))



    def __sort(self, data, axis):
        theLen = len(data[0])
        # looping through the different dimensions
        # sorting the data in place
        
        # adding a list of the axis -- may not need to do this later on
        self.__dimen.append(axis)

        data.sort(key=lambda dataPoint: dataPoint[axis)
        return data

    def __get_median(self, data, axis):
        """
        This function will return the median of the data on the axis 
        that is specified.  If the axis specified doesn't exist, this 
        function will throw an error stating the axis doesn't exist.

        data:  the data to be split. This must be a list of lists

        axis: the axis upon which to split
        """
        # first need to call the sorting function along the axis
        # to be split and then will get the median and return it and
        # also the data that has been sorted

        data = self.__sort(data)
        # now will find the median
        median = None
        # getting the median
        if len(data) % 2 == 0:
            # is even number in the length
            median = data//2
        else:
            median = data //2 + 1
        
        # returning both the data and the median
        return median, data



    def __build_tree(self, data, curDepth, theNode):
        # This will be the recursive function that will 
        # build the tree
        # building will occur until there are 20 point or the 
        # depth is reached
        if len(theNode.data) > 


