import numpy as np
from copy import deepcopy

from utils import Set


class Grammar:
    def __init__(self, X={}, D={}, acsiom=None, P={}):
        self.X = Set()
        self.D = Set()
        self.add_terminal_symbols(X)
        self.add_nonterminal_symbols(D)
        self.set_acsiom(acsiom)
        self.set_prod_rules(P)


    def __repr__(self):
        pass
        # rr = []
        # rules = 


        # return f"Grammar: {self.__name__}\nTerminal symbols: {self.X}\n/
        # Nonterminal symbols: {self.D}\nAcsiom: {self.acsiom}\nRules: {rules}"



    def add_terminal_symbols(self, tsymb: set):
        for i in tsymb:
            self.X.add(i)


    def add_nonterminal_symbols(self, ntsymb: set):
        for i in ntsymb:
            self.D.add(i)


    def set_acsiom(self, acs):
        self.acsiom = acs if acs in self.D else None
        return self.acsiom


    def set_prod_rules(self, prrules, auto_set_symbols=False):
        self.P = prrules

        if len(self.D) == 0:
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
            for i in self.P[d]:
                p.append((d, i))
        return p

    def get_nonterm_prod_rules(self):
        "Works with CNF"
        return list(filter(lambda x: len(x[1]) == 2, self.prod_rules_to_list()))


    def CYK(self, w):
        """
        Cock-Younger-Kasami
        """
        # TODO: rework with new set of writing product rules or just delete this
        # TODO: DELETE THIS
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
                    for element in self.P:
                        a = int(element[1])
                        for kortezh in self.P[element]:
                            if type(kortezh) is tuple:
                                b = int(kortezh[0][1])
                                c = int(kortezh[1][1])
                                if (Q[k-1, j-1, b] and Q[i-k-1, j+k-1, c]):
                                    Q[i-1, j-1, a] = True
        if Q[n-1, 0, 0]:
            return 'this word is produced by this grammar'
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
                    for ds in self.P[d]:
                        # we check if this is nonterm rule
                        if len(ds) == 2:
                            di = self.D.index(d)
                            d1 = self.D.index(ds[0])
                            d2 = self.D.index(ds[1])
                            for k in range(i, j):
                                produced = produced or (Q[d1, i-1, k-1] and Q[d2, k, j-1])
                    Q[self.D._nodes.index(d), i-1, j-1] = produced
        return Q, Q[0, 0, n-1]

    def CYK_parser(self, w):
        n = len(w)
        C = np.empty((n, n), dtype=Set)
        for i in range(n):
            for j in range(n):
                C[i, j] = Set()

        for d in self.P:
            for i in range(n):
                if self.check_prod_rule((d, w[i])):
                    C[i, i].add(d)

        for m in range(2, n+1):
            for i in range(1, n-m+2):
                j = i + m - 1
                for rule in self.get_nonterm_prod_rules():
                    for k in range(i, j):
                        lrule, rrule = rule[1][0], rule[1][1]
                        if lrule in C[i-1, k-1] and rrule in C[k, j-1]:
                            C[i-1, j-1].add(rule[0])
        return C

    
    # def CYK_recognizer_modified(self, w):



