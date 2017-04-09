

# A tokenizer for python


import fileinput
import re

# These need to match from start to end ^(keyword)$
keywords = {'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
               'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
               'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
               'with', 'yield'}

#These can match without spacing: 1+2 = 3 
operators = {'\+', '-', '\*', '\*\*', '/', '//', '%', '@', '<<', '>>', '&', '\|', '\^', '~', '<', '>', '<=', '>=', '==', '!='}

delimiters = {'\)', '\(', '\[', '\]', '\{', '\}', ',', ':', '\.', ';', '=', '->', '\+=', '-=', '\*=', '/=', '//=',
              '%=', '@=', '&=', '\|=', '\^=', '>>=', '<<=', '\*\*='}

#total_regs = '^(\.\.\.)|' + ('|'.join(keywords)) + '|^ +' + '|^(\r\n?|\n)' + '|^[a-zA-Z]*'

#regs = '|'.join(['^('+word+')$' for word in keywords.union(operators, delimiters)]) + '|^[0-9]'
#regs = re.compile(regs)

#print(regs)

def tokenize(line):
	for mo in re.finditer('|'.join(['(' + word +')' for word  in operators.union(delimiters)]), line):
		print(mo.group())

for line in fileinput.input():
	tokenize(line)






