# my implementation of the kd_tree
# This implimentation needs to be python 3.8 or greater

# doing an import of a queue
from queue import Queue, SimpleQueue
from numpy import linalg
from math import dist
import numpy as np
from collections import deque
from sklearn.datasets import make_blobs


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

        # making the attribute that will hold the data (the numpy array or the list)
        self.data = data

        if max_leaf_nodes == None:
            self.max_leaf_nodes = -1
        else:
            self.max_leaf_nodes = max_leaf_nodes

        
        # This is to check what the previous index was
        self.the_prev_index=None
        
        # building the tree with making the nodes
        self.__build(self.data_index, at_depth=0,  curNode=self.head)
        
        

        

    def __build(self, data_indices, at_depth, curNode):
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
        the_axis = None # this is to check the axis in the check_cut if necessary
        # will get the median of the data from the dimension --- this returning data sorted
        median_number ,median, data_indices = self.__get_median(data_indices)

        # need to check if the data_indices and the cut at the median is the same.
        # If they are then we need to check the rest of the directions axis.  If they end up being the same
        # we will then do the loop through the rest of the axis and if they remain the same then
        # the data_indices are all stored as data.
        if len(data_indices[median:]) == len(self.the_prev_index):
            med_num, med, d_ind = self.__check_cut(data_indices=data_indices, 
                                                                curNode=curNode)

            if d_ind == None:
                # if in here then we need to put all the data_indices into data
                # and then return because was unable to cut the data
                curNode.data = data_indices
                return
            else:
                median_number = med_num
                median = med
                data_indices = d_ind
                

        
        # getting the nodes that will be passed in and the current Node set up. 
        curNode.median_number = median_number
        curNode.median_point = median # this is the median index -- probably don't need this
        curNode.axis_cut = self.axis
        
        # creating the two new nodes
        curNode.left = Node(side_of_cut="l", parent=curNode)
        curNode.right = Node(side_of_cut="r", parent=curNode)

        # getting the new axis to which do the partitioning
        self.__get_new_axis(change_att=True)
        

        
        # doing the split of the data along the median.
        # left side
        # making sure the left side is not empty
        if len(data_indices[:median]) >= 1:
            self.__build(data_indices[:median], at_depth=at_depth + 1,curNode=curNode.left)
        
        # right side
        # the median will go to the right side
        self.__build(data_indices[median:], at_depth=at_depth+1, curNode=curNode.right) # from the median to the end
        


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
        
        # doing a loop of the data
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
           
            if self.num_of_axis == 1:
                # the iterable is the data_index to retieve the data
                val = self.data[iterable]
            else:
                val = self.data[iterable][self.axis]
        
        return val
        


    def __check_cut(self, data_indices, curNode):
        """
        This is the function that will check what to do if the same 
        data indices comes back twice.  This will mean that one of the axis did not 
        cut the data. The other axises will be checked until exhausted.  If finding an
        axis to cut, this function will return all the needed info to do the cut.
        If no cut was available, this function will signal wether to put the data on the current node
        or tell which axis to cut on. 
        """
        # setting the current axis
        axis = self.axis
        # setting the current indices
        curIndices = data_indices
        
        # doing a while loop
        # dong a sort of the data
        while True:
            the_cur_axis = self.__get_new_axis(change_att=True)
            median_number, median, data_indices = self.__get_median(data_indices=data_indices)
            if len(data_indices[median:]) != len(data_indices):
                # if in here then it can be cut along this axis
                return median_number, median, data_indices
            if axis == the_cur_axis:
                return None, None, None,
        
        
        

    def __sort(self, data_indices):

        
        # This is setting the prev indices to see if it is the same as the
        # the previous time.  This will alert the system to check other axis and then decide if 
        # it will all become leaves because it can't be split.
        # This is done before doing the splitting of the data
        self.the_prev_index = data_indices
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
        # print(f"Printing the indices of the sort and the values on the axis -- {self.axis}")
        # for d in data_indices:
        #     print(f"index {d} -- value {self.__get_val(d)}")
        # print()
        return data_indices


    def __get_new_axis(self,  change_att=True):
        # looking at what the axis is and will then return the one 
        # that will be the next in line
        current_axis = self.axis
        if current_axis < self.num_of_axis -1:
            # if in here we can just increment the current_axis
            current_axis = current_axis + 1 
        else:
            current_axis = 0
        if change_att == True:
            self.axis = current_axis
        return current_axis



    def __get_median(self, data_indices):
        """
        This function will return the median of the data on the axis 
        that is specified.  If the axis specified doesn't exist, this 
        function will throw an error stating the axis doesn't exist.

        data:  the data to be split. This must be a list of lists

        
        """
        # first need to call the sorting function along the axis
        # to be split and then will get the median and return it and
        # also the data that has been sorted
        
        
        data_indices = self.__sort(data_indices)


        # This is the median element in the data_indices -- so if there 7 elements this is the 4th element
        # now will find the median
        data_median_index = len(data_indices)//2
        # getting the element that will be used to look up the data value in the nd array or the list
        med = data_indices[data_median_index]
       

        # getting the median number -- from the nd array or the list of values (points)
        if self.num_of_axis == 1: # that means that is one dimensional, just numbers
            if isinstance(self.data, np.ndarray):
                median_number = self.data.item(med)
            else:
                median_number = self.data[med]
        
        else:                    
            if isinstance(self.data, np.ndarray):
                median_number = self.data.item((med, self.axis))

            else:
                median_number = self.data[med][self.axis]
        
        # checking what the number below the median if it is the same then we will need to 
        # move the median index down.
        # This is to keep all the points that have the same number on the same side.
        # We will move the index down unless we are at index 0 becuase it can't move any further.
        median_index = self.__move_if_need_median_index(median_number=median_number, 
                                                        median_index=data_median_index, data_indices=data_indices)
        
        # print(f"This is the median number -- {median_number} and the median index --- {median_index}, axis-- {self.axis}")
        # print("\n\n")
        # returning both the data and the median
        return median_number, median_index, data_indices




    def __move_if_need_median_index(self, median_number, median_index, data_indices):
        """
        This is the method that will move the index if it is needed to try to make sure that all the numbers
        that are the same remain on the same side.
        """
        # median_index is the element number for the data_indices list
        while True:
            if median_index == 0:
                return median_index
            
            if self.data[data_indices[median_index - 1]][self.axis] != median_number:
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
    def find_kd_tree_neighbors(self, eps, point, point_index=None, curNode=None, return_data=False):
        """
        This is the base function that will be used to search through the kd_tree to find the 
        neighbors of the point that is passed into this function.

        eps:  This is the value or distance that another point must be equal to or under to 
        be considered a neighbor.

        point:  This is the point that is used to look for its neighbors

        point_index:  When this is added then the function will make sure to not return itself as a neighbor
        It will return all neigbors who are at the index specified.
        
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
            
            some_neighbors = self.__check_data_points_for_neighbors(eps=eps, curNode=curNode, point=point,
                                                         point_index=point_index, return_data=return_data)
            return some_neighbors
        
        
        # need to choose the direction to go to look
        # getting the edge of the radius
        point_number = point[curNode.axis_cut]
        number_above_eps = point_number + eps
        number_below_eps = point_number - eps
        
        # if point[0] > 5.38 and point[0] < 5.40 and point[1] > 1.5 and point[1] < 1.55:
        #     breakpoint()
        # # This is for sure should continue in the left side
        # need to check if should go down the right side also
        if point_number < curNode.median_number:
            rightList = [] # getting it so that it can be added to the left list

            # Goint down the left side
            leftList = self.find_kd_tree_neighbors(eps=eps, point=point, point_index=point_index, 
                                                        curNode=curNode.left, return_data=return_data)

            # checking the right side
            if number_above_eps >= curNode.median_number:
                # going down the right side also
                rightList = self.find_kd_tree_neighbors(eps=eps, point=point, point_index=point_index, curNode=curNode.right,
                                                        return_data=return_data)   
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
                leftList = self.find_kd_tree_neighbors(eps=eps, point=point, point_index=point_index, curNode=curNode.left,
                                                        return_data=return_data)
            
            # going down the right side
            rightList = self.find_kd_tree_neighbors(eps=eps, point=point, point_index=point_index, curNode=curNode.right,
                                                    return_data=return_data)

            neighbors = leftList + rightList
            return neighbors

        
    def __get_val(self, data_index, np_to_scalar=False):
        """
        data_index are the indexes that you want to get the values for
        """

        if not isinstance(data_index, list):
            return self.data[data_index]
        else:
            theList = []

            for d in data_index:
                if np_to_scalar == True and isinstance(self.data, np.ndarray):
                    # this is used when want numpy array as just a list
                    np_scalar = self.data.item(d)

                theList.append(self.data[d])
            return theList
        
        
        

    def get_val(self, data_index):
        return self.__get_val(data_index)


    # This is the function that will check to see if any of the points are neighbors.
    # This is function will grab either the indices or the data depending on flag
    # of keep_original_index
    def __check_data_points_for_neighbors(self, eps, curNode, point,  point_index, return_data=False):
        neighbor_list = []
        # making it so that if the values are in a list that it will be able to find the 
        # distance

        # If print return_data == True, then will return the data instead of the indexes
        the_dist = None
        if point_index == None:
            point_index = -1
        for n_pt in curNode.data:
            if point_index == n_pt:
                continue
            else:        
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
        if return_data:
            return self.__get_val(neighbor_list)
        # returning the neigborlist
        return neighbor_list


    def get_cuts_for_val_index(self, val=None, index=None):
        """
        This function will search throught the tree and will return the cuts on which axis and also where the 
        median was for the cuts to reach the number reqested. Can enter
        in a value or the index.
        """
        the_queue = deque()
        # setting up the inner function
        val = self.__inner_get_cuts_val(curNode=self.head, val=val, index=index, the_queue=the_queue)

        if val == 1:
            # need to print the cuts for the tree
            # doing a loop through the queue
            while the_queue:
                
                val = the_queue.popleft()
                # checking what the value is
                # curNode.median_number, curNode.median, curNode.axis_cut, curNode.side_of_cut
                if  len(val) == 4:
                    print(f"The cut was done on the {val[2]} axis.")
                    print(f"The median index was -- {val[1]}")
                    print(f"The median number was -- {val[0]}\n")

                # curNode.data, curNode.side_of_cut
                else:
                    print(f"The following data is on the {val[1]}")
                    print(f"The following are the indexes and the values:")
                    for index in val[0]:
                        print(f"The index --- {index} and the value --- {self.__get_val(index)}\n")



    def __inner_get_cuts_val(self, curNode, val, index, the_queue):
        
        if curNode.data != None:
            # if val != None:
            #     theList = self.__get_val(curNode.data, np_to_scalar=True)
            #     if val in theList:
            #         the_queue.appendleft((theList, curNode.side_of_cut))
            #         return 1
            #     else:
            #         return 0
            
            if index in  curNode.data:
                the_queue.appendleft((curNode.data, curNode.side_of_cut))
                return 1
            else:
                return 0
        if curNode == None:
            return 0
        # doing the recursive part of the function
        val = self.__inner_get_cuts_val(curNode.left, val=val, index=index, the_queue=the_queue)
        if val == 0:
            
            # now trying the right side of the tree
            val = self.__inner_get_cuts_val(curNode.right, val=val, index=index, the_queue=the_queue)

            if val == 0:
                
                return 0
            else:
                the_queue.appendleft((curNode.median_number, curNode.median_point, curNode.axis_cut, curNode.side_of_cut))
                return 1
        else:
            the_queue.appendleft((curNode.median_number, curNode.median_point, curNode.axis_cut, curNode.side_of_cut))
            return 1


if __name__ == "__main__":
    # making a data point
    #d = [[3,4,5], [12, 22, 11], [33, 3, 7], [1,34, 12], [6, 85,8], [22, 18, 16]]
    # d = [
    #     [2,3], [4,5], [2,6], [2,1], [10, 1], [4,8], [12, 2], [1,1], [1,2],
    #     [5,5], [12, 4], [8,0], [13, 7], [23, 4], [7,3], [12,12], [10, 9],
    #     [15,4], [2,16], [2,10], [9, 15], [13, 13], [17, 9], [20, 2], [34, 5],
    #     [18, 5], [2, 17], [25, 5], [16, 16], [28, 5], [9, 16], [4, 10]
    # ]

    # # converting to a numpy array
    # d = np.array(d)

    # making a blob
    d, y = make_blobs(n_samples=45, centers=6, n_features=2, random_state=49)
    
    # trying to build the tree
    tree = KD_tree(data= d,max_leaf_nodes=15)

    # doing the printing of the tree that has been build
    #tree.print_tree()

    #print("Now doing the breadth print of the tree\n")
    # now doing the breath traversal print
    #tree.print_breadth()

    # now trying to do the finding of neighbors
    
    # for i, point in enumerate(d):
        
    #     print(f"For the point {point}, the neighbors with dist of 3 are:")
    #     neighbors = tree.find_kd_tree_neighbors(eps=1.1, point=point, point_index=i, return_data=True)
    #     print(*neighbors)



    tree.get_cuts_for_val_index(index=31)

    n = tree.find_kd_tree_neighbors(eps=1.1, point=tree.data[31], point_index=31, )

    print(f"The neighbors are {n}")

    print(*tree.get_val(n))

    #new_data = [(0,[3,4,5]), (1,[12, 22, 11]), (2,[33, 3, 7]), (3,[1,34, 12]), (4,[6, 4,8]), (5,[22, 18, 16])]

    # Trying to find the neighbors of the point that will be passed int
    #theList = tree.find_kd_tree_neighbors(eps=9, point=[5, 7, 8], curNode=tree.head)

    # print(f"The neighbors for the point [5,7,8] is {theList}")

    # print("The following is a loop that will loop through and will show what the distance")
    # print("is for each of the following points in the data with respect to the point")

    # for each_point in d:
    #     print(f"The distance for {each_point} and [5,7,8] is {dist(each_point, [5,7,8])}")
    # breakpoint()
    # for point in d:
    #     # finding all the neighbors of each other
    #     neighbors = tree.find_kd_tree_neighbors(eps=5, point=point, return_data=True)
        

    #     print(f"This is all the neighbors for the point {point}, \n {neigbors}")