def turn_to_HomskyForm(gramm):
    # creating new grammar as copy of argument in Homsky form:
    new_grammar = gramm
    #1) delete long rules:
    for j in range(len(new_grammar.P)):
        keys_list = list(new_grammar.P)
        rules = new_grammar.P[keys_list[j]]
        for rule in rules:
            if len(rule) > 2 and rule != 'eps':
                k = len(rule)
                for i in range(1, k-2):
                    newNonTerminal = chr(65+j) + str(i)
                    new_grammar.D.add(newNonTerminal)
                    new_grammar.P[newNonTerminal] = [(rule[i], chr(65+j) + str(i+1))]
                newlastNonTerminal = chr(65+j) + str(k-2)
                new_grammar.P[newlastNonTerminal] = [((rule[k-2]), (rule[k-1]))]
                new_grammar.D.add(newlastNonTerminal)
                rules.append((rule[0], chr(65+j) + str(1)))
                rules.remove(rule)

    # 2) delete epsilon-rules:
    # to find rules A => eps:
    S = Set() #set of espilon non-Terms
    for element in new_grammar.P.copy():
        for rule in new_grammar.P[element]:
            if rule == 'eps':
                S.add(element)
    s = S
    while True:
        S = s
        for element in new_grammar.P.copy():
            for rule in new_grammar.P[element]:
                if len(rule) == 2:
                    if rule[0] in S and rule[1] in S:
                        s.add(element)
                if len(rule) == 1:
                    if rule[0] in S:
                        s.add(element)
        if s == S:
            break
    #now Eliminate them!
    new_P = new_grammar.P
    for element in new_P.copy():
        rules = new_P[element]
        for rule in rules:
            for symbol in rule:
                if symbol in S and len(rule) > 1:
                    temp = list(rule)
                    temp.remove(symbol)
                    new_rule = tuple(temp)
                    rules.append(new_rule)

        delete_reps = set(rules)
        new_P[element] = list(delete_reps)
    for element in new_P.copy():
        if 'eps' in new_P[element]:
            new_P[element].remove('eps')
        if new_P[element] == []:
            del new_P[element]
    new_grammar.P = new_P
    #
    # # 3) delete the chain prod rules:
    # # to find unit pairs:
    def unit_pairs_set(D, P):
        the_set = list((i, i) for i in D)
        for element in P:
            for rule in P[element]:
                if len(rule) == 1 and rule[0] in D:
                    for item in the_set:
                        if item[1] == element and (item[0], rule[0]) not in the_set:
                            the_set.append((item[0], rule[0]))
        return the_set
    pairs_set = unit_pairs_set(new_grammar.D, new_grammar.P)
    for pair in pairs_set:
        if pair[0] != pair[1]:
            tupl = list()
            tupl.append(pair[1])
            tupl = tuple(tupl)
            new_grammar.P[pair[0]].remove(tupl)
            new_grammar.P[pair[0]] = new_grammar.P[pair[0]] + new_grammar.P[pair[1]]
            new_grammar.P[pair[0]] = list(set(new_grammar.P[pair[0]]))

    # #4) delete useless elems:
    #
    # # delete non-generating non-terms
    set_of_generatings = set()
    set_of_generatings.add(new_grammar.acsiom)
    for element in new_grammar.P:
        for rule in new_grammar.P[element]:
            if len(rule) > 1:
                if rule[0] not in new_grammar.D and rule[1] not in new_grammar.D:
                        set_of_generatings.add(element)
            if len(rule) == 1:
                if rule[0] not in new_grammar.D:
                        set_of_generatings.add(element)
    while True:
        s = set_of_generatings
        for element in new_grammar.P:
            for rule in new_grammar.P[element]:
                if len(rule) > 1:
                    if rule[0] in set_of_generatings and rule[1] in set_of_generatings:
                        s.add(element)
                else:
                    if rule[0] in set_of_generatings:
                        s.add(element)
        if s == set_of_generatings:
            break
    #delete ureachable non-Terms
    #algorithm of search
    found_elements = Set()
    found_elements.add(new_grammar.acsiom)
    for item in found_elements:
        if item in new_grammar.P:
            for rule in new_grammar.P[item]:
                for term in rule:
                    if term in new_grammar.D:
                        found_elements.add(term)

    #delete them all!
    for element in new_grammar.P:
        for rule in new_grammar.P[element]:
            for term in rule:
                if term not in set_of_generatings and term in new_grammar.D:
                    new_list = list(rule)
                    new_list.remove(term)
                    new_grammar.P[element].remove(rule)
                    if not(len(new_list) == 1 and new_list[0] == element):
                        new_grammar.P[element].append(tuple(new_list))
    for element in new_grammar.P.copy():
        if element not in found_elements:
            del new_grammar.P[element]

    # # #last shtrikh:
    for item in new_grammar.X:
        S1 = 'Z' + str(new_grammar.X.index(item))
        for element in new_grammar.P.copy():
            for rule in new_grammar.P[element]:
                if len(rule) == 2 and item in rule:
                    new_list = list(rule)
                    for i in range(2):
                        if rule[i] == item:
                            new_list[i] = S1
                    new_grammar.P[element][new_grammar.P[element].index(rule)] = tuple(new_list)

        new_grammar.P[S1] = [(item)]

    return new_grammar

def main():
    g = Grammar(
        P={
            'd0': [('d1', 'd1'), ('d2', 'd3')],
            'd1': [('d1', 'd1'), ('d2', 'd3')],
            'd2': [('(')],
            'd3': [('d1', 'd4'), ')'],
            'd4': [(')')],
        }
    )
    # g = Grammar(

    #     X = {'(', ')'},
    #     D = {'d0'},
    #     acsiom = 'd0',
    #     P = {
    #         'd0': [('(', 'd0', ')'), ('d0', 'd0'), 'eps'],

    #     }
    # )

    # print(f"{g.CYK_recognizer('()(()())()')=}")
    print(f"{g.CYK_recognizer('()()')=}")
    # print(f"{g.CYKY(')()()()()')=}")

    # print(g.Q)
    # print(g.CYK_parser('(()()())'))
    # print(g.get_nonterm_prod_rules())
    # print(g.prod_rules_to_list())
    # print(g.get_nonterm_prod_rules())
    # print(turn_to_HomskyForm(g).P)

    # arithm = Grammar(P={
    #     'digit': [(0), (1), (2), (3), (4), (5), (6), (7), (8), (9), ('digit', 'digit')],
    #     'oper': [('+'), ('-'), ('*'), ('/')],
    #     'formula': [('digit', 'f1')],
    #     'f1': [('oper', 'digit')],
    # })
    # print(arithm.D)
    # print(arithm.X)
    # print(arithm.CYK_recognizer('8+9'))

    # G = turn_to_HomskyForm(g)
    # G.CYK_recognizer('()()')



if __name__ == '__main__':
    main()
