# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computor.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rloulizi <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/12/02 19:06:21 by rloulizi          #+#    #+#              #
#    Updated: 2018/12/02 21:25:26 by rloulizi         ###   ########.fr        #
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
    if x_list[-1] == "X^2":
        power['two'].append(x_list[7] + x_list[8])
        power['one'].append(x_list[3] + x_list[4])
        power['zero'].append(x_list[0])
    if x_list[-1] == "X^1":
        power['one'].append(x_list[3] + x_list[4])
        power['zero'].append(x_list[0])
    if x_list[-1] == "X^0":
        power['zero'].append(x_list[0])
    y_list = y.split(' ')
    if y_list[-1] == "X^2":
        power['two'].append(y_list[7] + y_list[8])
        power['one'].append(y_list[3] + y_list[4])
        power['zero'].append(y_list[0])
    if y_list[-1] == "X^1":
        power['one'].append(y_list[3] + y_list[4])
        power['zero'].append(y_list[0])
    if y_list[-1] == "X^0":
        power['zero'].append(y_list[0])
    return power

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

if __name__ == '__main__':
    x, y = regex_and_split(help)
    power = lstrip(parser(x, y))
    for e in power['two']:
        print(int(e))
