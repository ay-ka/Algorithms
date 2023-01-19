import numpy
import math
import pdb
from abc import ABC, abstractmethod
from collections import Counter
import argparse


class Dijkstra:
    
    def __init__(self):
        
        pass
    
    def getData(self, path):
        
        data = {}
        
        with open(path, "r") as f:
            
            line = f.readline()
            
            line = line.strip()
            
            origin_target_cost = line.split()
            
            while line != "":
                
                origin, target, cost = origin_target_cost[0], origin_target_cost[1], origin_target_cost[2]
                
                if data.get(origin) is None:
                    
                    data[origin] = {"nodes" : {target : int(cost)}, "value" : math.inf}
                    
                else:
                    
                    data[origin]["nodes"].update({target : int(cost)})
                    
                if data.get(target) is None:
                    
                    data[target] = {"nodes" : {}, "value" : math.inf}
                    
                line = f.readline()

                line = line.strip()

                origin_target_cost = line.split()
                
        return data
    
    def Search(self, data, start):
        
        visited, options = [], {}
        
        data[start]["value"] = 0
        
        options.update({start : data[start]["value"]})
        
        while len(list(options.keys())) != 0:
            
            current_node = min(options, key = options.get)
            
            adjacency_nodes = data[current_node]["nodes"]
            
            visited.append(current_node)
        
            valid_adjacencies = self.checkVisited(adjacency_nodes, visited)

            for node in valid_adjacencies:

                if data[current_node]["value"] + data[current_node]['nodes'][node] < data[node]["value"]:

                    data[node]["value"] = data[current_node]["value"] + data[current_node]['nodes'][node] 
                    
            del options[current_node]
                    
            options.update({node : data[node]["value"] for node in valid_adjacencies})
            
        return data
        
        
    def checkVisited(self, adjacency_nodes, visited):
        
        return list(filter(lambda x : not(x in visited), adjacency_nodes))
    
    
    
    
    
if __name__ == "__main__":
    
    # get parameters from terminal

    Dijkstra_Parser = argparse.ArgumentParser()
    
    #bfs
    
    Dijkstra_Parser.add_argument("--start", default="1", help='start node', type = str)
    
    Dijkstra_Parser.add_argument("--data_path", default="SRC/Dijkstra/data.txt",  help='path to data', type = str)
    
    # parse args
    
    args = Dijkstra_Parser.parse_args()
    
    # run
        
    runner = Dijkstra()
    
    data = runner.getData(args.data_path)

    print(runner.Search(data, start = args.start))