# my implementation of the kd_tree

# doing an import of a queue
from queue import Queue

class Node:
    def __init__(self, data=None, median=None, median_number=None, side_of_cut=None, parent=None):
        self.data = data
        # The right or left is how the connection from one Node to the next node on the right or left will connect.
        # The parent is the connection to the Node that is the parent to this Node if there is one
        # If there is no parent, then will be left as None.
        self.right = None
        self.left = None
        self.parent = parent
        # The side_of_cut is to tell you which side of the cut the the node above this one does this 
        # Node lay.  If there is no Node above then will remain as None
        self.side_of_cut = side_of_cut # This is to tell if this node is a right or left node (which side of the median)
        self.median_point = median
        self.median_number = median_number
        # The axis cut will be an integer ie: 0, 1, 2.  The 0 means the first axis in the data, 1-- the second ect.
        self.axis_cut = None 


class KD_tree:
    """
    data: the data that will be passed in
    depth:  this is how much that the data will be broken down
    When the depth is left as -1, then it will go completely to just one leaf on the last node

    

    max_leaf_nodes: If the number of leaves is equal to or less than max_leaf_nodes then the building of 
    the tree will stop
    """
    def __init__(self, data, depth=-1, max_leaf_nodes=None, keep_original_index=True):

        """
        keep_original_index: when this flag is set to true then the data which is a list of data points is
        changed to a list of tuples where the first index of the tuple is the original elment index and 
        the second element is the data point.  This makes it so that when sorting occurs you can still have
        knowlege of the original element index if desired

        """

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

        self.keep_original_index = keep_original_index

        if self.keep_original_index:
            # This is the fucnction that will make the tuple that 
            # where the first element in the tuple will contain the original index of all the data
            data = self.__make_tup(data)
       

        #self.max_leaf_nodes = max_leaf_nodes
        # building the tree with making the nodes
        self.__build(data, at_depth=0, axis=0, curNode=self.head)
    


    def __build(self, data, at_depth, axis, curNode):
        """
        This is the method that will build the 
        tree.  This function  is recursive and will continue to be called
        while building the tree.

        When preparing the tree it will do a loop first which will put the data in a 
        list of tuples where the first element is n the tuple is the original index 
        of the data.  This is so that when using the DBSCAN it can use the methods that
        have beeen implemented, which use the data indexes.
        
        data:  the data that is to be split and put into nodes.  The data is made so that 
        it comes in as a l

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
        
        # getting the nodes that will be passed in and the current Node set up. 
        curNode.median_number = median_number
        curNode.median_point = median
        curNode.axis_cut = axis
        
        # creating the two new nodes
        curNode.left = Node(side_of_cut="l", parent=curNode)
        curNode.right = Node(side_of_cut="r", parent=curNode)

        # getting the new axis to which do the partitioning
        axis = self.__get_new_axis(axis)

        # doing the split of the data along the median.
        # left side
        self.__build(data[:median], at_depth=at_depth + 1, axis=axis, curNode=curNode.left)
        # right side
        # the median will go to the right side
        self.__build(data[median:], at_depth=at_depth+1, axis=axis, curNode=curNode.right) # from the median to the end
        



    def __make_tup(self, data):
        """
        This is the function that will make the tuple of the data.
        """
        # doing a loop of the data and makin the tuple
        for i in range(len(data)):
            data[i] = (i, data[i])
        
        return data


    def __sort(self, data, axis):
        
        # adding a list of the axis -- may not need to do this later on
        self.__dimen.append(axis)

        # making it so that it can use the tuples if necesary to keep the original index
        if self.keep_original_index:
            if self.num_of_axis == 1:
                data.sort(key=lambda dataPoint: dataPoint[1])
            else:
                data.sort(key=lambda dataPoint: dataPoint[1][axis])
        elif self.num_of_axis ==1:
            data.sort(key=lambda dataPoint: dataPoint)
        else:
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
       
        # making it so that if there is a tuple that it can be used
        if self.keep_original_index:

            if self.num_of_axis == 1: # that means that is one dimensional, just numbes
                median_number = data[median_index][1]
            
            else:                    
                median_number = data[median_index][1][axis]

        elif self.num_of_axis == 1: # checking how many dimensions, if true is just a scalar
            median_number = data[median_index]

        else:
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
        
        # printing the cuts that have happened
        print(f"The cut was done at {curNode.median_number} ")

        # going to the left and then going to the right branch
        self.__depth_traversal_print(curNode=curNode.left)
        self.__depth_traversal_print(curNode=curNode.right)


    def print_breadth(self):
        self.__breadth_traversal_print(curNode=self.head)
    
    def __breadth_traversal_print(self, curNode):

        """
        To start this function the curNode must have the head node passed into it.
        
        """
            
        # making the queue and then putting something into the queue   
        the_queue = Queue()
        # will be putting in the curNode into the queue
        # so that the function will work further down the line
        the_queue.put(curNode)

        while the_queue.empty() == False:
            # will go through the function and use the queue
            # dequeing 
            curNode = the_queue.get()
            
            # building the print list
            if curNode.axis_cut != None:
                # willl print that a cut has been done
                print(f"A cut was performed at this node on the number {curNode.median_number} on the axis of {curNode.axis_cut}")
            if curNode.data != None:
                # printing out the data that is at the node here -- these are the leaves
                print(f"At this Node are the leaves (data-points) found -- {curNode.data}")
            
            # checking to see if the chile Nodes are empty and if they are not then they will be added
            if curNode.left is not None:
                the_queue.put(curNode.left)
            if curNode.right is not None:
                the_queue.put(curNode.right)

    
    # below is the building of the function that will do the searching in the kd_tree
    # this function will have passed in the eps parameter from the DBSCAN function.
    # The function below will make it so that it doesn't hopefully need to look at
    # all of the points to find another points neighbors becuase the data will be partitioned in 
    # the tree.
    def find_kd_tree_neighbors(self, eps, point, curNode=None, neighbors=[]):
        """
        This is the base function that will be used to search through the kd_tree to find the 
        neighbors of the point that is passed into this function.

        eps:  This is the value or distance that another point must be equal to or under to 
        be considered a neighbor.

        point:  This is the point that is used to look for its neighbors
        
        Returns:  This function will return a list of all the neighbors of the point that is passed in.
            
        """

        # Will first need to traverse the tree. -- will do a breath type of traversal
        # If one branch is good to go down then it will be added to the queue, if is not good to 
        # traverse through then the branch will not be added to the queue.

        # doing a depth type of search
        if curNode == None:
            curNode = self.head
        
        # doing the checks to when we want to return 

        # have reached the data that are neighbors
        if curNode.data is not None:
            neighbors.append(curNode.data)
            return 
        


        







if __name__ == "__main__":
    # making a data point
    data = [[3,4,5], [12, 22, 11], [33, 3, 7], [1,34, 12], [6, 4,8], [22, 18, 16]]
    # trying to build the tree
    tree = KD_tree(data= data, keep_original_index=False)

    # doing the printing of the tree that has been build
    tree.print_tree()

    print("Now doing the breadth print of the tree\n")
    # now doing the breath traversal print
    tree.print_breadth()