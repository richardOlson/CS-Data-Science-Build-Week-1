# my implementation of the kd_tree
# This implimentation needs to be python 3.8 or greater

# doing an import of a queue
from queue import Queue
from numpy import linalg
from math import dist
import numpy as np

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
        if not isinstance(data, (list, np.ndarray)):
            raise Exception("Data is not in correct format, must be a list or list of lists")

        
        self.head = Node() # making the first Node as the head

        # This is making the data attribute that will hold the data
        # when keep_original index == True
        #self.data = None 
        
        # Creating depth attribute for the class
        self.depth = depth

        # Finding the number axis to which cut the data
        self.num_of_axis = len(data[0])

        # getting the attribute for the axis
        self.axis = 0

        
        # Data index is the index of the list or the array it is what is sorted and changed
        # the numpy array or the list is not changed
        self.data_index = [None] * len(data)
        self.__make_data_index(data)

        # making the attribute that will hold the data
        self.data = data

        if max_leaf_nodes == None:
            self.max_leaf_nodes = -1
        else:
            self.max_leaf_nodes = max_leaf_nodes

        self.keep_original_index = keep_original_index

        #self.max_leaf_nodes = max_leaf_nodes
        # building the tree with making the nodes
        self.__build(self.data_index, at_depth=0, axis=0, curNode=self.head)

        

    def __build(self, data_indices, at_depth, axis, curNode):
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
        if self.max_leaf_nodes >= len(data_indices) and self.max_leaf_nodes != -1:
            # THESE DATA IN THE CUR NODE ARE JUST THE INDEXES TO WHERE THE 
            # DATA IS FOUND IN THE SELF.DATA 
            # will need to add the data to the current node and then return
            curNode.data = data_indices # this is a list of the data in the curNode
            return  
        if self.depth < at_depth and self.depth != -1:
            curNode.data = data_indices
            return
        # checking to see if there are no more to split
        if len(data_indices) == 1 or len(data_indices) == 0:
            curNode.data = data_indices
            return
        
        # below here still building the tree
        
        # will get the median of the data from the dimension --- this returning data sorted
        median_number ,median, data_indices = self.__get_median(data_indices, axis=axis) 
        
        # getting the nodes that will be passed in and the current Node set up. 
        curNode.median_number = median_number
        curNode.median_point = median # this is the median index -- probably don't need this
        curNode.axis_cut = axis
        
        # creating the two new nodes
        curNode.left = Node(side_of_cut="l", parent=curNode)
        curNode.right = Node(side_of_cut="r", parent=curNode)

        # getting the new axis to which do the partitioning
        axis = self.__get_new_axis(axis)
        self.axis = axis

        if self.axis == None:
            print("axis is none")
            breakpoint()
        # doing the split of the data along the median.
        # left side
        self.__build(data_indices[:median], at_depth=at_depth + 1, axis=axis, curNode=curNode.left)
        # right side
        # the median will go to the right side
        self.__build(data_indices[median:], at_depth=at_depth+1, axis=axis, curNode=curNode.right) # from the median to the end
        


    def __get_data(self, data_indices):
        """
        This is the function that will get the data and return it.
        This function is passed in a list of data indexes that can be used to find the correct elements
        in the self.data which is either a numpy array or a list
        """
        d_list = []
        for the_index in data_indices:
            d_list.append(self.data[the_index])
        return d_list


    def __make_data_index(self, data):
        """
        This is the function that will make the tuple of the data.
        """
        
        # doing a loop of the data and makin the tuple
        for i in range(len(data)):
            self.data_index[i] = i
        
      

    # This is the funtion that will return the value that needs to be found to do the sorting
    # This function was buit because we were dealing with an error of 
    # "The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()"
    # without using this function
    def t_key(self,iterable):
        
        val = None
        if isinstance(self.data, np.ndarray):
            if self.num_of_axis == 1:
                val = self.data.item(iterable)
            else:
                val = self.data.item((iterable, self.axis))
        else:
            if self.axis == None:
                print("It is none")
                breakpoint()
            if self.num_of_axis == 1:
                # the iterable is the data_index to retieve the data
                val = self.data[iterable]
            else:
                val = self.data[iterable][self.axis]
        
        return val


    def __sort(self, data_indices, axis):
        
        # # making it so that it can use the tuples if necesary to keep the original index
        # if self.keep_original_index:
        #     if self.num_of_axis == 1:
        #         data.sort(key=lambda dataPoint: dataPoint[1])
        #     else:
        #         data.sort(key=lambda dataPoint: dataPoint[1][axis])
        # elif self.num_of_axis ==1:
        #     data.sort(key=lambda dataPoint: dataPoint)
        # else:
        #     data.sort(key=lambda dataPoint: dataPoint[axis])
        # return data
        # sorting just the data index and leaving the original data alone
        data_indices.sort(key=self.t_key)
        return data_indices


    def __get_new_axis(self, current_axis):
        # looking at what the axis is and will then return the one 
        # that will be the next in line
        if current_axis < self.num_of_axis -1:
            # if in here we can just increment the current_axis
            return current_axis + 1
        else:
            current_axis = 0
        return current_axis



    def __get_median(self, data_indices, axis):
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
        

        data_indices = self.__sort(data_indices, axis=axis)


        # This is the median element in the data_indices -- so if there 7 elements this is the 4th element
        # now will find the median
        data_median_index = len(data_indices)//2
        # getting the element that will be used to look up the data value in the nd array or the list
        med = data_indices[data_median_index]
       

        # getting the median number -- from the nd array or the list of values (points)
        if self.num_of_axis == 1: # that means that is one dimensional, just numbers
            median_number = self.data[med]
        
        else:                    
            median_number = self.data[med][axis]

        # checking what the number below the median if it is the same then we will need to 
        # move the median index down.
        # This is to keep all the points that have the same number on the same side.
        # We will move the index down unless we are at index 0 becuase it can't move any further.
        median_index = self.__move_if_need_median_index(median_number=median_number, 
                                                        median_index=data_median_index, data_indices=data_indices, axis=axis)
        
        # returning both the data and the median
        return median_number, median_index, data_indices




    def __move_if_need_median_index(self, median_number, median_index, data_indices, axis):
        """
        This is the method that will move the index if it is needed to try to make sure that all the numbers
        that are the same remain on the same side.
        """
        # median_index is the element number for the data_indices list
        while True:
            if median_index == 0:
                return median_index
            
            if self.data[data_indices[median_index - 1]][axis] != median_number:
                return median_index
            
            # shifting down to next element
            median_index = median_index -1



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
                print(f"At this Node are the leaves (data-points) found -- {self.__get_val(curNode.data)}")
            
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
    def find_kd_tree_neighbors(self, eps, point, curNode=None):
        """
        This is the base function that will be used to search through the kd_tree to find the 
        neighbors of the point that is passed into this function.

        eps:  This is the value or distance that another point must be equal to or under to 
        be considered a neighbor.

        point:  This is the point that is used to look for its neighbors
        
        Returns:  This function will return a list of all the neighbors of the point that is passed in.
        If "keep_original_index == True" then the list of neighbors will be the indexes of the neighbors
            
        """

        # Will first need to traverse the tree. -- will do a breath type of traversal
        # If one branch is good to go down then it will be added to the queue, if is not good to 
        # traverse through then the branch will not be added to the queue.

        # doing a depth type of search
        if curNode == None:
            curNode = self.head
        
        # doing the checks to when we want to return 

        # have reached the data that are neighbors
        # Here will either store the index of the neigbors or will store the neighbors
        if curNode.data is not None:
            
            some_neighbors = self.__check_data_points_for_neighbors(eps=eps, curNode=curNode, point=point)
            return some_neighbors

        # need to choose the direction to go to look
        # getting the edge of the radius
        point_number = point[curNode.axis_cut]
        number_above_eps = point_number + eps
        number_below_eps = point_number - eps

        # This is for sure should continue in the left side
        # need to check if should go down the right side also
        if point_number < curNode.median_number:
            rightList = [] # getting it so that it can be added to the left list

            # Goint down the left side
            leftList = self.find_kd_tree_neighbors(eps=eps, point=point, curNode=curNode.left)

            # checking the right side
            if number_above_eps > curNode.median_number:
                # going down the right side also
                rightList = self.find_kd_tree_neighbors(eps=eps, point=point, curNode=curNode.right)   
            # joining the lists
            neighbors = leftList + rightList
            return neighbors
        # In here means that the point number is on the right side
        else:
            rightList = []
            leftList = []
            # checking if want to use the left side along with the right side
            if number_below_eps < curNode.median_number:
                # if in here will be going down the left side also
                leftList = self.find_kd_tree_neighbors(eps=eps, point=point, curNode=curNode.left)
            
            # going down the right side
            rightList = self.find_kd_tree_neighbors(eps=eps, point=point, curNode=curNode.right)

            neighbors = leftList + rightList
            return neighbors

        
    def __get_val(self, data_index):
        if not isinstance(data_index, list):
            return self.data[data_index]
        else:
            theList = []

            for d in data_index:
                theList.append(self.data[d])
            return theList
        
        
        

        


    # This is the function that will check to see if any of the points are neighbors.
    # This is function will grab either the indices or the data depending on flag
    # of keep_original_index
    def __check_data_points_for_neighbors(self, eps, curNode, point):
        neighbor_list = []
        # making it so that if the values are in a list that it will be able to find the 
        # distance
        the_dist = None
        
        for n_pt in curNode.data:
            # getting a data point 
            data_point = self.data[n_pt]
            # checking the instance of the data if it is a instance then the dist will be used
            if isinstance(data_point, list):
                the_dist = dist(point, data_point)
            else:# this one is for the numpy array
                # using the linagl_norm to find the distance
                the_dist = linalg.norm(point - data_point)
            
            if the_dist <= eps:
                # adding the data points that are neighbors this will just be the element 
                # number of the data
                neighbor_list.append(n_pt)
        
        # returning the neigborlist
        return neighbor_list





if __name__ == "__main__":
    # making a data point
    d = [[3,4,5], [12, 22, 11], [33, 3, 7], [1,34, 12], [6, 85,8], [22, 18, 16]]
    # trying to build the tree
    tree = KD_tree(data= d,)

    # doing the printing of the tree that has been build
    tree.print_tree()

    print("Now doing the breadth print of the tree\n")
    # now doing the breath traversal print
    tree.print_breadth()

    new_data = [(0,[3,4,5]), (1,[12, 22, 11]), (2,[33, 3, 7]), (3,[1,34, 12]), (4,[6, 4,8]), (5,[22, 18, 16])]

    # Trying to find the neighbors of the point that will be passed int
    theList = tree.find_kd_tree_neighbors(eps=9, point=[5, 7, 8], curNode=tree.head)

    print(f"The neighbors for the point [5,7,8] is {theList}")

    print("The following is a loop that will loop through and will show what the distance")
    print("is for each of the following points in the data with respect to the point")

    for each_point in d:
        print(f"The distance for {each_point} and [5,7,8] is {dist(each_point, [5,7,8])}")

    