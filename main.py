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


    def prod_rules_to_list(self):
        p = []
        for d in self.P:
            if type(self.P[d]) == list:
                for i in self.P[d]:
                    p.append((d, i))
            else:
                p.append((d, i))
        return p


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
                                    if (Q[k, j, b] and Q[i-k, j+k, c]):
                                        Q[i, j, a] = True
        if Q[n-1, 0, 0]:
            return 'this word is producted by this grammar'
        else:
            return 'this word is not produced by this grammar'


    def CYKY(self, w):
        "Yakovliev Cock"
        N = len(self.D)
        n = len(w)
        Q = np.full((N, n, n), False, dtype=bool)

        for d in range(N):
            for i in range(n):
                Q[d, i, i] = 1 if self.check_prod_rule((self.D[d], w[i])) else 0

        # print(f"0 - { n = }")
        # for m in range(1, n):
        #     print(f"1 - { m = }")
        #     for i in range(n-m+1):
        #         j = i + m - 1
        #         print(f"2 - { i = }, { j =}")
        #
        #         for d in range(N):
        #
        #             derived = False
        #             for d_der in self.P.get(self.D[d]):
        #                 # print(f"4 - { d_der = }, { derived = }")
        #                 for k in range(i, j):
        #                     print(f"5 - { k = }")
        #                     print(d_der)
        #             # Q[d, i, j] =


        for m in range(2, n+1):

            for i in range(1, n-m+2):
                j = i + m - 1
                nonterm_prod_rules = list(filter(
                    lambda x: type(x[1]) == tuple,
                    self.prod_rules_to_list()))
                for d in nonterm_prod_rules:
                    di = self.D._nodes.index(d[0])
                    d1 = self.D._nodes.index(d[1][0])
                    d2 = self.D._nodes.index(d[1][1])
                    # print(di, d1, d2)
                    for k in range(i, j):
                        # Q[d, i-1, j-1] = Q[d1, i-1, k-1] and Q[d2, k, j-1]
                        print(f"{di=}")
                        print(f"{d1=}, {d2=}, {i=}, {j=}, {k=}")
                        print(f"{Q[d1, i-1, k-1]=}, {Q[d2, k-1, j-1]=}, {Q[d1, i-1, k-1] and Q[d2, k-1, j-1] = }")
                        print()
                        # Q[d, i, j] = Q[d1, i, k] and Q[d2, k, j]


                # for d in range(N):
                #     derived = False

                    # right = self.P.get(self.D[d])
                    # print(right)


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
        'd1': [('d1', 'd1'), ('d2', 'd3')],
        'd2': '(',
        'd3': [('d1' , 'd4'), ')'],
        'd4': ')'
    })

    # print( g.check_prod_rule( ('d0', ('d2', 'd1')) ) )

    print(g.CYK('()'))
    # print(g.prod_rules_to_list())


if __name__ == '__main__':
    main()
