# my implementation of the kd_tree

class Node:
    def __init__(self, data=None, median=None, median_number=None, greater_lesser=None):
        self.data = data
        self.right = None
        self.left = None
        self.greater_lesser = None # This is to tell if this node is a right or left node (which side of the median)
        self.median_point = median
        self.median_number = None
        self.dimension = None # This will tell the dimension that the 
                              # cut is found at


class KD_tree:
    """
    data: the data that will be passed in
    depth:  this is how much that the data will be broken down
    When the depth is left as -1, then it will go completely to just one leaf on the last node

    max_leaf_nodes: If the number of leaves is equal to or less than max_leaf_nodes then the building of 
    the tree will stop
    """
    def __init__(self, data, depth=-1, max_leaf_nodes=None):

        # Making sure the data is the correct form
        if not isinstance(data, list):
            raise Exception("Data is not in correct format, must be a list or list of lists")

        
        self.head = Node() # making the first Node as the head
        
        # Creating depth attribute for the class
        self.depth = depth

        # Finding the number axis to which cut the data
        self.num_of_axis = len(data[0])
        
        self.__dimen = []


        if max_leaf_nodes == None:
            self.max_leaf_nodes = -1
        else:
            self.max_leaf_nodes = max_leaf_nodes

        #self.max_leaf_nodes = max_leaf_nodes
        # building the tree with making the nodes
        self.__build(data, at_depth=0, axis=0, curNode=self.head)
    


    def __build(self, data, at_depth, axis, curNode):
        """
        This is the method that will build the 
        tree.  This function  is recursive and will continue to be called
        while building the tree.
        
        data:  the data that is to be split and put into nodes

        at_depth: this is the current depth that the function is at 
        on the tree.  This is used to compare with the tree instance depth so as
        to not pass it.

        median: this is the median at with the cut was done when entering this function
        if it is none then there is no cut and is the first node likely or an end node

        curNode:  This is the currrent node that the tree is on when entering this function

        axis: this is the current axis that the cut should be done on
        """

        
        # when to stop the building of the tree
        # if have reach the required depth or the nodes are 
        # less than the max_leaf_nodes
        if self.max_leaf_nodes >= len(data) and self.max_leaf_nodes != -1:
            # will need to add the data to the current node and then return
            curNode.data = data # this is a list of the data in the curNode
            return  
        if self.depth < at_depth and self.depth != -1:
            curNode.data = data
            return
        # checking to see if there are no more to split
        if len(data) == 1 or len(data) == 0:
            curNode.data = data
            return
        
        # below here still building the tree
        
        # will get the median of the data from the dimension --- this returning data sorted
        median_number ,median, data = self.__get_median(data, axis=axis) # axis minus 1 is to have the correct element
        
        # getting the new axis to which do the partitioning
        axis = self.__get_new_axis(axis)

        # getting the nodes that will be passed in
        curNode.left = Node(median=median, greater_lesser="l", median_number=median_number)
        curNode.right = Node(median=median, greater_lesser="g", median_number=median_number)
        # doing the split of the data along the median.
        # left side
        self.__build(data[:median], at_depth=at_depth + 1, axis=axis, curNode=curNode.left)
        # right side
        # the median will go to the right side
        self.__build(data[median:], at_depth=at_depth+1, axis=axis, curNode=curNode.right) # from the median to the end
        



    def __sort(self, data, axis):
        
        # adding a list of the axis -- may not need to do this later on
        self.__dimen.append(axis)

        data.sort(key=lambda dataPoint: dataPoint[axis])
        return data



    def __get_new_axis(self, current_axis):
        # looking at what the axis is and will then return the one 
        # that will be the next in line
        if current_axis < self.num_of_axis -1:
            # if in here we can just increment the current_axis
            return current_axis + 1
        else:
            current_axis = 0



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

        data = self.__sort(data, axis=axis)

        
        # now will find the median
        median_index = len(data) // 2
        # getting the median number
        median_number = data[median_index][axis]
        
        # returning both the data and the median
        return median_number, median_index, data



    # def __build_tree(self, data, curDepth, theNode):
    #     # This will be the recursive function that will 
    #     # build the tree
    #     # building will occur until there are 20 point or the 
    #     # depth is reached
    #     if len(theNode.data) > 


    # doing the searching for the new tree
    # doing the printing of the tree
    def print_tree(self):
        # will be doing a dfs for the printing of the tree
        self.__depth_traversal_print(self.head)

    def __depth_traversal_print(self, curNode):
        # doing the return cases first
        if curNode == None:
            return
        # doing the recursive portion of the method
        # will check to see if this node holds leaves
        # if it does will print all the leaves in the node
        if curNode.data != None:
            print(*curNode.data)
            return
        breakpoint()
        # printing the cuts that have happened
        print(f"The cut was done at {curNode.median_number} ")

        # going to the left and then going to the right branch
        self.__depth_traversal_print(curNode=curNode.left)
        self.__depth_traversal_print(curNode=curNode.right)






if __name__ == "__main__":
    # making a data point
    data = [[3,4,5], [12, 22, 11], [33, 3, 7], [1,34, 12], [6, 4,8], [22, 18, 16]]
    # trying to build the tree
    tree = KD_tree(data= data, )

    # doing the printing of the tree that has been build
    tree.print_tree()