import numpy
import math
import pdb
from abc import ABC, abstractmethod
from collections import Counter
import argparse

class NegativePathError(Exception):
    
    def __init__(self, message):
        
        """
            
        a class to crate error for situations when encountering negative cycle in graph
        
        Args:

            message : message to be thrown
            
        Returns:

            no return (just create error object)

        """
        
        self.message = message
        
        
    def __str__(self):
        
        """
            
        modification to str representation of error object
        
        Args:

            no argument
            
        Returns:

            change string representation of obeject to be used when raising error

        """
        
        self.message = self.message + " in your data "
        
        return self.message
    
class Bellman:
    
    def __init__(self):
        
        """
            
        base class for running algorithm

        Args:

            no arument

        Returns:

            no return just initialize algorithm

        """
        
        pass
    
    def getData(self, path):
        
        """
            
        get data to create graph (array representation of graph)

        Args:

            path : directory which file is stored (txt.file)

        Returns:

            data : data created from text file (array representation of graph)
            
            edges : a list containing all nodes values
            
        """
        
        data, edges, set_ = {}, [], set()
        
        with open(path, "r") as f:
            
            line = f.readline()
            
            line = line.strip()
            
            origin_target_cost = line.split()
            
            while line != "":
                
                origin, target, cost = origin_target_cost[0], origin_target_cost[1], origin_target_cost[2]
                
                edges.append((origin, target))
                
                if data.get(origin) is None:
                    
                    data[origin] = {"nodes" : {target : int(cost)}, "value" : math.inf}
                    
                else:
                    
                    data[origin]["nodes"].update({target : int(cost)})
                    
                if data.get(target) is None:
                    
                    data[target] = {"nodes" : {}, "value" : math.inf}
                    
                line = f.readline()

                line = line.strip()

                origin_target_cost = line.split()
                    
        return data, edges
    
    
    
    def Search(self, data, edges, start, path_error = NegativePathError("negative path is detected")):
        
        """
            
        mai method to impelment algorithm

        Args:

            data : data created from text file (array representation of graph)
            
            edges : a list containing all nodes values
            
            start : which node wes should find it's shortest distances to other node
            
            path_error : error to be thrown when encountring negative cycles in graph

        Returns:

            no return --> update nodes value
            
        """
        
        data[start]["value"] = 0
        
        for iteration in range(len(list(data.keys())) - 1):
            
            for edge in edges:
                
                origin_node, target_node = edge[0], edge[1]
                
                if data[origin_node]["value"] + data[origin_node]["nodes"][target_node] < data[target_node]["value"]:
                                                                                   
                    data[target_node]["value"] = data[origin_node]["value"] + data[origin_node]["nodes"][target_node]
                    
        for edge in edges:
            
            origin_node, target_node = edge[0], edge[1]
            
            if data[origin_node]["value"] + data[origin_node]["nodes"][target_node] < data[target_node]["value"]:
                
                raise path_error
            
        return data
            
            
if __name__ == "__main__":
    # get parameters from terminal
    
    Bellman_Parser = argparse.ArgumentParser()
    
    #bfs
    
    Bellman_Parser.add_argument("--start", default="1", help='start node', type = str)
    
    Bellman_Parser.add_argument("--data_path", default="src/Bellman-Ford/data.txt",  help='path to data', type = str)
    
    # parse args
    
    args = Bellman_Parser.parse_args()
    
    # run
        
    runner = Bellman()
    
    data, edges = runner.getData(args.data_path)

    data = runner.Search(data, edges, start = args.start)
    
    print(f"from node {args.start} shortest path to all node is defined by values : {data}")
                


