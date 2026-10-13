"""Task 4: knapsack variants and Floyd-Warshall."""
from functools import lru_cache
PARCELS=[("P1",2,180),("P2",3,250),("P3",4,300),("P4",5,420),("P5",6,450),("P6",7,560),("P7",8,610),("P8",9,700)]
def naive_knapsack(capacity):
    calls=0
    def solve(i,w):
        nonlocal calls;calls+=1
        if i==len(PARCELS) or w<=0:return 0
        name,weight,value=PARCELS[i]
        if weight>w:return solve(i+1,w)
        return max(solve(i+1,w),value+solve(i+1,w-weight))
    return solve(0,capacity),calls
def memo_knapsack(capacity):
    calls=0
    @lru_cache(None)
    def solve(i,w):
        nonlocal calls;calls+=1
        if i==len(PARCELS) or w<=0:return 0
        _,weight,value=PARCELS[i]
        if weight>w:return solve(i+1,w)
        return max(solve(i+1,w),value+solve(i+1,w-weight))
    return solve(0,capacity),calls,solve
def bottom_up(capacity):
    n=len(PARCELS); dp=[[0]*(capacity+1) for _ in range(n+1)]
    for i in range(1,n+1):
        _,weight,value=PARCELS[i-1]
        for w in range(capacity+1):
            dp[i][w]=dp[i-1][w]
            if weight<=w:dp[i][w]=max(dp[i][w],value+dp[i-1][w-weight])
    chosen=[];w=capacity
    for i in range(n,0,-1):
        if dp[i][w]!=dp[i-1][w]:
            name,weight,value=PARCELS[i-1];chosen.append(name);w-=weight
    return dp[n][capacity],list(reversed(chosen)),dp
def greedy(capacity):
    chosen=[];w=0;v=0
    for name,weight,value in PARCELS:
        if w+weight<=capacity:chosen.append(name);w+=weight;v+=value
    return v,chosen,w
INF=float("inf")
HUBS=["Manila","Batangas","Iloilo","Cebu","Davao"]
DIRECT=[[0,4,INF,12,INF],[4,0,6,INF,INF],[INF,6,0,3,10],[12,INF,3,0,5],[INF,INF,10,5,0]]
def floyd_warshall():
    d=[row[:] for row in DIRECT]; nxt=[[j if d[i][j]!=INF else None for j in range(5)] for i in range(5)]
    snapshots=[]
    for k in range(5):
        for i in range(5):
            for j in range(5):
                if d[i][k]+d[k][j]<d[i][j]:
                    d[i][j]=d[i][k]+d[k][j];nxt[i][j]=nxt[i][k]
        snapshots.append([r[:] for r in d])
    path=[];i=0;j=4
    if nxt[i][j] is not None:
        path=[HUBS[i]]
        while i!=j:
            i=nxt[i][j];path.append(HUBS[i])
    return d,snapshots,path
if __name__=="__main__":
    S=7148;W=20+(S%11)
    print("Capacity:",W,"kg")
    print("Greedy:",greedy(W))
    value,chosen,dp=bottom_up(W);print("Optimal:",value,chosen,"weight",sum(x[1] for x in PARCELS if x[0] in chosen))
    nv,nc=naive_knapsack(W);mv,mc,_=memo_knapsack(W);print("Call counts naive/memo:",nc,mc)
    dist,snapshots,path=floyd_warshall()
    for i,matrix in enumerate(snapshots,1):print("k=",i,matrix)
    print("Manila to Davao:",dist[0][4],"thousand PHP; path:", " -> ".join(path))
