from ast import operator
from collections import OrderedDict
import numpy as np
import math
import pdb
from abc import ABC, abstractmethod
from collections import Counter
import argparse
import copy

class linkedList():
    
    def __init__(self, value):
        
        self.value = value
        
        self.next = None
        
        self.head_key = None
        



class Operation:
    
    def __init__(self):
        
        self.linked_list = {}
    
    def GetData(self, path):
            
        data = OrderedDict()
        
        with open(path, "r") as f:
            
            line = f.readline()
            
            line = line.strip()
            
            key_value = line.split()
            
            while line != "":
            
                data[key_value[0]] = key_value[1]
                
                line = f.readline()
                
                line = line.strip()
                
                key_value = line.split()
                
        return data 
    
    def create_list(self, data):
        
        keys = list(data.keys())
        
        self.head = linkedList(data.pop(keys[0]))
        
        self.head.head_key = keys[0]
        
        self.linked_list = {data_key : linkedList(data_value) for data_key, data_value in data.items()}
        
        keys = list(self.linked_list.keys())
        
        self.head.next = self.linked_list[keys[0]]
        
        #########
        
        for idx, key in enumerate(keys):
            
            try:
            
                self.linked_list[keys[idx]].next = self.linked_list[keys[idx + 1]]
                
            except : pass
    
    def insert(self, head, LinkedList, index, value):
        
        current_node = head
        
        for iteration in range(index - 2):
            
            current_node = current_node.next
            
        next_ = current_node.next
        
        new_node = LinkedList(value)
            
        current_node.next = new_node
        
        new_node.next = next_
            
    def delete(self, head, index):
        
        current_node = head
        
        for iteration in range(index - 2):
            
            current_node = current_node.next
            
        current_node.next = current_node.next.next
    
    def reverse(self, head):
        
        prev = None
        
        keys = list(self.linked_list.keys())
        
        current = head
        
        while current != None:
            
            next_ = current.next
            
            current.next = prev
            
            prev = current
            
            current = next_
            
        head_candidate = self.linked_list.pop(list(self.linked_list.keys())[-1])
        
        self.linked_list[self.head.head_key] = copy.deepcopy(self.head)
        
        head_candidate.head_key = keys[-1]
        
        self.head = head_candidate
    
    def findValue(self, head, index):
        
        current_node = head
        
        count = 0
        
        while head != None:
            
            if count == index - 1:
                
                return current_node.value
            
            current_node = current_node.next
            
            count += 1
        
        return "no value"
    
    def findIndex(self, head, value):
        
        current_node = head
        
        count = 0
        
        while current_node != None:
            
            if current_node.value == value:
                
                return count + 1
            
            count += 1
            
            current_node = current_node.next
                
        return "no value"



if __name__ == "__main__":

    # get parameters from terminal
    
    parser = argparse.ArgumentParser()
    
    subparser = parser.add_subparsers(dest= "algo")
        
    LinkedList_Parser = subparser.add_parser("LinkedList")
    
    #linkedlist
    
    LinkedList_Parser.add_argument("--value", help='find index of value', type = str, default = None)
    
    LinkedList_Parser.add_argument("--index", help='find value by index', type = int, default = None)
    
    LinkedList_Parser.add_argument("--delete_val_index", help='delete value to this index', type = int, default = None)
    
    LinkedList_Parser.add_argument("--insert_index", help='insert value to this index', type = int, default = None)
    
    LinkedList_Parser.add_argument("--insert_value", help='insert this value to defined index', default = None, type = str)
    
    LinkedList_Parser.add_argument("--reverse", help='insert this value to defined index', action = "store_true")

    LinkedList_Parser.add_argument("--data_path", default = "src/LinkedList/data.txt", help='path to data', type = str)
    
    # parse args
    
    args = parser.parse_args()
    
    # run
    
    if args.algo == "LinkedList":
        
        runner = Operation()
        
        data = runner.GetData(args.data_path)
        
        runner.create_list(data)
        
        if args.value != None:
            
            print(f" value {args.value} found in index {runner.findIndex(head = runner.head, value = args.value)} ")
         
        if args.index != None:
            
            print(f"value {runner.findValue(head = runner.head, index = args.index)} found in index {args.index} ")
            
        if args.delete_val_index != None:
            
            runner.delete(head = runner.head, index = args.delete_val_index)
            
            print("requested node deleted")
            
        if args.reverse:
            
           runner.reverse(head = runner.head)  
           
           print(f"list reversed and now head's key is : {runner.head.head_key} and head's value is : {runner.head.value}") 
           
        if args.insert_index and args.insert_value:
        
           runner.insert(head = runner.head, LinkedList = linkedList, index = args.insert_index, value = args.insert_value)  
        
           print(f" value {args.insert_value} inserted in index {args.insert_index}")

        
        


