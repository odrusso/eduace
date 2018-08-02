from sympy import *
from sympy.parsing.sympy_parser import standard_transformations, split_symbols, implicit_multiplication_application, convert_xor, parse_expr


def remove_left_right(s):
    s = s.replace(r"\left", "")
    s = s.replace(r"\right", "")
    return s


def decompose_frac(s):
    """Please don't touch this .... You have been warned!
    Removes \frac latex elements from a string and turns them into infix-happy elements hopefully
    """
    k = []
    itt = 0

    while "\\frac" in s:
        if itt >= len(s):
            itt = 0
        if s[itt] == "\\":
            if s[itt+1 : itt+5] == "frac":
                # print("Running fraction decomp on %s" % s)
                o = ["", ""]
                o_itt = 0
                current = itt + 6

                k.append("{")
                while len(k) > 0:
                    # print("K: %s, O: %s, o_itt: %s, current: %s" % (k, o, o_itt, current))
                    if s[current] == "{":
                        k.append("{")
                        o[o_itt] += "{"
                    elif s[current] == "}":
                        k.pop()
                        if len(k) != 0:
                            o[o_itt] += "}"
                    else:
                        o[o_itt] += s[current]
                    current += 1

                o_itt += 1

                current += 1

                k.append("{")
                while len(k) > 0:
                    # print("K: %s, O: %s, o_itt: %s, current: %s" % (k, o, o_itt, current))
                    if s[current] == "{":
                        k.append("{")
                        o[o_itt] += "{"
                    elif s[current] == "}":
                        k.pop()
                        if len(k) != 0:
                            o[o_itt] += "}"
                    else:
                        o[o_itt] += s[current]
                    current += 1

                new_s = s[0:itt] + "(%s)/(%s)" % (o[0], o[1]) + s[current:]
                s = new_s

        itt += 1
    return s


def decompose_surds(s):
    """Please don't touch this .... You have been warned!
        Removes \sqrt latex elements from a string and turns them into infix-happy elements hopefully
        Should work in the form of both \sqrt{expression} and \sqrt{base}{expression}
        Will replace these sections with (expression)^(1/base)
    """
    k = []
    itt = 0

    while "\\sqrt" in s:

        if itt >= len(s): #reset the itt counter if reached end. Allows while loop to function multiple times.
            itt = 0


        if s[itt] == "\\": #delimiter for LaTeX
            if s[itt+1 : itt+5] == "sqrt": #Checks to see function is sqrt
                # print("Running fraction decomp on %s" % s)
                o = ["", ""]
                current = itt + 6

                k.append("{")
                while len(k) > 0:
                    # print("K: %s, O: %s, o_itt: %s, current: %s" % (k, o, o_itt, current))
                    if s[current] == "{":
                        k.append("{")
                        o[0] += "{"
                    elif s[current] == "}":
                        k.pop()
                        if len(k) != 0:
                            o[0] += "}"
                    else:
                        o[0] += s[current]
                    current += 1
                if current < len(s):
                    if s[current] == "{":
                        current += 1
                        k.append("{")
                        while len(k) > 0:
                            # print("K: %s, O: %s, o_itt: %s, current: %s" % (k, o, o_itt, current))
                            if s[current] == "{":
                                k.append("{")
                                o[1] += "{"
                            elif s[current] == "}":
                                k.pop()
                                if len(k) != 0:
                                    o[1] += "}"
                            else:
                                o[1] += s[current]
                            current += 1
                        new_s = s[0:itt] + "(%s)^(1/%s)" % (o[1], o[0]) + s[current:]
                    else:
                        new_s = s[0:itt] + "(%s)^(1/2)" % (o[0]) + s[current:]
                else:
                    new_s = s[0:itt] + "(%s)^(1/2)" % (o[0]) + s[current:]
                s = new_s

        itt += 1
    return s


def parse_latex(input_latex):
    """
    Takes a string of LaTeX and returns it as a SymPy expression, kinda.
    Only supports normal operations { + - * ^ / ( ) }, surds, and fractions.
    Uses parse_expr, so not really injection safe.
    """
    input_latex = input_latex.replace(" ", "")
    input_latex = remove_left_right(input_latex)
    input_latex = decompose_frac(input_latex)
    input_latex = decompose_surds(input_latex)

    tfms = (standard_transformations + (implicit_multiplication_application, convert_xor, split_symbols))

    sympy_expression = parse_expr(input_latex, transformations=tfms)

    return sympy_expression


if __name__ == "__main__":
    print("Testing code...")
    s2 = r"\frac{ - b + \sqrt{b^2-4ac}}{2a}"
    print(parse_latex(s2))
    # s3 =