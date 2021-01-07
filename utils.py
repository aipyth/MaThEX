from uuid import uuid4

class Set:
    def __init__(self):
        self._nodes = []


    def __repr__(self):
        str_nodes = list(map(str, self._nodes))
        return '{ ' + ', '.join(str_nodes) + ' }'


    def __iter__(self):
        return iter(self._nodes)


    def __len__(self):
        return len(self._nodes)


    def __getitem__(self, item):
        return self._nodes[item]


    def __add__(self, obj):
        s = Set()
        s._nodes = deepcopy(self._nodes)
        for item in obj:
            s.add(item)
        return s


    def index(self, item):
        return self._nodes.index(item)


    def add(self, item):
        if item not in self._nodes:
            self._nodes.append(item)
        return item


    def remove(self, item):
        self._nodes.remove(item)


class TreeNode:
    def __init__(self, data=None, next=None, prev=None, id=None):
        self.data = data
        self.next = next
        self.prev = prev
        self.id = id if id else uuid4()

    def __repr__(self):
        prev = f"({self.prev.id}, {self.prev.data})" if self.prev else ''
        next = f"({self.next.id}, {self.next.data})" if self.next else ''
        return f"[node {prev}->({self.id, self.data})->{next} ]"
        # return f"[node {self.id} \"{self.data}\"]"

    def __eq__(self, obj):
        return self.id == obj.id


class Tree:
    def __init__(self):
        self.V = Set()
        self.E = Set()

    def __repr__(self):
        return f"Vertexes: {self.V}\nEdges: {self.E}"


    def add_vertex(self, v, next=None, prev=None, id=None):
        if type(v) == TreeNode:
            return self.V.add(v)
        else:
            return self.V.add(TreeNode(v, next, prev, id))

    def add_edge(self, a: TreeNode, b: TreeNode):
        a.next, b.prev = b, a
        self.E.add((a, b))



class Forest:
    pass


def main():
    t = Tree()
    a = t.add_vertex('a', id=1)
    a1 = t.add_vertex('a', id=4)
    b = t.add_vertex('b')
    t.add_edge(a, b)
    t.add_edge(b, a1)

    print(t)

    print("node a: ", a)

if __name__ == '__main__':
    main()
