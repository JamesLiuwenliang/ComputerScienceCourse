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
            self.tail = self.head = None

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

# LFU缓存置换算法中将使用频率相同的节点存放在同一个链表中,
# 所以LFUCache上是可能存在多个链表的

class LFUNode(Node):
    def __init__(self,key,value):
        self.freq = 0
        super(LFUNode ,self).__init__(key,value)

class LFUCache(object):

    def __init__(self, capacity):
        self.capacity = capacity;
        self.size = 0;
        self.map = {}
        # key : 频率 ,value : 频率对应的双向链表
        self.freq_map = {}

    # 更新节点频率的操作
    def __update_freq(self, node):
        freq = node.freq

        # 将要更新的节点从原来的freq链表中取出,
        # 如果该freq链表中没有节点了,就删除这个频率(freq)的链表
        node = self.freq_map[freq].remove(node)
        if self.freq_map[freq].size == 0:
            del self.freq_map[freq]

        # 更新
        freq += 1
        node.freq = freq
        if freq not in self.freq_map:
            self.freq_map[freq] = DoubleLinkedList()
        self.freq_map[freq].append(node)

    def get(self, key):
        if key not in self.map:
            return -1 
        node = self.map.get(key)
        self.__update_freq(node)
        return node.value

    def put(self,key,value):
        if self.capacity == 0:
            return 
        
        # 缓存命中
        if key in self.map:
            node = self.map.gett(key)
            node.value = value 
            self.__update_freq(node)
        # 缓存没有命中
        else:
            # 判断缓存是否满了,将存放频率最低的节点的map全部删除
            if self.capacity == self.size :
                min_freq = min(self.freq_map)
                node = self.freq_map[min_freq].pop()
                del self.map[node.key]
                self.size -= 1 

            # 建立相应频率的节点
            node = LFUNode(key,value)
            node.freq = 1
            self.map[key] = node
            if node.freq not in self.freq_map:
                self.freq_map[node.freq] = DoubleLinkedList()
            node = self.freq_map[node.freq].append(node)            
            self.size += 1
            
    def print(self):
        print('*************************')
        for k,v in self.freq_map.items():
            print('Freq = %d' % k)
            self.freq_map[k].print()
        print('*************************')
        print()

        

if __name__ == '__main__':
    cache = LFUCache(3)
    cache.put(1, 1)
    cache.print()
    cache.put(2, 2)
    cache.print()
    print(cache.get(1))
    cache.print()
    cache.put(3, 3)
    cache.print()
    print(cache.get(2))
    cache.print()
    print(cache.get(3))
    cache.print()
    cache.put(4, 4)
    cache.print()
    print(cache.get(1))
    cache.print()
    print(cache.get(3))
    cache.print()
    print(cache.get(4))
    cache.print()