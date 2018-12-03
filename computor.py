# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computor.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rloulizi <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/12/02 19:06:21 by rloulizi          #+#    #+#              #
#    Updated: 2018/12/03 20:41:51 by rloulizi         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re
from docopt import docopt
import sys

help = """

Usage: computor.py <argument>

"""

power = {
        'zero' : [],
        'one' : [],
        'two' : [],
        }

def regex_and_split(help):
    arguments = docopt(help)
    equation = str(arguments['<argument>'])

    regex = r"^(?!\s)([0-9]*[.]?[0-9]*\s\*\sX\^[0-9]*)(\s[-+]\s[0-9]*[.]?[0-9]*\s\*\sX\^[0-9]*)*(\s=\s)([0-9]*[.]?[0-9]*\s\*\sX\^[0-9]*)(\s[-+]\s[0-9]*[.]?[0-9]*\s\*\sX\^[0-9]*)*$"

    if not re.match(regex, equation):
        print("Error")
        sys.exit(0)
    else:
        x, y = equation.split('=')
        return x[:-1], y[1:]

def parser(x, y):
    x_list = x.split(' ')
    y_list = y.split(' ')
    if x_list[-1] == 'X^0' and y_list[-1] == 'X^0':
        if x_list[0] == y_list[0]:
            print("the solution is |R")
            sys.exit(0)
        else:
            print("no solution")
            sys.exit(0)
    try:
        if x_list[-1] == "X^2":
            power['two'].append(x_list[7] + x_list[8])
            power['one'].append(x_list[3] + x_list[4])
            power['zero'].append(x_list[0])
            power['power'] = 2
        elif x_list[-1] == "X^1":
            power['one'].append(x_list[3] + x_list[4])
            power['zero'].append(x_list[0])
            power['power'] = 1
        elif x_list[-1] == "X^0":
            power['zero'].append(x_list[0])
            power['power'] = 0
        elif x_list[-1] not in ("X^0", "X^1", "X^2"):
            print("The polynomial degree is stricly greater than 2, I can t solve.")
            sys.exit(0)
        if y_list[-1] == "X^2":
            power['two'].append("-" + y_list[8])
            power['one'].append("-" + y_list[4])
            power['zero'].append(y_list[0])
        if power['power'] < 2:
            power['power'] = 2
        if y_list[-1] == "X^1":
            power['one'].append("-" + y_list[4])
            power['zero'].append(y_list[0])
        if power['power'] < 1:
            power['power'] = 1
        if y_list[-1] == "X^0":
            power['zero'].append("-" + y_list[0])
        if power['power'] < 0:
            power['power'] = 0
        if y_list[-1] not in ("X^0", "X^1", "X^2"):
            print("The polynomial degree is stricly greater than 2, I can t solve.")
            sys.exit(0)
        if x_list[-1] == '0' and y_list[-1] == '0':
            print("the solution is |R")
            sys.exit(0)
        return power
    except:
        print("Unordered degree")
        sys.exit(0)

def lstrip(power):
    lzero, lone, ltwo = [], [], []
    for e in power['zero']:
        lzero.append(e.lstrip('+'))
    power['zero'] = lzero
    for e in power['one']:
        lone.append(e.lstrip('+'))
    power['one'] = lone
    for e in power['two']:
        ltwo.append(e.lstrip('+'))
    power['two'] = ltwo
    return power

def atofloat(power):
    nzero, none, ntwo = [], [], []
    for e in power['zero']:
        if e[0] == '-':
            nzero.append(float(e[1:]) * -1)
        else:
            nzero.append(float(e))
    power['zero'] = nzero
    for e in power['one']:
        if e[0] == '-':
            none.append(float(e[1:]) * -1)
        else:
            none.append(float(e))
    power['one'] = none
    for e in power['two']:
        if e[0] == '-':
            ntwo.append(float(e[1:]) * -1)
        else:
            ntwo.append(float(e))
    power['two'] = ntwo
    return (power)

def delta(power):
    power['two'], power['one'], power['zero']  = sum(power['two']), sum(power['one']), sum(power['zero'])
    a, b, c = power['two'], power['one'], power['zero']
    delta = (b * b) - 4 * (a * c)
    power['delta'] = delta
    return (power)

def discriminant_1(power):
    power['one'], power['zero']  = sum(power['one']), sum(power['zero'])
    b, c = power['one'], power['zero']
    power['discriminant'] = str(float((c * -1) / b))
    return power

def discriminant_2(power):
    a, b, c, d = power['two'], power['one'], power['zero'], power['delta']
    if power['delta'] == 0:
        power['discriminant'] = (b * -1) / (2 * a)
    if power['delta'] > 0:
        power['discriminant'] = [((b * -1) - (d**0.5)) / (2 * a), ((b * -1) + (d**0.5)) / (2 * a)]
    if power['delta'] < 0:
        power['delta'] = power['delta'] * -1
        power['delta'] = "(" + str(int(power['delta'])) + "**0.5)i"
        if b > 0:
            power['discriminant'] = ["("+str((b * -1)) + " - " + power['delta'] + ") / " +  str(2 * a), "("+str((b * -1)) + " + " + power['delta'] + ") / " +  str(2 * a)]
        else:
            power['discriminant'] = ["("+str((b)) + " - " + power['delta'] + ") / " +  str(2 * a), "("+      str((b)) + " + " + power['delta'] + ") / " +  str(2 * a)]
    return power

def choice_power(power):
    if power['power'] == 2:
        power = delta(power)
        power = discriminant_2(power)
    if power['power'] == 1:
        power = discriminant_1(power)
    return power

def char_positive_or_negative(l):
    if l > 0:
        return "+ "
    else:
        return ""

def reduced_form(power):
    if power['power'] == 2:
        print("Reduced form: " + str(power['zero']) + " * X^0 " + char_positive_or_negative(power['one']) + str(power['one']) + " * X^1 " + char_positive_or_negative(power['two']) + str(power['two']) + " * X^2 = 0")
    if power['power'] == 1:
        print("Reduced form: " + str(power['zero']) + " * X^0 " + char_positive_or_negative(power['one']) + str(power['one']) + " * X^1 = 0")

def polynomial_degree(power):
    print("Polynomial degree: " + str(power['power']))

def result(power):
    if power['power'] == 2:
        if power['delta'] == 0:
            print("Discriminant is 0, the solution is:\n" + str(power['discriminant']))
        if power['delta'] > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            print(str(power['discriminant'][0]))
            print(str(power['discriminant'][1]))
        if power['delta'] < 0:
            print("Discriminant is strictly negative, the two complex solutions are:")
            print(str(power['discriminant'][0]))
            print(str(power['discriminant'][1]))
    if power['power'] == 1:
        print("The solution is:\n" + str(power['discriminant']))

if __name__ == '__main__':
    x, y = regex_and_split(help)
    power = lstrip(parser(x, y))
    power = atofloat(power)
    power = choice_power(power)
    reduced_form(power)
    polynomial_degree(power)
    result(power)
