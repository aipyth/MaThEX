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
        rr = []
        for d in self.P:
            s = []
            for ds in self.P[d]:
                if type(ds) == tuple:
                    s.append(' '.join(tuple(map(str, ds))))
                else:
                    s.append(str(ds))
            rr.append('\t' + str(d) + ' -> ' + ' | '.join(s))
        rules = '\n'.join(rr)


        return f"<Grammar>:\nTerminal symbols: {self.X}\nNonterminal symbols: {self.D}\nAcsiom: {self.acsiom}\nRules:\n{rules}"



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
            return rule[1] in ruled


    def prod_rules_to_list(self):
        p = []
        for d in self.P:
            for i in self.P[d]:
                p.append((d, i))
        return p

    def get_nonterm_prod_rules(self):
        "Works with CNF"
        return list(filter(lambda x: len(x[1]) == 2, self.prod_rules_to_list()))


    def CYK_recognizer(self, w, ret_matrix=False):
        "Yakovliev Cock"
        N = len(self.D)
        n = len(w)
        Q = np.full((N, n, n), False, dtype=bool)

        for d in range(N):
            for i in range(n):
                # for k in range(0, n-i, -1):
                for k in range(n-i):
                    Q[d, i, i+k] = self.check_prod_rule((self.D[d], w[i:i+k+1]))

        for m in range(2, n+1):
            for i in range(1, n-m+2):
                j = i + m - 1
                for d in self.P:
                    produced = False
                    for ds in self.P[d]:
                        # we check if this is nonterm rule
                        if type(ds) == tuple:
                            di = self.D.index(d)
                            d1 = self.D.index(ds[0])
                            d2 = self.D.index(ds[1])
                            for k in range(i, j):
                                produced = produced or (Q[d1, i-1, k-1] and Q[d2, k, j-1])
                    Q[self.D.index(d), i-1, j-1] = Q[self.D.index(d), i-1, j-1] or produced
        if ret_matrix:
            return Q, Q[self.D.index(self.acsiom), 0, n-1]
        else: return Q[self.D.index(self.acsiom), 0, n-1]

    def CYK_parser(self, w):
        n = len(w)
        C = np.empty((n, n), dtype=Set)
        for i in range(n):
            for j in range(n):
                C[i, j] = Set()

        for d in self.P:
            for i in range(n):
                # for k in range(0, n-i, -1):
                for k in range(n-i):
                    if self.check_prod_rule((d, w[i:i+k+1])):
                        C[i, i+k].add(d)

        for m in range(2, n+1):
            for i in range(1, n-m+2):
                j = i + m - 1
                for rule in self.get_nonterm_prod_rules():
                    for k in range(i, j):
                        lrule, rrule = rule[1][0], rule[1][1]
                        if lrule in C[i-1, k-1] and rrule in C[k, j-1]:
                            C[i-1, j-1].add(rule[0])
        return C


