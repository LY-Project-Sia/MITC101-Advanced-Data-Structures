"""Task 2: hand-built stack, circular queue, priority dispatch, doubly linked list."""
class Stack:
    def __init__(self): self._items=[]
    def push(self,x): self._items.append(x)
    def pop(self):
        if self.isEmpty(): raise IndexError("pop from empty stack")
        return self._items.pop()
    def peek(self):
        if self.isEmpty(): raise IndexError("peek at empty stack")
        return self._items[-1]
    def isEmpty(self): return not self._items
    def size(self): return len(self._items)
    def contents(self): return list(self._items)

class UndoRedo:
    def __init__(self, initial=None):
        self.state=list(initial or []); self.undo_stack=Stack(); self.redo_stack=Stack()
    def apply(self, action):
        self.undo_stack.push(list(self.state)); self.state.append(action); self.redo_stack=Stack()
    def undo(self):
        if self.undo_stack.isEmpty(): return False
        self.redo_stack.push(list(self.state)); self.state=self.undo_stack.pop(); return True
    def redo(self):
        if self.redo_stack.isEmpty(): return False
        self.undo_stack.push(list(self.state)); self.state=self.redo_stack.pop(); return True

class CircularQueue:
    def __init__(self, capacity):
        if capacity<=0: raise ValueError("capacity must be positive")
        self._a=[None]*capacity; self.capacity=capacity; self.head=0; self.tail=0; self.count=0
    def isEmpty(self): return self.count==0
    def isFull(self): return self.count==self.capacity
    def size(self): return self.count
    def enqueue(self,item):
        if self.isFull(): raise OverflowError("queue full")
        self._a[self.tail]=item; self.tail=(self.tail+1)%self.capacity; self.count+=1
    def dequeue(self):
        if self.isEmpty(): raise IndexError("dequeue from empty queue")
        x=self._a[self.head]; self._a[self.head]=None
        self.head=(self.head+1)%self.capacity; self.count-=1; return x
    def front(self):
        if self.isEmpty(): raise IndexError("front of empty queue")
        return self._a[self.head]
    def contents(self): return [self._a[(self.head+i)%self.capacity] for i in range(self.count)]

class PriorityDispatch:
    """Two FIFO queues preserve arrival order within Same-Day and Standard."""
    def __init__(self, capacity):
        self.same=CircularQueue(capacity); self.standard=CircularQueue(capacity)
    def enqueue(self, parcel, priority):
        (self.same if priority=="Same-Day" else self.standard).enqueue(parcel)
    def dequeue(self):
        if not self.same.isEmpty(): return self.same.dequeue()
        return self.standard.dequeue()

class Node:
    def __init__(self, key, value=None):
        self.key=key; self.value=value; self.prev=None; self.next=None
class DoublyLinkedList:
    def __init__(self): self.head=None; self.tail=None; self.count=0
    def insert_head(self,key,value=None):
        n=Node(key,value); n.next=self.head
        if self.head: self.head.prev=n
        else: self.tail=n
        self.head=n; self.count+=1
    def insert_tail(self,key,value=None):
        n=Node(key,value); n.prev=self.tail
        if self.tail: self.tail.next=n
        else: self.head=n
        self.tail=n; self.count+=1
    def search(self,key):
        n=self.head
        while n:
            if n.key==key:return n
            n=n.next
        return None
    def insert_after(self,target,key,value=None):
        cur=self.search(target)
        if cur is None:return False
        n=Node(key,value); n.prev=cur; n.next=cur.next
        if cur.next:cur.next.prev=n
        else:self.tail=n
        cur.next=n; self.count+=1; return True
    def delete(self,key):
        n=self.search(key)
        if n is None:return False
        if n.prev:n.prev.next=n.next
        else:self.head=n.next
        if n.next:n.next.prev=n.prev
        else:self.tail=n.prev
        self.count-=1; return True
    def forward(self):
        out=[]; n=self.head
        while n:out.append(n.key); n=n.next
        return out
    def backward(self):
        out=[]; n=self.tail
        while n:out.append(n.key); n=n.prev
        return out
    def reverse(self):
        n=self.head
        while n:
            n.prev,n.next=n.next,n.prev
            n=n.prev
        self.head,self.tail=self.tail,self.head
    def has_cycle(self):
        slow=fast=self.head
        while fast and fast.next:
            slow=slow.next; fast=fast.next.next
            if slow is fast:return True
        return False

if __name__=="__main__":
    S=7148; q= CircularQueue(20+(S%30))
    for i in range(12): q.enqueue(f"P{i:02}")
    for _ in range(8): q.dequeue()
    for i in range(12,20): q.enqueue(f"P{i:02}")
    print("Circular queue capacity:",q.capacity,"contents:",q.contents(),"head:",q.head,"tail:",q.tail)
    u=UndoRedo()
    for i in range(10+(S%10)):u.apply(f"ACTION-{i+1}")
    u.undo();u.undo();u.undo();u.redo()
    print("Undo/redo state size:",len(u.state),"undo depth:",u.undo_stack.size(),"redo depth:",u.redo_stack.size())
    ll=DoublyLinkedList()
    for x in ["P1","P2","P3"]:ll.insert_tail(x)
    ll.insert_after("P2","P2A"); print("Manifest:",ll.forward()); ll.reverse();print("Reversed:",ll.forward(),"cycle:",ll.has_cycle())
