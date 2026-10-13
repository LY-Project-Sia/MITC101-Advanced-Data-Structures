"""Task 1: program structure, analysis, simulation, sorting and selection."""
from __future__ import annotations
import random, time, math

def remove_duplicates(scans):
    seen=set(); out=[]
    for value in scans:
        if value not in seen:
            seen.add(value); out.append(value)
    return out

def legacy_remove_duplicates(scans):
    unique=[]
    for s in scans:
        found=False
        for u in unique:
            if u == s: found=True
        if not found: unique.append(s)
    return unique

def bubble_sort(values):
    a=list(values); n=len(a)
    for i in range(n):
        swapped=False
        for j in range(0,n-i-1):
            if a[j] > a[j+1]:
                a[j],a[j+1]=a[j+1],a[j]; swapped=True
        if not swapped: break
    return a

def merge_sort(values):
    a=list(values)
    if len(a)<=1: return a
    mid=len(a)//2
    left=merge_sort(a[:mid]); right=merge_sort(a[mid:])
    out=[]; i=j=0
    while i<len(left) and j<len(right):
        if left[i] <= right[j]: out.append(left[i]); i+=1
        else: out.append(right[j]); j+=1
    out.extend(left[i:]); out.extend(right[j:])
    return out

def quick_sort(values, rng=None):
    rng=rng or random.Random(0)
    a=list(values)
    def part(lo,hi):
        if lo>=hi: return
        pivot_idx=rng.randrange(lo,hi+1)
        a[pivot_idx],a[hi]=a[hi],a[pivot_idx]
        pivot=a[hi]; i=lo
        for j in range(lo,hi):
            if a[j] <= pivot:
                a[i],a[j]=a[j],a[i]; i+=1
        a[i],a[hi]=a[hi],a[i]
        part(lo,i-1); part(i+1,hi)
    # Iterative stack prevents Python recursion overflow on unlucky inputs.
    stack=[(0,len(a)-1)]
    while stack:
        lo,hi=stack.pop()
        while lo<hi:
            pi=rng.randrange(lo,hi+1)
            a[pi],a[hi]=a[hi],a[pi]
            pivot=a[hi]; i=lo
            for j in range(lo,hi):
                if a[j] <= pivot:
                    a[i],a[j]=a[j],a[i]; i+=1
            a[i],a[hi]=a[hi],a[i]
            # Continue on smaller partition and stack larger to bound stack depth.
            left=(lo,i-1); right=(i+1,hi)
            if left[1]-left[0] < right[1]-right[0]:
                if right[0]<right[1]: stack.append(right)
                lo,hi=left
            else:
                if left[0]<left[1]: stack.append(left)
                lo,hi=right
    return a

def randomized_select(values, k, rng=None):
    """Return zero-based kth order statistic in expected O(n)."""
    if not 0 <= k < len(values): raise IndexError("k out of range")
    a=list(values); rng=rng or random.Random(0); lo=0; hi=len(a)-1
    while lo<=hi:
        p=rng.randrange(lo,hi+1); a[p],a[hi]=a[hi],a[p]
        pivot=a[hi]; store=lo
        for j in range(lo,hi):
            if a[j] < pivot:
                a[store],a[j]=a[j],a[store]; store+=1
        a[store],a[hi]=a[hi],a[store]
        if store==k: return a[store]
        if k<store: hi=store-1
        else: lo=store+1
    raise RuntimeError("selection failed")

def hiring_updates(m, trials=10000, seed=7148):
    rng=random.Random(seed)
    # Relative ranks 1..m in a uniformly random permutation.
    total=0
    for _ in range(trials):
        order=list(range(1,m+1)); rng.shuffle(order)
        best=0
        for rank in order:
            if rank>best: best=rank; total+=1
    return total/trials, sum(1/i for i in range(1,m+1))

def benchmark(sizes=(8148,17148,107148), seed=7148):
    rng=random.Random(seed); rows=[]
    for n in sizes:
        values=[rng.random()*100 for _ in range(n)]
        for name,fn in [("merge_sort",merge_sort),("randomized_quick_sort",quick_sort),("sorted/Timsort",sorted)]:
            start=time.perf_counter(); result=fn(values); elapsed=time.perf_counter()-start
            assert result==sorted(values)
            rows.append({"n":n,"algorithm":name,"seconds":elapsed,"status":"measured"})
        # Quadratic bubble sort only for small sizes; never pretend 100k is feasible.
        if n<=10000:
            small=values[:]; start=time.perf_counter(); result=bubble_sort(small); elapsed=time.perf_counter()-start
            assert result==sorted(values)
            rows.append({"n":n,"algorithm":"bubble_sort","seconds":elapsed,"status":"measured"})
        else:
            rows.append({"n":n,"algorithm":"bubble_sort","seconds":None,"status":"skipped: O(n^2) benchmark impractical"})
    return rows

if __name__=="__main__":
    S=7148
    m=50+(S%50)
    print("Task 1 | S=",S,"n=",1000+S,"audit m=",m)
    avg,theory=hiring_updates(m,10000,S)
    print(f"Hiring updates: simulated={avg:.4f}; harmonic expectation={theory:.4f} (10,000 trials)")
    data=[(f"SC{i:010d}",float((i*17)%70)) for i in range(100)]
    print("Dedup sample:",len(remove_duplicates([x for x,_ in data]+[data[0][0]])))
    print("Median/90th weight demo:",randomized_select([x for x in [9,1,4,7,2,8,3,6,5,10]],4),randomized_select([9,1,4,7,2,8,3,6,5,10],8))
