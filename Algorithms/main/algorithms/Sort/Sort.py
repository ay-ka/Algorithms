import numpy
import math
import pdb
from abc import ABC, abstractmethod
from collections import Counter
import argparse

class Sort(ABC):
    
    def __init__(self):
        
        pass
        
    @abstractmethod    
    def doSort(self):
        
        pass
    
class MergeSort(Sort):
    
    def __init__(self):
        
        super(MergeSort, self).__init__()
        
    def doSort(self, data_lst):
        
        length = len(data_lst)
        
        middle_length = math.ceil(length / 2)
        
        if middle_length == 1:
            
            if length == 1:
                
                return data_lst
                
            else:
                
                if data_lst[0] > data_lst[1]:
                    
                    return list(reversed(data_lst))
                    
                else:
                    
                    return data_lst
           
        else:
            
            left_data_lst = data_lst[0: middle_length]
            
            right_data_lst = data_lst[middle_length : ]
            
            sorted_left_part = self.doSort(left_data_lst)
            
            sorted_right_part = self.doSort(right_data_lst)
            
            merged_lst = self.Merge(sorted_left_part, sorted_right_part)
            
            return merged_lst
        
        
            
    def Merge(self, lst_1, lst_2):
        
        lst_length_1, lst_length_2 = len(lst_1), len(lst_2)
            
        lst_1_index, lst_2_index = 0, 0
        
        merged_lst = []
        
        while lst_1_index != lst_length_1 and lst_2_index != lst_length_2:
            
            node_1, node_2 = lst_1[lst_1_index], lst_2[lst_2_index]
            
            if node_1 < node_2:
                
                merged_lst.append(node_1)
                
                lst_1_index += 1
                
            else:
                
                merged_lst.append(node_2)
                
                lst_2_index += 1
                
        if lst_1_index == lst_length_1:
            
            merged_lst.extend(lst_2[lst_2_index : ])
            
        else:
            
            merged_lst.extend(lst_1[lst_1_index : ]) 
            
        return merged_lst
    
    
class QuickSort(Sort):
    
    def __init__(self):
        
        super(QuickSort, self).__init__()
        
    def doSort(self, data_lst):
        
        if len(data_lst) == 0:
            
            return []
        
        pivot = data_lst[-1]
        
        low, high = 0, len(data_lst) - 1
        
        replace_index = 0
        
        for index in range(low, high):
            
            if data_lst[index] < pivot:
                
                passive_var = data_lst[index]
                
                data_lst[index] = data_lst[replace_index]
                
                data_lst[replace_index] = passive_var
                
                replace_index += 1
                
        passive_var = data_lst[replace_index]

        data_lst[replace_index] = data_lst[high]

        data_lst[high] = passive_var
            
        if len(data_lst) == 2:
            
            return data_lst
            
        first_low, first_high = 0, replace_index
        
        second_low, second_high = replace_index + 1, len(data_lst)
            
        sorted_lst_1 = self.doSort(data_lst[first_low : first_high])
        
        sorted_lst_2 = self.doSort(data_lst[second_low : second_high])
        
        sorted_lst_1.extend([pivot])
        
        sorted_lst_1.extend(sorted_lst_2)
        
        goal_lst = sorted_lst_1
        
        return goal_lst


class Heap(Sort):
    
    def __init__(self):
        
        super(Heap, self).__init__()
        
    def doSort(self, data):
        
        sorted_lst = [0 for index in range(len(data))]
        
        for index in range(len(data) - 1, -1, -1 ):
            
            passive = data[0]
            
            data[0] = data[-1]
            
            data.pop()

            sorted_lst[index] = passive
            
            if len(data) == 0:
                
                break
            
            self.heapify(data, index = 0)
            
        return sorted_lst

    
    def createHeap(self, data):
        
        for index in range(len(data) - 1, -1, -1):
            
            self.heapify(data, index)
            
        return data
            
   
    def heapify(self, data, index):
        
        values = []

        parent_node = data[index]
        
        values.append((parent_node, index))
        
        if 2 * index + 1 <= len(data) - 1:
            
            child_1_node = data[2 * index + 1]

            values.append((child_1_node, 2 * index + 1))
            
        if 2 * index + 2 <= len(data) - 1:
            
            child_2_node = data[2 * index + 2]

            values.append((child_2_node, 2 * index + 2))

        largest_node_index = self.update(data, values, index)
        
        if largest_node_index != index:
            
            self.heapify(data, largest_node_index)
            
    def r_heapify(self, data, index):
        
        parent_index, parent_node = math.floor(((index - 1) / 2)), data[math.floor(((index - 1) / 2))]
        
        if parent_node < data[index]:
            
            self.replace(data, parent_index, index)
            
            index = parent_index
            
            self.r_heapify(data, index)
        
    def replace(self, data, index_1, index_2):
        
        passive = data[index_1]
        
        data[index_1] = data[index_2]
        
        data[index_2] = passive
                                                                                                                  
    def update(self, data, values, index):  
        
        largest_node = max(values)[0]
        
        largest_node_index = max(values)[1]
        
        if largest_node_index != index:
            
            self.replace(data, largest_node_index, index)
            
        return largest_node_index
    
    def delete(self, data):
        
        passive = data[0]
            
        data[0] = data[-1]

        data.pop()
                                                                                                                         
        self.heapify(data, index = 0)    
        
    def insert(self, data, value):
        
        data.append(value)
        
        self.r_heapify(data, len(data) - 1)   
        
        
if __name__ == "__main__":
    # get parameters from terminal
    
    parser = argparse.ArgumentParser()
    
    subparser = parser.add_subparsers(dest= "algo")
        
    Merge = subparser.add_parser("Merge")
        
    Quick = subparser.add_parser("Quick")
    
    Heap_ = subparser.add_parser("Heap")
    
    # merge
    
    Merge.add_argument("--data", default= [3, 44, 38, 5, 47, 15, 36, 26, 27, 2, 46, 4, 4, 19, 50, 48],  nargs = "+", help='data to sort', type = int)
    
    # quick
    
    Quick.add_argument("--data", default= [3, 44, 38, 5, 47, 15, 36, 26, 27, 2, 46, 4, 4, 19, 50, 48],  nargs = "+", help='data to sort', type = int)
        
    #heap
        
    Heap_.add_argument("--data", default= [3, 44, 38, 5, 47, 15, 36, 26, 27, 2, 46, 4, 4, 19, 50, 48],  nargs = "+",  help='data to sort', type = int)
    
    # parse args
    
    args = parser.parse_args()
    
    # run

    if args.algo == "Merge":
        
        runner = MergeSort()
    
        print(f"returned sorted list is : {runner.doSort(args.data)}")
        
    
    if args.algo == "Quick":
        
        runner = QuickSort()
        
        print(f"returned sorted list is : {runner.doSort(args.data)}")
        
    if args.algo == "Heap":
            
        runner = Heap()
        
        data = runner.createHeap(args.data)
        
        print(f"returned sorted list is : {runner.doSort(data)}")
    