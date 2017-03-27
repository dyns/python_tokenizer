

# A tokenizer for python


import fileinput
import re

keywords = {'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
               'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
               'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
               'with', 'yield'}

operators = {'\+', '-', '\*', '\*\*', '/', '//', '%', '@', '<<', '>>', '&', '\|', '\^', '~', '<', '>', '<=', '>=', '==', '!='}

delimiters = {'\)', '\(', '\[', '\]', '\{', '\}', ',', ':', '\.', ';', '=', '->', '\+=', '-=', '\*=', '/=', '//=',
              '%=', '@=', '&=', '\|=', '\^=', '>>=', '<<=', '\*\*='}

keywords = keywords.union(operators, delimiters)

keywords = {'^(' + word + ')' for word in keywords}

#total_regs = '^\(|^\)|^("|\').*("|\')|^:|^\.|^ |^[a-zA-Z]+$|' + '|'.join(keywords)

total_regs = '^(\.\.\.)|' + ('|'.join(keywords)) + '|^ +' + '|^(\r\n?|\n)' + '|^[a-zA-Z]*'

#for (i, l) in enumerate(total_regs):
#    print(str(i) + ' ' + l)

regs = re.compile(total_regs)

# for each line, parse it into tokens and print
def parseLine(line):
    if not line:
        print('empty line')
        return
    matches = list(re.finditer(regs, line))
    if not matches:
        print('empty matches list')
        return
    match = matches[0].group()
    print('\nmatch: \'' + str(matches[0]) + '\'')
    line = line[len(match):]
    print('rest of line: \'' + line + '\'\n')
    parseLine(line)

for line in fileinput.input():
	parseLine(line)

