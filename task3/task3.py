"""Task 3: chained/open-address hash tables and BST operations."""
import math, random
def division_hash(key,m):
    digits=int(key[2:]); return digits % m
def multiplication_hash(key,m):
    digits=int(key[2:]); A=(math.sqrt(5)-1)/2
    return int(m*((digits*A)%1))
def is_prime(n):
    if n<2:return False
    return all(n%d for d in range(2,int(math.sqrt(n))+1))
def next_prime(n):
    n+=1
    while not is_prime(n):n+=1
    return n

class ChainedHash:
    def __init__(self,m,hash_fn=division_hash):self.m=m;self.h=hash_fn;self.b=[[] for _ in range(m)]
    def insert(self,key):
        bucket=self.b[self.h(key,self.m)]
        if key not in bucket:bucket.append(key)
    def search(self,key):
        bucket=self.b[self.h(key,self.m)]
        for i,x in enumerate(bucket,1):
            if x==key:return True,i
        return False,len(bucket)
    def stats(self):
        lengths=[len(x) for x in self.b]
        return {"alpha":sum(lengths)/self.m,"longest_chain":max(lengths,default=0)}

class LinearProbingHash:
    def __init__(self,m,hash_fn=division_hash):self.m=m;self.h=hash_fn;self.a=[None]*m;self.size=0
    def insert(self,key):
        i=self.h(key,self.m)
        for probes in range(1,self.m+1):
            j=(i+probes-1)%self.m
            if self.a[j] is None:self.a[j]=key;self.size+=1;return probes
            if self.a[j]==key:return probes
        raise OverflowError("hash table full")
    def search(self,key):
        i=self.h(key,self.m)
        for probes in range(1,self.m+1):
            j=(i+probes-1)%self.m
            if self.a[j] is None:return False,probes
            if self.a[j]==key:return True,probes
        return False,self.m
    def stats(self):
        longest=0; run=0
        for x in self.a+self.a:
            run=run+1 if x is not None else 0; longest=max(longest,run)
        return {"alpha":self.size/self.m,"longest_occupied_run":min(longest,self.m)}

class BSTNode:
    def __init__(self,key):self.key=key;self.left=None;self.right=None
class BST:
    def __init__(self):self.root=None
    def insert(self,key):
        if self.root is None:self.root=BSTNode(key);return
        n=self.root
        while True:
            if key<n.key:
                if n.left:n=n.left
                else:n.left=BSTNode(key);return
            elif key>n.key:
                if n.right:n=n.right
                else:n.right=BSTNode(key);return
            else:return
    def search(self,key):
        n=self.root
        while n:
            if key==n.key:return n
            n=n.left if key<n.key else n.right
        return None
    def minimum(self,node=None):
        n=node or self.root
        if not n:return None
        while n.left:n=n.left
        return n.key
    def maximum(self,node=None):
        n=node or self.root
        if not n:return None
        while n.right:n=n.right
        return n.key
    def inorder(self):
        out=[]
        def walk(n):
            if n:walk(n.left);out.append(n.key);walk(n.right)
        walk(self.root);return out
    def height(self):
        def h(n):return -1 if n is None else 1+max(h(n.left),h(n.right))
        return h(self.root)
    def delete(self,key):
        def rec(n,key):
            if not n:return None
            if key<n.key:n.left=rec(n.left,key)
            elif key>n.key:n.right=rec(n.right,key)
            else:
                if not n.left:return n.right
                if not n.right:return n.left
                succ=n.right
                while succ.left:succ=succ.left
                n.key=succ.key;n.right=rec(n.right,succ.key)
            return n
        self.root=rec(self.root,key)

if __name__=="__main__":
    S=7148; m=next_prime(1000+S); print("S=",S,"table size=",m)
    names=["Abad","Bautista","Cruz","Dela Cruz","Espiritu","Flores","Garcia","Hernandez","Ilagan","Jimenez"]
    b=BST()
    for name in names:b.insert(name)
    print("Sorted-insertion BST height (edges):",b.height(),"worst comparisons:",len(names))
    shuffled=BST()
    for name in ["Flores","Bautista","Hernandez","Abad","Jimenez","Cruz","Ilagan","Dela Cruz","Garcia","Espiritu"]:shuffled.insert(name)
    print("Shuffled BST height (edges):",shuffled.height())
    keys=[f"SC{i:010d}" for i in range(5000)]
    h=ChainedHash(m)
    for k in keys:h.insert(k)
    print("Chaining stats:",h.stats())
    op=LinearProbingHash(next_prime(2*len(keys)))
    for k in keys:op.insert(k)
    print("Linear probing stats:",op.stats())


class RBNode:
    def __init__(self,key,color="RED"):
        self.key=key;self.color=color;self.left=None;self.right=None;self.parent=None
class RedBlackTree:
    def __init__(self):self.nil=RBNode(None,"BLACK");self.root=self.nil;self.events=[]
    def left_rotate(self,x):
        y=x.right;x.right=y.left
        if y.left is not self.nil:y.left.parent=x
        y.parent=x.parent
        if x.parent is self.nil:self.root=y
        elif x is x.parent.left:x.parent.left=y
        else:x.parent.right=y
        y.left=x;x.parent=y;self.events.append(f"left rotation at {x.key}")
    def right_rotate(self,y):
        x=y.left;y.left=x.right
        if x.right is not self.nil:x.right.parent=y
        x.parent=y.parent
        if y.parent is self.nil:self.root=x
        elif y is y.parent.right:y.parent.right=x
        else:y.parent.left=x
        x.right=y;y.parent=x;self.events.append(f"right rotation at {y.key}")
    def insert(self,key):
        z=RBNode(key);z.left=z.right=self.nil
        y=self.nil;x=self.root
        while x is not self.nil:
            y=x;x=x.left if z.key<x.key else x.right
        z.parent=y
        if y is self.nil:self.root=z
        elif z.key<y.key:y.left=z
        else:y.right=z
        z.color="RED";self._fix(z)
    def _fix(self,z):
        while z.parent.color=="RED":
            if z.parent is z.parent.parent.left:
                y=z.parent.parent.right
                if y.color=="RED":
                    z.parent.color=y.color="BLACK";z.parent.parent.color="RED"
                    self.events.append(f"recolor around {z.parent.parent.key} (uncle red)")
                    z=z.parent.parent
                else:
                    if z is z.parent.right:z=z.parent;self.left_rotate(z)
                    z.parent.color="BLACK";z.parent.parent.color="RED";self.right_rotate(z.parent.parent)
            else:
                y=z.parent.parent.left
                if y.color=="RED":
                    z.parent.color=y.color="BLACK";z.parent.parent.color="RED"
                    self.events.append(f"recolor around {z.parent.parent.key} (uncle red)")
                    z=z.parent.parent
                else:
                    if z is z.parent.left:z=z.parent;self.right_rotate(z)
                    z.parent.color="BLACK";z.parent.parent.color="RED";self.left_rotate(z.parent.parent)
        if self.root.color!="BLACK":self.events.append("recolor root BLACK")
        self.root.color="BLACK"
    def inorder(self):
        out=[]
        def walk(n):
            if n is not self.nil:walk(n.left);out.append((n.key,n.color));walk(n.right)
        walk(self.root);return out
    def height(self):
        def h(n):return -1 if n is self.nil else 1+max(h(n.left),h(n.right))
        return h(self.root)
