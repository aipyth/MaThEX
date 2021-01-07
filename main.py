from grammar import Grammar, turn_to_HomskyForm, compile_rules


if __name__ == "__main__":
    rules = compile_rules("""
        Function -> Variable|Digit|( Function )|Function Function|Function Operator Function|FuncName Function
        Digit -> 0|1|2|3|4|5|6|7|8|9|Digit Digit
        Operator -> +|-|*|/|%|=
        Variable -> q|w|e|r|t|y|u|i|o|p|a|s|d|f|g|h|j|k|l|z|x|c|v|b|n|m|alpha|beta|gamma|phi|theta
        FuncName -> sin|cos|tan|ctan|log|ln|exp
        """)
    # print(rules)
    meth = Grammar(
        X={'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '=', '%', '(', ')', 'log', 'exp', 'sin', 'cos', 'tan', 'ctan', 'ln', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'alpha', 'beta', 'gamma', 'phi', 'theta'},
        D={'Function', 'Digit', 'Operator', 'Variable', 'FuncName'},
        acsiom='Function',
        P=rules,
    )
    meth = turn_to_HomskyForm(meth)
    print(meth)

    # Parsing
    # while (True):
    #     eq = input()
    #     print(meth.CYK_parser(eq))

    # Recognizing
    while(True):
        eq = input()
        print("Recognized" if meth.CYK_recognizer(eq) else "Not recognized")