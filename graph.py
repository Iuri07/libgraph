import numpy as np
import random

class Graph:
    adjMatrix = 0    
    adjList = 1
    
    class AdjacencyMatrix:       
        def __init__(self, n):
            self.nCount = n
            self.m = np.zeros((n, n))
            
        def checkVertex(self, u):
            u -= 1
            return (u >= 0 and u < self.nCount)
        
        def addAdjacency(self, u, v):
            u -= 1
            v -= 1
            self.m[u,v] = 1
            self.m[v,u] = 1
            
        def getMaxDegree(self):
            return np.amax(self.m.sum(axis=0))
        
        def getMinDegree(self):
            return np.amin(self.m.sum(axis=0))

        def getAvgDegree(self):
            return np.average(self.m.sum(axis=0))
        
        def getDegreeMedian(self):
            return np.median(self.m.sum(axis=0))
        
        def getEdgeCount(self):
            return self.m.sum(axis=0).sum()/2

        def getNeighbours(self, u):
            u -= 1
            neighbours = [ i+1 for i in range(self.nCount) if self.m[u][i] == 1 ]
            neighbours.sort(reverse=True)
            return neighbours
        
        
                
    class AdjacencyList:
        def __init__(self, n):
            self.nCount = n
            self.l = [None]*n

        def checkVertex(self, u):
            return (u >= 0 and u < self.nCount)
        
        def addAdjacency(self, u, v):
            if self.checkVertex(u) and self.checkVertex(v):
                if self.l[u-1] == None:
                    self.l[u-1] = [v]
                elif v not in self.l[u-1]:
                    self.l[u-1].append(v)

                if self.l[v-1] == None:
                    self.l[v-1] = [u]
                elif u not in self.l[v-1]:
                    self.l[v-1].append(u)

        def getNeighbours(self, u):
            neighbours = self.l[u - 1]
            neighbours.sort(reverse=True)
            return neighbours
        
        def getVertexDegree(self, u):
            u -= 1
            if self.l[u]:
                return len(self.l[u])
            return 0
        
        def getMaxDegree(self):
            maxDegree = 0
            for vertex in self.l:
                if vertex:
                    maxDegree = max(maxDegree, len(vertex))
            return maxDegree
        
        def getMinDegree(self):
            minDegree = 100000000
            for vertex in self.l:
                if vertex:
                    minDegree = min(minDegree, len(vertex))
            return minDegree
        
        def getAvgDegree(self):
            degrees = [len(i) for i in self.l if i]
            return np.average(degrees)
        
        def getDegreeMedian(self):
            degrees = [len(i) for i in self.l if i]
            return np.median(degrees)
        
        def getEdgeCount(self):
            sum = 0
            for vertex in self.l:
                if vertex:
                    sum += len(vertex)
            return sum/2
         
        
    def __init__(self, filename, representationType):
        f = open(filename, 'r')
        n = int(f.readline())

        if representationType == self.adjMatrix:
            self.representation = self.AdjacencyMatrix(n)
        else:
            self.representation = self.AdjacencyList(n)
        
        while True:
            edge = f.readline().strip().split(' ')
            if len(edge) != 2:
                break
            self.representation.addAdjacency(int(edge[0]), int(edge[1]))
        f.close()
        
    def bfs(self, s):
        marked = [s]
        queue = [s]
        parent = [None]*self.representation.nCount
        level = [None]*self.representation.nCount
        parent[s-1] = 0
        level[s-1] = 0        
        
        while len(queue):
            v = queue.pop()
            for w in self.representation.getNeighbours(v):
                if w not in marked:
                    parent[w-1] = v
                    level[w-1] = level[v-1] + 1
                    marked.append(w)
                    queue.insert(0,w)
                    
        return marked, parent, level
    
    def dfs(self, s):
        marked = []
        stack = [s]
        parent = [None]*self.representation.nCount
        level = [None]*self.representation.nCount
        level[s-1] = 0
        
        while len(stack):
            u = stack.pop()
            if u not in marked:
                marked.append(u)
                for v in self.representation.getNeighbours(u):
                    if v not in marked:
                        parent[v-1] = u
                        level[v-1] = level[u-1]+1
                    stack.append(v)
        
        return marked, parent, level
    
    def getDistance(self, u, v):
        return self.bfs(u)[2][v-1]
    
    def getDiameter(self):
        maxDist = 0
        n = self.representation.nCount
       
        for root in range(1, n):
            bfs = self.bfs(root)
            level = bfs[2]
            for distance in level:
                if distance:
                    maxDist = max(maxDist, distance)
        return maxDist
    
    def getConnectedComponents(self):
        ccs = []
        marked = [0]*self.representation.nCount
        for root in range(1,self.representation.nCount):
            if not marked[root-1]:
                cc = self.bfs(root)[0]
                ccs.append(cc)
                for v in cc:
                    marked[v-1] = 1
        return ccs
        
    
    def dump(self):
        f = open("dump.txt", "w")
        f.write(str(self.representation.nCount)+'\n')
        f.write(str(self.representation.getMaxDegree())+'\n')
        f.write(str(self.representation.getMinDegree())+'\n')        
        f.write(str(self.representation.getMinDegree())+'\n')        
        f.write(str(self.representation.getAvgDegree())+'\n')
        f.write(str(self.representation.getDegreeMedian())+'\n')
        f.write(str(self.representation.getEdgeCount())+'\n') 
        f.close() 
    
    def dumpSpanningTree(self, u, treeType):
        bfs = 0
        dfs = 1
        
        parents = []
        level = []
        
        if treeType == bfs:
            parents = self.bfs(u)[1]
            level = self.bfs(u)[2]
        
        else:
            parents = self.dfs(u)[1]
            level = self.dfs(u)[2]

        f = open("tree.txt", "w")
        for i in range(self.representation.nCount):
            if level[i] != None:
                f.write("{} {} {}\n".format(i+1, parents[i], level[i]))
        f.close()
        