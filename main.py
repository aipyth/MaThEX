import numpy as np


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


    def add(self, item):
        if item not in self._nodes:
            self._nodes.append(item)
        else:
            return False
        return True


    def remove(self, item):
        self._nodes.remove(item)



class Grammar:
    X = Set()   # set of terminal symbols
    D = Set()   # set of non-terminal symbols
    acsiom = None  # acsiom
    P = {}   # set of production rules


    def __init__(self):
        pass


    def add_terminal_symbols(self, *tsymb):
        for i in tsymb:
            self.X.add(i)


    def add_nonterminal_symbols(self, *ntsymb):
        for i in ntsymb:
            self.D.add(i)


    def set_acsiom(self, acs):
        if acs in self.D:
            self.acsiom = acs
        else:
            return False
        return True


    def set_ProdRules(self, prrules):
        self.P = prrules

    def check_prod_rule(self, rule):
        ruled = self.P.get(rule[0])
        if not ruled:
            return False
        else:
            if type(ruled) == list:
                return rule[1] in ruled
            return rule[1] == ruled

    def CYK(self, w):
        """
        Cock-Younger-Kasami
        """
        n = len(w)
        N = len(self.D)
        Q = np.full((n, n, N), False, dtype=bool)
        for i in range(n):
            for j in range(N):
                if self.check_prod_rule((self.D[j], w[i])):
                    Q[0, i, j] = True
        for i in range(1, n):
            for j in range(n-i+1):
                for k in range(i-1):
                    for a in range(N):
                        for b in range(N):
                            for c in range(N):
                                if self.check_prod_rule((self.D[a], (self.D[b], self.D[c]))):
                                    if Q[k, j, b] and Q[i-k, j+k, c]:
                                        Q[i, j, a] = True
        if Q[n-1, 0, 0]:
            return 'this word is producted by this grammar'
        else:
            return 'this word is not produced by this grammar'


    def CYKY(self, w):
        "Yakovliev Cock"
        N = len(self.D)
        n = len(w)
        Q = np.empty((N, n, n))
        # Pkeys = self.P.keys()

        for d in N:
            for i in range(N):
                Q[d, i, i] = 1 if self.check_prod_rule((self.D[d], w[i])) else 0

        print(Q)


def main():
    # s = Set()
    # s.add(1)
    # print(1 in s)
    g = Grammar()
    g.add_terminal_symbols('(', ')')
    g.add_nonterminal_symbols('d0', 'd1', 'd2', 'd3', 'd4')
    g.set_acsiom('d0')
    g.set_ProdRules({
        # d0 -> d1 d1 | d2 d3
        'd0': [('d1', 'd1'), ('d2', 'd3')],
        #d1 -> d1 d1 | d2 d2
        'd1': [('d1', 'd1'), ('d2', 'd2')],
        'd2': '(',
        'd3': [('d1' , 'd4'), ')'],
        'd4': ')'
    })

    # print( g.check_prod_rule( ('d0', ('d2', 'd1')) ) )

    print(g.CYK('()'))

if __name__ == '__main__':
    main()
