def makeSet(p,r,i):
    p[i] = i

def findSet(p,r,i):
    # print(f"called findSet with {i}")
    if p[i] != i:
        pi = p[i]
        # print(f"p[i] is {pi}")
        p[i] = findSet(p,r,pi)
    # print(f"parent of {i} is {p[i]}")
    return(p[i])

def merge(p,r,i,j):
    if r[i] > r[j]:
        p[j] = i
        r[j]+=1
    if r[i] == r[j]:
        p[j] = i
        r[i] =+ r[j]
    if r[i] < r[j]:
        p[i] = j
        r[i]+=1

def union(p,r,i,j):
    merge(p,r,findSet(p,r,i), findSet(p,r,j))