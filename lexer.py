

# A tokenizer for python


import fileinput
import re

# These need to match from start to end ^(keyword)$
keywords = {'False', 'None', 'True', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
               'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import',
               'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while',
               'with', 'yield'}

#These can match without spacing: 1+2 = 3 
operators = {'\+', '\-', '\*', '\*\*', '/', '//', '%', '@', '<<', '>>', '&', '\|', '\^', '~', '<(?!=|<)', '>', '<=', '>=', '==', '!='}

delimiters = {'\)', '\(', '\[', '\]', '\{', '\}', ',', ':', '\.', '\.\.\.', ';', '=(?!=)', '->', '\+=', '-=', '\*=', '/=', '//=',
              '%=', '@=', '&=', '\|=', '\^=', '>>=', '<<=', '\*\*='}

token_types = [
('NEWLINE', r'\n'),
('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
('NUMBER', r'\d+(\.\d*)?'),
('OPEN_STRING', r'\'[^\']*\n'),
('STRING', r'\'[^\']*\''),
('COMMENT', r'#.*\n'),
('PUNCT', r'|'.join(wrd for wrd in delimiters.union(operators))),
('LINE_CONTINUE', r'\\'),
('SPACE', r' ')
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_types)

def tokenize(line):
    for mo in re.finditer(tok_regex, line):
        group = mo.lastgroup
        match = mo.group(group)
        if group == 'ID' and match in keywords:
            group = 'KEYWORD'
        yield (group, match)

tokens = []
out = []
pastIndent = None
stack = []
def filterToken(match):
    global stack, pastIndent
    tokenType = match[0]
    if tokenType == 'COMMENT':
        return
    if stack and stack[-1] == 'NEWLINE':
        raise ValueError('')
        return
    if tokenType == 'SPACE':
        if not stack or stack[-1] == 'SPACE':
            stack.append('SPACE')
        return
    else:
        # not a space, check if there are spaces on stack, if so, pop them and emit indent tokens
        spaces = stack and stack[-1] == 'SPACE'
        if (spaces or not stack) and tokenType != 'NEWLINE':
            if pastIndent is None:
                pastIndent = len(stack)
            elif len(stack) > pastIndent:
                out.append('(INDENT)')
                pastIndent = len(stack)
            elif len(stack) < pastIndent:
                out.append('(DEDENT)')
                pastIndent = len(stack)
            stack = []
            #print('token: {0} of token type: {1} with space at: {2}'.format(repr(match[1]), str(tokenType),  pastIndent))
    if tokenType == 'NEWLINE':
        if stack and stack[-1] == 'SPACE':
            stack = []
        if stack and (stack[-1] == 'LINE_CONTINUE' or stack[-1] == '['):
            stack.pop()
            return
        if not stack:
            return
        else:
            stack = []
            out.append(str(match))
            return
    if tokenType == 'LINE_CONTINUE':
        stack.append('LINE_CONTINUE')
        return
    stack.append(str(tokenType))
    out.append(str(match))

for line in fileinput.input():
    for match in tokenize(line):
        tokens.append(match)
        filterToken(match)
else:
    #print( '\n'.join(tokens) ) 
    print( '\n'.join(out) )


