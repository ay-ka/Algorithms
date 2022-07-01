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
            
            # get line
            
            line = f.readline()
            
            # remove scraps
            
            line = line.strip()
            
            # split to key and value
            
            key_value_lst = line.split()
            
            while line != "":
                
                key, value = key_value_lst[0], key_value_lst[1]
                
                if data.get(key) != None and data.get(value) != None:
                    
                    data[key].append(value)                    
                    
                    data[value].append(key)
                        
                elif data.get(key) != None:
                    
                    data[value] = [key]
                    
                    data[key].append(value)
                    
                elif data.get(value) != None:
                    
                    data[key] = [value]
                    
                    data[value].append(key)
                    
                else:
                    
                    data[key] = [value]
                    
                    data[value] = [key]   
                    
                # get line

                line = f.readline()

                # remove scraps

                line = line.strip()

                # split to key and value

                key_value_lst = line.split()

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
    def checkVisited(self, adjacency_list):
        
        """
            
        check node in adjacency nodes is visited before or not
        
        Args:

            adjacency_nodes : all node in adjacency of target node
            
            visited : list of all visited node up to now
        Returns:

            list of all nodes in adjacency_node list which haven't visited yet

        """
        
        raise NotImplementedError()
    
    
    
class BFS(Algo):
    
    def __init__(self):
        
        """
            
        base class for running algorithm

        Args:

            no arument

        Returns:

            no return just initialize algorithm

        """
        
        super(BFS, self).__init__()
        
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
        
        start, goal = str(start), str(goal)
        
        queue = []
        
        visited = []
        
        adjacency_nodes = data.get(start)
        
        visited.append(start)
        
        queue.append(start)
        
        while len(queue):
        
            adjacency_nodes = self.checkVisited(adjacency_nodes, visited)

            adjacency_nodes = self.check_container(adjacency_nodes, queue)
            
            try:
            
                adjacency_nodes = list(map(lambda x : str(x), sorted(list(map(lambda x : int(x), adjacency_nodes)))))
                
            except:
                
                adjacency_nodes.sort()

            queue.extend(adjacency_nodes)
            
            queue.pop(0)
            
            next_node = queue[0]
            
            visited.append(next_node)
            
            adjacency_nodes = data[next_node]
            
            if next_node == goal:
                
                break
                
        return visited
        
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
    
    def check_container(self, adjacency_nodes, queue):
        
        """
            
        check node in adjacency nodes are inserted to queue or not
        
        Args:

            adjacency_nodes : all node in adjacency of target node
            
            queue : data structure for nodes to be selected and avaluated
            
        Returns:

            list of all nodes in adjacency_node list which haven't been inserted to queue yet

        """
        
        return list(filter(lambda x : not(x in queue), adjacency_nodes))
    
    
class DFS(Algo):
    
    def __init__(self):
        
        """
            
        base class for running algorithm

        Args:

            no arument

        Returns:

            no return just initialize algorithm

        """
        
        super(DFS, self).__init__()
        
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
        
        start, goal = str(start), str(goal)
        
        stack, visited = [], []
        
        current_node = start
        
        stack.append(start)
        
        visited.append(start)
        
        adjacency_nodes = data.get(start)
        
        stack.pop(-1)
        
        while current_node != goal:
            
            adjacency_nodes = self.checkVisited(adjacency_nodes, visited)
            
            try:
            
                adjacency_nodes = list(map(lambda x : str(x), sorted(list(map(lambda x : int(x), adjacency_nodes)))))
                
            except:
                
                adjacency_nodes.sort()
            
            adjacency_nodes = list(reversed(adjacency_nodes))
            
            stack.extend(adjacency_nodes)
            
            current_node = stack.pop(-1)
            
            visited.append(current_node)
            
            adjacency_nodes = data.get(current_node)
            
        return visited
        
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

    
    
if __name__ == "__main__":
    # get parameters from terminal
    
    parser = argparse.ArgumentParser()
    
    subparser = parser.add_subparsers(dest= "algo")
        
    BFS_Parser = subparser.add_parser("BFS")
        
    DFS_Parser = subparser.add_parser("DFS")
    
    #bfs
    
    BFS_Parser.add_argument("--start", default="1", help='start node', type = str)
        
    BFS_Parser.add_argument("--goal", default="2",  help='goal node', type = str)
    
    BFS_Parser.add_argument("--data_path", default="src/BFS-DFS/data.txt",  help='path to data', type = str)
    
    # dfs
    
    DFS_Parser.add_argument("--start", default="1", help='start node', type = str)
        
    DFS_Parser.add_argument("--goal", default="2",  help='goal node', type = str)
    
    DFS_Parser.add_argument("--data_path", default="src/BFS-DFS/data.txt",  help='path to data', type = str)
    
    # parse args
    
    args = parser.parse_args()
    
    # run

    if args.algo.upper() == "BFS":
        
        runner = BFS()
        
        data = runner.getData(args.data_path)
    
        print(runner.Search(data, args.start, args.goal))
        
    
    if args.algo.upper() == "DFS":
        
        runner = DFS()
        
        data = runner.getData(args.data_path)
    
        print(runner.Search(data, args.start, args.goal))