def turn_to_HomskyForm(gramm):
    # creating new grammar as copy of argument in Homsky form:
    new_grammar = gramm
    #1) delete long rules:
    for j in range(len(new_grammar.P)):
        keys_list = list(new_grammar.P)
        rules = new_grammar.P[keys_list[j]]
        for m in range(len(rules)):
            if type(rules[m]) == tuple and len(rules[m]) > 2:
                k = len(rules[m])
                for i in range(1, k-2):
                    newNonTerminal = chr(65+j) + str(i+m)
                    new_grammar.D.add(newNonTerminal)
                    new_grammar.D.add(chr(65+j) + str(i+1+m))
                    new_grammar.P[newNonTerminal] = [(rules[m][i], chr(65+j) + str(i+1))]
                newlastNonTerminal = chr(65+j) + str(k-2+m)
                new_grammar.P[newlastNonTerminal] = [((rules[m][k-2]), (rules[m][k-1]))]
                new_grammar.D.add(newlastNonTerminal)
                rules.append((rules[m][0], chr(65+j) + str(1+m)))
                rules.remove(rules[m])

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
                if type(rule) == tuple:
                    if rule[0] in S and rule[1] in S:
                        s.add(element)
                else:
                    if rule in S:
                        s.add(element)
        if s == S:
            break
    #now Eliminate them!
    new_P = new_grammar.P
    for element in new_P.copy():
        rules = new_P[element]
        for rule in rules:
            if type(rule) == tuple:
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
    # # # 3) delete the chain prod rules:
    # # # to find unit pairs:
    def unit_pairs_set(D, P):
        the_set = list((i, i) for i in D)
        for element in P:
            for rule in P[element]:
                if rule in D:
                    for item in the_set:
                        if item[1] == element and (item[0], rule[0]) not in the_set:
                            if type(rule) == tuple:
                                the_set.append((item[0], rule[0]))
                            else:
                                the_set.append((item[0], rule))
        return the_set
    pairs_set = unit_pairs_set(new_grammar.D, new_grammar.P)
    # print(pairs_set)
    for pair in pairs_set:
        if pair[0] != pair[1]:
            # tupl = list()
            # tupl.append(pair[1])
            # tupl = tuple(tupl)
            # print(pair)
            new_grammar.P[pair[0]].remove(pair[1])
            new_grammar.P[pair[0]] = new_grammar.P[pair[0]] + new_grammar.P[pair[1]]
            new_grammar.P[pair[0]] = list(set(new_grammar.P[pair[0]]))
    for element in new_grammar.P:
        for rule in new_grammar.P[element]:
            if type(rule) == tuple and len(rule) == 1:
                new_grammar.P[element][new_grammar.P[element].index(rule)] = rule[0]
    # # #4) delete useless elems:
    # #
    # # # delete non-generating non-terms
    set_of_generatings = set()
    set_of_generatings.add(new_grammar.acsiom)
    for element in new_grammar.P:
        for rule in new_grammar.P[element]:
            if type(rule) == tuple:
                # print(rule)
                if rule[0] not in new_grammar.D and rule[1] not in new_grammar.D:
                        set_of_generatings.add(element)
            else:
                if rule not in new_grammar.D:
                        set_of_generatings.add(element)
    while True:
        s = set_of_generatings
        for element in new_grammar.P:
            for rule in new_grammar.P[element]:
                if type(rule) == tuple:
                    if (rule[0] in set_of_generatings or rule[0] in new_grammar.X) and (rule[1] in set_of_generatings or rule[1] in new_grammar.X):
                        s.add(element)
                else:
                    if rule in set_of_generatings:
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
                if type(rule) == tuple:
                    for term in rule:
                        if term in new_grammar.D:
                            found_elements.add(term)
                else:
                    if rule in new_grammar.D:
                        found_elements.add(term)

    #delete them all!
    for element in new_grammar.P:
        for rule in new_grammar.P[element]:
            if type(rule) == tuple:
                for term in rule:
                    if term not in set_of_generatings and term in new_grammar.D:
                        new_list = list(rule)
                        new_list.remove(term)
                        new_grammar.P[element].remove(rule)
                        if not(len(new_list) == 1 and new_list[0] == element):
                            new_grammar.P[element].append(new_list[0])
            else:
                if rule not in set_of_generatings and rule in new_grammar.D:
                    new_grammar.P[element].remove(rule)

    for element in new_grammar.P.copy():
        if element not in found_elements:
            del new_grammar.P[element]
    # # #last shtrikh:
    for item in new_grammar.X:
        S1 = 'Z' + str(new_grammar.X.index(item))
        for element in new_grammar.P.copy():
            for rule in new_grammar.P[element]:
                if type(rule) == tuple and item in rule and len(rule) > 1:
                    new_list = list(rule)
                    for i in range(2):
                        if rule[i] == item:
                            new_list[i] = S1
                            new_grammar.D.add(S1)
                    new_grammar.P[element][new_grammar.P[element].index(rule)] = tuple(new_list)
                    new_grammar.P[S1] = [item]
    return new_grammar

def compile_rules(s : str):
    """
    Compile rules to dictionary of list of rules
    acsiom -> nt1 nt2 | nt2 nt2
    nt2 -> ( nt2 ) | eps
    nt2 -> eps
    """
    ss = s.split('\n')
    rules = {}
    for srules in ss:
        arrow_index = srules.find('->')
        left_nonterm = srules[:arrow_index].strip()
        right_derivs = list(map(lambda x: x.strip(), srules[arrow_index+2:].strip().split('|')))
        if left_nonterm != '' and len(right_derivs) != 0 and right_derivs[0] != '':
            right_derivs = list(map(lambda x: tuple(x.split(' ')), right_derivs))
            right_derivs = list(map(lambda x: x[0] if len(x) == 1 else x, right_derivs))
            rules[left_nonterm] = right_derivs
    return rules



def main():
    # g = Grammar(
    #     X={"aa", "bb"},
    #     D={'d0', 'd1', 'd2', 'd3', 'd4'},
    #     acsiom='d0',
    #     P={
    #         'd0': [('d1', 'd1'), ('d2', 'd3')],
    #         'd1': [('d1', 'd1'), ('d2', 'd3')],
    #         'd2': [('aa')],
    #         'd3': [('d1', 'd4'), 'bb'],
    #         'd4': [('bb')],
    #     }
    # )
    # print(g.CYK_recognizer("aabb"))
    arithm = Grammar(
        X = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '=', '(', ')', 'log', 'exp', 'sin', 'cos'},
        D = { 'Dig', 'Opr', 'For', 'Fun', 'Nam'},
        acsiom ='For',
        P={
          'Dig': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ('Dig', 'Dig')],
          'Opr': ['+', '-', '*', '/', '='],
          'For': [('For', 'Opr', 'For'), 'Fun'],
          'Fun': ['Dig', ('(', 'Fun', ')'), ('Nam', 'Fun'), ('Fun', 'Opr', 'Fun')],
          'Nam': ['log', 'exp', 'sin', 'cos']
   })

    G = turn_to_HomskyForm(arithm)
    # print(G)
    print(G.CYK_recognizer('log(2)+2'))




if __name__ == '__main__':
    main()
