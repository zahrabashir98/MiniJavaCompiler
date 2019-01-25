import sys
import os
import subprocess
import jinja2
from antlr4 import *
from ProjectLexer import ProjectLexer
from ProjectErrorListener import ProjectLexerErrorListener, CompilerException
from antlr4.error.ErrorListener import ErrorListener

f=open("t.c", "r")
if f.mode == 'r':
    code =f.read()

############## LEXER PART ##############

lexer = ProjectLexer(InputStream(code))
lexer.removeErrorListeners()
lexer.addErrorListener(ProjectLexerErrorListener())
stream = CommonTokenStream(lexer)
tokens = []
lexer_errors = []
items = []
while True:
    try:
        next_token = lexer.nextToken()
        if next_token.type == next_token.EOF:
            break
        tokens.append((lexer.symbolicNames[next_token.type], next_token))
        an_item=dict(line=str(next_token.line),column=str(next_token.column),text=str(next_token.text))
        items.append(an_item)
    except CompilerException as e:
        lexer_errors.append(e)
        lexer.recover(e)

print 'tokens : ' , tokens
print 'lexer errors : ' , lexer_errors