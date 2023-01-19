import argparse
import numpy
import math
import pdb
from abc import ABC, abstractmethod

class Algo(ABC):
    
    def __init__(self):
        
        """
            
        base class to inherite

        Args:

            no argument

        Returns:

            no return --> just iniialize algorithm

        """
        
        pass
    
    def getData(self, file_path):
        
        """
            
        get data to create graph (array representation of graph)

        Args:

            file_path : directory which file is stored (txt.file)

        Returns:

            data : data created from text file (array representation of graph)

        """
        
        data = {}
        
        with open(file_path, "r") as f:
            
            line = f.readline()  
            
            line = line.strip()
            
            key_value_cost = line.split()
            
            while line != "":
                
                key, value, cost = key_value_cost[0], key_value_cost[1], key_value_cost[2]
                
                if data.get(key) is None and data.get(value) is None:

                    data[key] = {value : int(cost)}
                    
                    data[value] = {key : int(cost)}

                elif data.get(key) is None:
                    
                    data[key] = {value : int(cost)}
                    
                    data[value].update({key : int(cost)})
                    
                elif data.get(value) is None:
                    
                    data[value] = {key : int(cost)}
                    
                    data[key].update({value : int(cost)})
                    
                else:
                    
                    data[value].update({key : int(cost)})

                    data[key].update({value : int(cost)})

                line = f.readline()

                line = line.strip()

                key_value_cost = line.split()

        return data
    
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
    def checkVisited(self):
        
        """
            
        check node in adjacency nodes is visited before or not
        
        Args:

            adjacency_nodes : all node in adjacency of target node
            
            visited : list of all visited node up to now
        Returns:

            list of all nodes in adjacency_node list which haven't visited yet

        """
        
        pass
    
    
class UCS(Algo):
    
    def __init__(self):
        
        """
            
        base class for running algorithm

        Args:

            no arument

        Returns:

            no return just initialize algorithm

        """
        
        super(UCS, self).__init__()
        
        
        
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
        
        visited, options, solutions = [], {}, {}
        
        current_node = start
        
        visited.append(start)
        
        adjacency_nodes = list(data.get(current_node).keys())
        
        valid_keys = self.checkVisited(adjacency_nodes, visited)
        
        options = {(current_node, key) : data.get(current_node)[key] for key in valid_keys}
        
        index = 1

        while len(list(options.keys())):
            
            (cost, path) = self.pickNode(options)
            
            current_node = path[-1]
            
            visited.append(current_node)
            
            if current_node == goal:
                
                solutions["solution_" + str(index)] = {"path" : path, "cost" : cost}
                
                index += 1
                
                del options[path]
                
                continue
            
            if data.get(current_node) is None:
                
                del options[path]
                
            else:
            
                adjacency_nodes = list(data.get(current_node).keys())
            
                valid_keys = self.checkVisited(adjacency_nodes, visited)
            
                path_cost = options[path]
            
                del options[path]
            
                options.update({path + (key,) : path_cost + data.get(current_node)[key] for key in valid_keys})
                
        return solutions
    
    def checkVisited(self, adjacency_nodes, visited):
        
        """
            
        check node in adjacency nodes is visited before or not
        
        Args:

            adjacency_nodes : all node in adjacency of target node
            
            visited : list of all visited node up to now
        Returns:

            list of all nodes in adjacency_node list which haven't visited yet

        """
        
        return list(filter(lambda x : not(x in visited), adjacency_nodes))
    
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
    
    parser = argparse.ArgumentParser()
    
    subparser = parser.add_subparsers(dest= "algo")
        
    UCS_Parser = subparser.add_parser("UCS")
    
    #bfs
    
    UCS_Parser.add_argument("--start", default="1", help='which node we start', type = str)
        
    UCS_Parser.add_argument("--goal", default="2",  help='which node we want to go', type = str)
    
    UCS_Parser.add_argument("--data_path", default="src/UCS/data.txt",  help='path to data', type = str)

    
    # parse args
    
    args = parser.parse_args()
    
    # run
    
    if args.algo == "UCS":
        
        runner = UCS()
        
        data = runner.getData(args.data_path)
    
        print(runner.Search(data, start = args.start, goal = args.goal))