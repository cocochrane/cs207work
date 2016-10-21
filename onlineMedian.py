from operator import gt, lt

class BinaryHeap:
    """
    Binary Heap implementation
    
    Examples:
    
    >>> data = [1,8,5,-5]
    >>> min_heap = BinaryHeap.heapify_slow(data,lt)
    >>> min_heap.storage
    [None, -5, 1, 5, 8]
    >>> max_heap = BinaryHeap.heapify_slow(data,gt)
    >>> max_heap.storage
    [None, 8, 1, 5, -5]
    >>> max_heap.insert(12)
    >>> max_heap.storage
    [None, 12, 8, 5, -5, 1]
    >>> print(max_heap.dominant())
    12
    >>> max_heap.del_dominant()
    12
    >>> max_heap.storage
    [None, 8, 1, 5, -5]
    
    
    """
    def __init__(self):
        self.storage=[None]
        self.upto=0
        self.comp_op = None
        
    @classmethod
    def heapify_slow(cls, it, compare_op):
        """Method to create heap out of data and comparison operator
        
        it: data used to populate heap
        compare_op: binary operation used to produce heap
        """
        inst = cls()
        inst.comp_op = compare_op
        for i in it:
            inst.insert(i)
        return inst
            
    def insert(self, value):
        """Method to insert given value into heap
        
        value: value to add into heap
        """
        self.storage.append(value)
        self.upto += 1
        self.sift_up(self.upto)

    def sift_up(self, i):
        """Helper function for insert method 
        
        i: index of current node 
        """
        parent = i // 2
        if parent > 0 and self.comp_op(self.storage[i],self.storage[parent]):
            self.storage[i], self.storage[parent] = self.storage[parent], self.storage[i]
            self.sift_up(parent)
     
    def _min_child(self, i):
        """Helper function for sift_down functon
        
        i: index of current node 
        """
        if 2*i + 1 > self.upto:
            return 2*i
        else:
            if self.comp_op(self.storage[2*i], self.storage[2*i+1]):
                return 2*i
            return 2*i + 1
    
    def sift_down(self, i):
        """Helper function for del_dominant
        Sifts values down the heap
        
        i: index of current node 
        """
        if 2*i <= self.upto:
            child = self._min_child(i)
            if not self.comp_op(self.storage[i],self.storage[child]):
                self.storage[child], self.storage[i] = self.storage[i], self.storage[child]
                self.sift_down(child)
        
    def dominant(self):
        """Method to find dominant element in heap-
        dominant is the largest in a max heap and smallest
        in a min heap
        """
        return self.storage[1]
    
    def del_dominant(self):
        """Method to delete dominant element in heap-
        dominant is the largest in a max heap and smallest
        in a min heap
        """
        dom_val = self.storage[1]
        self.storage[1], self.storage[self.upto] = self.storage[self.upto], self.storage[1]
        self.storage.pop()
        self.upto -= 1
        self.sift_down(1)
        return dom_val


def online_median(iterator):
    """ Function that finds online median
    
    iterator: type=iterator, data that our median
    will be determined from
    >>> import random
    >>> import numpy as np
    >>> l = [i**2 for i in range(150)]
    >>> medians = list(online_median(iter(l)))
    >>> medians[-1]
    5550.5
    """
    min_heap = BinaryHeap.heapify_slow([], lt)
    max_heap = BinaryHeap.heapify_slow([], gt)
    
    for i in iterator:
        if max_heap.upto == 0 or i < max_heap.dominant():
            max_heap.insert(i)
        else:
            min_heap.insert(i)
            
        if min_heap.upto > max_heap.upto + 1:
            max_heap.insert(min_heap.del_dominant())
        elif max_heap.upto > min_heap.upto + 1:
            min_heap.insert(max_heap.del_dominant())
            
        if min_heap.upto == max_heap.upto: # if same size
            yield (min_heap.dominant() + max_heap.dominant())/2.0
        elif min_heap.upto > max_heap.upto:
            yield min_heap.dominant()
        else:
            yield max_heap.dominant()