import numpy
import math
import pdb
from abc import ABC, abstractmethod
from collections import Counter
import argparse

class Base(ABC):
    
    def __init__(self):
        
        pass
    
    @abstractmethod
    def doSearch(self, path):
        
        pass
    
    
class BinarySearch(Base):
    
    def __init__(self):
        
        pass
    
    def doSearch(self, data, x, left, right):
        
        #pdb.set_trace()
        
        middle = left + (right - left) // 2
        
        if middle == len(data): 
            
            return "not detected"
        
        if data[middle] == x:
            
            return middle
        
        if middle == 0:
            
            return "not detected"
        
        if data[middle] < x:
            
            index = self.doSearch(data, x, middle + 1, right)
            
        else:
            
            index = self.doSearch(data, x, left, middle -1)
            
        return index
    
    
    
class FibunachiSearch:
    
    def __init__(self):
        
        pass
    
    def doSearch(self, data, value, array_length):
        
        fib_main, fib_1, fib_2 = self.findSmallGreaterLength(array_length)
        
        offset = -1
        
        while (fib_main > 1):
        
            target_index = min(fib_2 + offset, array_length - 1)

            if data[target_index] < value:

                fib_main = fib_1

                fib_1 = fib_2

                fib_2 = fib_main - fib_1

                offset = target_index

            elif data[target_index] > value:

                fib_main = fib_2

                fib_1 = fib_1 - fib_2

                fib_2 = fib_main - fib_1

            else:

                return target_index
        
        return "not finded"
    
    def findSmallGreaterLength(self, array_length):
        
        fib_2, fib_1 = 0, 1
        
        fib_main = fib_2 + fib_1
        
        while fib_main < array_length:
            
            fib_2 = fib_1
            
            fib_1 = fib_main
            
            fib_main = fib_1 + fib_2
            
        return fib_main, fib_1, fib_2
        
        
if __name__ == "__main__":
    # get parameters from terminal
    
    parser = argparse.ArgumentParser()
    
    subparser = parser.add_subparsers(dest= "algo")
        
    Binary = subparser.add_parser("Binary")
        
    Fibo = subparser.add_parser("Fibo")
    
    # binary
    
    Binary.add_argument("--data", default= [3, 9, 10, 27, 38, 43, 82],  nargs = "+", help='data to sort', type = int)
    
    Binary.add_argument("--value", default= 9,  help='value to search', type = int)
    
    # fibo
    
    Fibo.add_argument("--data", default= [3, 5, 15, 26, 27, 44,  46, 47,  50],  nargs = "+", help='data to sort', type = int)
    
    Fibo.add_argument("--value", default= 9,  help='value to search', type = int)
    
    # parse args
    
    args = parser.parse_args()
    
    # run

    if args.algo == "Binary":
        
        runner = BinarySearch()
    
        print(f" value {args.value} is at index {runner.doSearch(args.data, args.value, left = 0, right = len(args.data))} ")
        
    
    if args.algo == "Fibo":
        
        runner = FibunachiSearch()
        
        print(f" value {args.value} is at index {runner.doSearch(args.data, args.value, len(args.data))} ")
        
        
