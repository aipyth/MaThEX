import numpy as np
from copy import deepcopy


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


    def __init__(self, P):
        self.set_prod_rules(P)


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


    def set_prod_rules(self, prrules):
        self.P = prrules

        for nt in self.P:
            self.D.add(nt)

        if len(self.X) == 0:
            for nt in self.P:
                if type(self.P[nt]) == list:
                    for i in self.P[nt]:
                        for term in i:
                            if term not in self.D:
                                self.X.add(term)
                else:
                    for term in self.P[nt]:
                        if term not in self.D:
                            self.X.add(term)

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

    def get_nonterm_prod_rules(self):
        l = self.prod_rules_to_list()
        nonterm_rules = Set()
        for rule in l:
            if type(rule[1]) == list:
                for sub_right in rule[1]:
                    if type(sub_right) == tuple:
                        nonterm_rules.add((rule[0], sub_right))
            else:
                if type(rule[1]) == tuple:
                    nonterm_rules.add((rule[0], rule[1]))
        return nonterm_rules


    def CYK(self, w):
        """
        Cock-Younger-Kasami
        """
        n = len(w)
        N = len(self.D)
        Q = np.full((n, n, N), False, dtype=bool)
        for i in range(1, n+1):
            for j in range(1, N+1):
                if self.check_prod_rule((self.D[j-1], w[i-1])):
                    Q[0, i-1, j-1] = True
        for i in range(2, n+1):
            for j in range(1, n-i+2):
                for k in range(1, i):
                    for a in range(1, N+1):
                        for b in range(1, N+1):
                            for c in range(1, N+1):
                                if self.check_prod_rule((self.D[a-1], (self.D[b-1], self.D[c-1]))):
                                    if (Q[k-1, j-1, b-1] and Q[i-k-1, j+k-1, c-1]):
                                        Q[i-1, j-1, a-1] = True
        if Q[n-1, 0, 0]:
            return 'this word is producted by this grammar'
        else:
            return 'this word is not produced by this grammar'


    def CYK_recognizer(self, w):
        "Yakovliev Cock"
        N = len(self.D)
        n = len(w)
        Q = np.full((N, n, n), False, dtype=bool)

        for d in range(N):
            for i in range(n):
                Q[d, i, i] = 1 if self.check_prod_rule((self.D[d], w[i])) else 0

        for m in range(2, n+1):
            for i in range(1, n-m+2):
                j = i + m - 1
                for d in self.P:
                    produced = False
                    if type(self.P[d]) == list:
                        for ds in self.P[d]:
                            if type(ds) == tuple:
                                di = self.D.index(d)
                                d1 = self.D.index(ds[0])
                                d2 = self.D.index(ds[1])
                                for k in range(i, j):
                                    produced = produced or (Q[d1, i-1, k-1] and Q[d2, k, j-1])
                    elif type(self.P[d]) == tuple:
                        di = self.D.index(d)
                        d1 = self.D.index(self.P[d][0])
                        d2 = self.D.index(self.P[d][1])
                        for k in range(i, j):
                            produced = produced or (Q[d1, i-1, k-1] and Q[d2, k, j-1])
                    Q[self.D._nodes.index(d), i-1, j-1] = produced
        self.Q = Q
        return Q[0, 0, n-1]

    def CYK_parser(self, w):
        n = len(w)
        C = np.empty((n, n), dtype=Set)
        for i in range(n):
            for j in range(n):
                C[i, j] = Set()

        for d in self.P:
            for i in range(n):
                if self.check_prod_rule((d, w[i])):
                    C[i, 0].add((d, w[i]))

        # print(C)
        for l in range(1, n+1):
            for i in range(1, n+1):
                for d in self.get_nonterm_prod_rules():
                    print(d, l)
                    for l1 in range(1, l-1):
                        print(f"{l1=}")
                        # [0] in C_i,l1 && [1] in C_i+l1,l-l1
                        b = d[1][0]
                        c = d[1][1]

                        # print(d)
                        print(f"{b = }, {c = }")

                        f = False
                        # print(type(i), type(l1))
                        # print(C[0, 0])
                        for rule in C[i-1, l1-1]:
                            if b == rule[0]:
                                f = True
                        s = False
                        for rule in C[i+l1-1, l-l1-1]:
                            if c == rule[0]:
                                s = True
                        if f and s:
                            C[i-1, l-1].add(d)

                print()
        print(C)
        # nonterm_rules = self.get_nonterm_prod_rules()
        # for i in range(n):
        #     for j in range(n):
        #         for k in range(n):
        #
        #             for t1 in C[i, j]
        #             # for d in self.get_nonterm_prod_rules():


        print(C)



def main():
    g = Grammar(
        P={
            'd0': [('d1', 'd1'), ('d2', 'd3')],
            'd1': [('d1', 'd1'), ('d2', 'd3')],
            'd2': '(',
            'd3': [('d1', 'd4'), ')'],
            'd4': ')',
        }
    )

    print(f"{g.CYK_recognizer('()()')=}")
    # print(f"{g.CYKY(')()()()()')=}")

    # print(g.Q)
    print(g.CYK_parser('()'))
    # print(g.get_nonterm_prod_rules())





if __name__ == '__main__':
    main()
