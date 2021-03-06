import re
from collections import defaultdict
from functools import partial
from itertools import product
from operator import sub, add


def tokenize(expression):

    def process_number(_, token):
        return {0: int(token)}

    def process_x(_, token):
        return {1: 1}

    def process_other(_, token):
        return token

    scanner = re.Scanner([(r'\d+', process_number),
                          (r'x', process_x),
                          (r'.', process_other)])

    tokens, unrecognised = scanner.scan(expression)

    return tokens


def reduce_polynomial(tokens):

    tokens = reduce_sub_expression(tokens)

    tokens = reduce_operation(tokens, '*', multiply_poly)
    tokens = reduce_operation(tokens, '-', partial(add_sub_poly, operation=sub))
    tokens = reduce_operation(tokens, '+', partial(add_sub_poly, operation=add))

    return tokens


def reduce_sub_expression(tokens):

    while '(' in tokens:

        last_bracket_index = 0

        for token_index, token in enumerate(tokens):

            if token == '(':
                last_bracket_index = token_index

            if token == ')':
                sub_expression = tokens[last_bracket_index + 1:token_index]

                left_tokens = tokens[:last_bracket_index]
                right_tokens = tokens[token_index + 1:]

                tokens = left_tokens + reduce_polynomial(sub_expression) + right_tokens
                break

    return tokens


def reduce_operation(tokens, operation_symbol, operation_function):

    while operation_symbol in tokens:

        for token_index, token in enumerate(tokens):

            if token == operation_symbol:
                a_poly = tokens[token_index - 1]
                b_poly = tokens[token_index + 1]

                c_poly = operation_function(a_poly, b_poly)

                tokens = tokens[:token_index - 1] + [c_poly] + tokens[token_index + 2:]
                break

    return tokens


def multiply_poly(a_poly, b_poly):

    term_pairs = list(product(a_poly.items(), b_poly.items()))

    terms = [(u_degree + v_degree, u_coefficient * v_coefficient)
             for (u_degree, u_coefficient), (v_degree, v_coefficient)
             in term_pairs]

    c_poly = defaultdict(int)

    for term in terms:
        term_degree, term_coefficient = term
        c_poly[term_degree] += term_coefficient

    return dict(c_poly)


def add_sub_poly(a_poly, b_poly, operation):

    degrees = set(a_poly) | set(b_poly)

    c_poly = {degree: operation(a_poly.get(degree, 0), b_poly.get(degree, 0))
              for degree in degrees}

    return c_poly


def polynomial_to_string(polynomial):

    polynomial_string = ''

    sorted_polynomial = sorted(polynomial.items(), reverse=True)

    for degree, coefficient in sorted_polynomial:

        if coefficient == 0:
            coefficient_string = ''

        elif coefficient == 1 and degree == max(degree for degree, coefficient in polynomial.items()):
            coefficient_string = ''

        elif coefficient > 0 and degree == max(degree for degree, coefficient in polynomial.items()):
            coefficient_string = f'{coefficient:d}'

        elif coefficient == 1 and degree > 0:
            coefficient_string = '+'

        elif coefficient == -1 and degree > 0:
            coefficient_string = '-'

        else:
            coefficient_string = f'{coefficient:+d}'

        if degree == 0 or coefficient == 0:
            degree_string = ''

        elif degree == 1:
            degree_string = f'x'

        else:
            degree_string = f'x**{degree}'

        if coefficient_string in '-+':
            inter_term_symbol = ''
        else:
            inter_term_symbol = '*'

        term_string = inter_term_symbol.join(filter(None, (coefficient_string, degree_string)))

        polynomial_string += term_string

    if polynomial_string == '':
        polynomial_string = '0'

    return polynomial_string


def simplify(expr):

    tokens = tokenize(expr)

    resulting_polynomial = reduce_polynomial(tokens)[0]

    resulting_polynomial_string = polynomial_to_string(resulting_polynomial)

    print('Expression:                 ', expr)
    print('Resulting polynomial:       ', resulting_polynomial)
    print('Resulting polynomial string:', resulting_polynomial_string)
    print()

    return resulting_polynomial_string


if __name__ == "__main__":
    assert simplify("((x*5)*(x+1))-16456*x*x*x+(x*x)*(1)") == '-16456*x**3+6*x**2+5*x'
    assert simplify("x*x*x+5*x*x+x*x+3*x-1") == "x**3+6*x**2+3*x-1"

    assert simplify("(x-1)*(x+1)") == "x**2-1", "First and simple"
    assert simplify("(x+1)*(x+1)") == "x**2+2*x+1", "Almost the same"
    assert simplify("(x+3)*x*2-x*x") == "x**2+6*x", "Different operations"
    assert simplify("x+x*x+x*x*x") == "x**3+x**2+x", "Don't forget about order"
    assert simplify("(2*x+3)*2-x+x*x*x*x") == "x**4+3*x+6", "All together"
    assert simplify("x*x-(x-1)*(x+1)-1") == "0", "Zero"
    assert simplify("5-5-x") == "-x", "Negative C1"
    assert simplify("x*x*x-x*x*x-1") == "-1", "Negative C0"
