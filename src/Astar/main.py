import numpy
import math
import pdb
from abc import ABC, abstractmethod
from collections import Counter
import argparse

class Algo(ABC):
    
    def __init__(self):
        
        """
            
        base class to inherite

        Args:

            no argument

        Returns:

            no return --> just iniialize algorithm

        """
        
        self.data = {}
    
    def getData(self, file_path, distance = True):
        
        """
            
        get data to create graph (array representation of graph)

        Args:

            file_path : directory which file is stored (txt.file)

        Returns:

            no return --> just bilud array as a representation of graph

        """
        
        data = {}
        
        if distance:
        
            with open(file_path, "r") as f:

                line = f.readline()  

                line = line.strip()

                key_value_cost = line.split()

                while line != "":

                    key, value, cost = key_value_cost[0].upper(), key_value_cost[1].upper(), key_value_cost[2]

                    if self.data.get(key) is None and self.data.get(value) is None:

                        self.data[key] = {"nodes" : {value : int(cost)} }

                        self.data[value] = {"nodes" : {key : int(cost)} }

                    elif self.data.get(key) is None:

                        self.data[key] = {"nodes" : {value : int(cost)} }

                        self.data[value]["nodes"].update({key : int(cost)})

                    elif self.data.get(value) is None:

                        self.data[value] = {"nodes" : {key : int(cost)} }

                        self.data[key]["nodes"].update({value : int(cost)})

                    else:

                        self.data[value]["nodes"].update({key : int(cost)})

                        self.data[key]["nodes"].update({value : int(cost)})

                    line = f.readline()

                    line = line.strip()

                    key_value_cost = line.split()
                    
        else:
                
            with open(file_path, "r") as f:    
                
                line = f.readline()  

                line = line.strip()
                
                key_huristic = line.split()
                
                while line != "":
                    
                    key, huristic = key_huristic[0].upper(), key_huristic[1]
                    
                    if self.data.get(key) is None:
                        
                        self.data[key] = {"huristic" : int(huristic), "nodes" : {}}
                        
                    else:
                        
                        self.data[key].update({"huristic" : int(huristic)})
                        
                    line = f.readline()

                    line = line.strip()

                    key_huristic = line.split()

    
    @abstractmethod
    def Search(self, data, start, goal):
        
        """
            
        method for main part of algorithm (Search)

        Args:

            data : array representation of graph 
            
            start : start node to begin (number in string format)
            
            goal : goal node to raech (number in string format)

        Returns:

            solutions : dictionarycontaining all the solutions available

        """
        
        pass
    
    @abstractmethod
    def checkLoop(self, adjacency_nodes, path):
        
        """
            
        abstract method removing loops (path which are cycle) in graph

        Args:

            adjacency_nodes : all node in adjacency of target node
            
            path : chosen path in current iteration (target node is derived from this path)

        Returns:

            list of all nodes which by selecting dosen't make cycle in cntinuing current path

        """
        
        pass
    
    
    
class AStar(Algo):
    
    def __init__(self):
        
        """
            
        base class for running algorithm

        Args:

            no arument

        Returns:

            no return just initialize algorithm

        """
        
        super(AStar, self).__init__()
        
    def Search(self, data, start, goal):
        
        """
            
        method for main part of algorithm (Search)

        Args:

            data : array representation of graph 
            
            start : start node to begin (number in string format)
            
            goal : goal node to raech (number in string format)

        Returns:

            solutions : dictionarycontaining all the solutions available

        """
        
        current_node = start
        
        options, solutions = {}, {}
        
        adjacency_nodes = list(data.get(current_node)["nodes"].keys())
        
        valid_keys = self.checkLoop(adjacency_nodes, [current_node])
        
        options = {(current_node, key) : data.get(current_node)["nodes"][key] + data.get(key)["huristic"]
                                                                                       for key in valid_keys}
        index = 1
        
        while len(list(options.keys())):
            
            (cost, path) = self.pickNode(options)
            
            current_node = path[-1]
            
            if current_node == goal:
                
                solutions["solution_" + str(index)] = {"path" : path, "cost" : cost}
                
                index += 1
                
                del options[path]
                
                continue
                
            if data.get(current_node)["nodes"] is None:
                
                del options[path]  
                
            
            else:
            
                adjacency_nodes = list(data.get(current_node)["nodes"].keys())
            
                valid_keys = self.checkLoop(adjacency_nodes, path)
            
                path_cost = options[path]
                
                path_cost -= data[current_node]["huristic"]
            
                del options[path]
            
                options.update({path + (key,) : 
                                path_cost + data.get(current_node)["nodes"][key] + data.get(key)["huristic"] 
                                for key in valid_keys})
                
                self.removeSamePath(options)
                
        return solutions
    
    
    def checkLoop(self, adjacency_nodes, path):
        
        """
            
        abstract method removing loops (path which are cycle) in graph

        Args:

            adjacency_nodes : all node in adjacency of target node
            
            path : chosen path in current iteration (target node is derived from this path)

        Returns:

            list of all nodes which by selecting dosen't make cycle in cntinuing current path

        """
        
        return list(filter(lambda x : not(x in path), adjacency_nodes)) 
    
    
    
    def removeSamePath(self, options):
        
        """
            
        remove all path ending up to same node except the path with minimum cost

        Args:

            options : options currently available to choose one path from

        Returns:

            no return just update our options

        """
        
        same_path = [end_node for end_node, number_occurence in 
                         Counter(list(map(lambda x : x[-1], list(options.keys())))).items()
                         if number_occurence > 1]
        
        for node in same_path:
            
            cost_path = list(map(lambda x : (options[x], x) ,
                        list(filter(lambda x : x[-1] == node , list(options.keys())))))
            
            cost_paths = sorted(cost_path)
            
            for path_index in range(1, len(cost_paths)):
                
                path = cost_paths[path_index][1]
                
                del options[path]
        
    def pickNode(self, options):
        
        """
            
        select next node from path availbale with minimum cost

        Args:

            options : options currently available to choose one path from

        Returns:

            a tuple containing path with minimum cost available to choose and derive node from it alongside the cost of it

        """
      
        selection_list = [(cost, path) for path, cost in options.items()]
        
        selection_list = sorted(selection_list)
        
        return selection_list[0]
    
    
    
if __name__ == "__main__":
    
    
    # get parameters from terminal
    
    Astar_Parser = argparse.ArgumentParser()
    
    #bfs
    
    Astar_Parser.add_argument("--start", default="s", help='start node', type = str)
        
    Astar_Parser.add_argument("--goal", default="f",  help='goal node', type = str)
    
    Astar_Parser.add_argument("--data_distances", default="src/Astar/data_distances.txt",  help='path to data_distances.txt', type = str)
    
    Astar_Parser.add_argument("--data_heuristics", default="src/Astar/data_heuristics.txt",  help='path to data_heuristic.txt values', type = str)
    
    # parse args
    
    args = Astar_Parser.parse_args()
    
    # run
        
    runner = AStar()
    
    runner.getData(args.data_distances, distance = True)
    
    runner.getData(args.data_heuristics, distance = False)
    
    data = runner.data

    sollutions = runner.Search(data, start = args.start.upper(), goal = args.goal.upper())
    
    print(sollutions)