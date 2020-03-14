#! _*_ encoding=utf-8 _*_

class Node :
    def __init__ (self,key,value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def __str__(self):
        val = '{%d: %d}' % (self.key, self.value)
        return val

    def __repr__(self):
        val = '{%d: %d}' % (self.key, self.value)
        return val

class DoubleLinkedList :
    def __init__(self,capacity = 0xffff):
        self.capacity = capacity
        self.head = None
        self.tail = None
        self.size = 0

    # 从头部添加 , self.head是一个指针
    def __add_head(self, node):
        if not self.head:
            self.head = node
            self.tail = node
            self.head.next = None
            self.head.prev = None
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node 
            self.head.prev = None 
        
        self.size +=1
        return node

    def __add_tail(self,node):
        if not self.tail:
            self.tail = node
            self.head = node
            node.next = None
            node.tail = None
        else:
            node.prev = self.tail
            self.tail.next = node
            node.next = None
            self.tail = node
        self.size += 1
        return node

    # 从尾部删除
    def __del_tail(self):
        if not self.head:
            return
        
        node = self.tail

        if node.prev: 
            self.tail = node.prev
            self.tail.next = None
        else:
            self.tail = self.head = None

        self.size -= 1
        return node

    # 从头部删除
    def __del_head(self):
        if not self.head:
            return

        node = self.head
        if node.next:
            self.head = self.head.next
            self.head.prev = None
        else:
            self.tail = sel.head = None

        self.size -= 1
        return node

    def __delete (self ,node):
        # 如果node = None ,默认删除尾部节点
        if not node:
            node= self.tail

        # 先判断是尾部节点还是头部节点
        if node == self.tail:
            self.__del_tail()
        elif node == self.head:
            self.__del_head()
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            self.size -= 1
        return node

    # 弹出头部节点
    def pop(self):
        return self.__del_head()

    # 添加节点
    def append(self, node):
        return self.__add_tail(node)

    # 往头部添加节点
    def append_front(self ,node):
        return self.__add_head(node)
    
    # 删除节点
    def remove(self,node = None):
        return self.__delete(node)

    def print(self):
        p = self.head
        line = ' '
        while p:
            line += '%s' % (p)
            p = p.next
            if p:
                line += '->'
        print(line)



class LRUCache(object):
    def __init__(self,capacity):
        self.capacity = capacity;
        self.size = 0;
        self.map = {}
        self.list = DoubleLinkedList(self.capacity)

    def get(self,key):
        if key not in self.map:
            return -1
        else:
            node = self.map.get(key)
            self.list.remove(node)
            self.list.append_front(node)
            return node.value

    def put(self,key,value):

        # 节点在Cache中 : 找到节点并更新节点值,节点会进入最前面的位置
        if key in self.map:
            node = self.map.get(key)
            self.list.remove(node)
            node.value = value
            self.list.append_front(node)
        # 节点不在Cache中,需要添加节点
        else:  
            
            node = Node(key,value)

            # 需要考虑缓存满否
            if(self.list.size >= self.list.capacity):
                old_node = self.list.remove()
                self.map.pop(old_node.key)

            self.list.append_front(node)
            self.map[key] = node
    
    def print(self):
        self.list.print()

if __name__ == '__main__':
    cache = LRUCache(2)
    cache.put(2, 2)
    cache.print()
    cache.put(1, 1)
    cache.print()
    cache.put(3, 3)
    cache.print()

    print(cache.get(1))
    cache.print()
    print(cache.get(2))
    cache.print()

    print(cache.get(3))
    cache.print()