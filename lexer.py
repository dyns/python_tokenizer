

# A tokenizer for python


import fileinput
import re

# These need to match from start to end ^(keyword)$
keywords = {'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
               'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
               'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
               'with', 'yield'}

#These can match without spacing: 1+2 = 3 
operators = {'\+', '\-', '\*', '\*\*', '/', '//', '%', '@', '<<', '>>', '&', '\|', '\^', '~', '<', '>', '<=', '>=', '==', '!='}

delimiters = {'\)', '\(', '\[', '\]', '\{', '\}', ',', ':', '\.', '\.\.\.', ';', '=', '->', '\+=', '-=', '\*=', '/=', '//=',
              '%=', '@=', '&=', '\|=', '\^=', '>>=', '<<=', '\*\*='}

token_types = [
('NEWLINE', r'\n'),
('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
('INDENT', r'\t'),
('NUMBER', r'\d+(\.\d*)?'),
('OPEN_STRING', r'\'[^\']*\n'),
('STRING', r'\'[^\']*\''),
('PUNCT', r'|'.join(wrd for wrd in delimiters.union(operators)))
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_types)

def tokenize(line):
	for mo in re.finditer(tok_regex, line):
		yield str(mo.lastgroup) + ' ' + str(mo.group())

tokens = []
for line in fileinput.input():
	tokens.extend(tokenize(line))
else:
	print( '\n'.join(tokens) )
