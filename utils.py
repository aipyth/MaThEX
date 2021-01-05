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
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

    def __repr__(self):
        # prev = self.prev if self.prev else ''
        # next = self.prev if self.next else ''
        # return f"[node {prev}->({self.data})->{next} ]"
        return f"[node {self.data}]"


class Tree:
    def __init__(self):
        self.V = Set()
        self.E = Set()

    def __repr__(self):
        return f"Vertices: {self.V}\nEdges: {self.E}"


    def add_v(self, v):
        if type(v) == TreeNode:
            return self.V.add(v)
        else:
            return self.V.add(TreeNode(v))

    def add_e(self, a: TreeNode, b: TreeNode):
        a.next, b.prev = b, a
        self.E.add((a, b))



class Forest:
    pass


def main():
    t = Tree()
    a = t.add_v('a')
    b = t.add_v('b')
    t.add_e(a, b)

    print(t)

if __name__ == '__main__':
    main()
