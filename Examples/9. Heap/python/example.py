import heapq

operations = ["I -45", "I 653", "D 1", "I -642", "I 45", "I 97", "D 1", "D -1", "I 333"]

pq = []
operations = list(reversed(operations))

while operations:
    cmd = operations.pop().split()
    if cmd[0] == "I":
        heapq.heappush(pq, int(cmd[1]))
    else:
        if len(pq) != 0:
            if int(cmd[1]) == 1:
                pq.pop()
            else:
                heapq.heappop(pq)
pq = sorted(pq)

print([pq[-1], pq[0]] if len(pq) != 0 else [0,0])