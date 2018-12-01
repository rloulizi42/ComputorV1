from docopt import docopt

help = """

Usage: computor.py <argument>

"""

arguments = docopt(help)
equation = str(arguments['<argument>'])

print(equation)
