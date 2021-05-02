import time
from graph import Graph

a = Graph('../grafo_1.txt', 1)
a.dumpSpanningTree(1, 0)

# time.sleep(1000)

# import time
# vertices = [random.randrange(1, a.representation.nCount, 1) for i in range(1000)]
# start_time = time.time()
# for v in vertices:
#     a.bfs(v)
    
# print("--- %s seconds ---" % ((time.time() - start_time)/1000))

# start_time = time.time()
# for v in vertices:
#     a.dfs(v)
    
# print("--- %s seconds ---" % ((time.time() - start_time)/1000))