import sys
import os
import subprocess
import jinja2
from antlr4 import *
from antlr4 import *
from ProjectLexer import ProjectLexer
from ProjectParser import ProjectParser
from ProjectErrorListener import ProjectLexerErrorListener, ProjectParserErrorListener, CompilerException
from ProjectPrintListener import ProjectPrintListener
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
    print "DDDDDDDDD"
    try:
        next_token = lexer.nextToken()
        if next_token.type == next_token.EOF:
            break
        print lexer.symbolicNames[next_token.type]
        print next_token
        tokens.append((lexer.symbolicNames[next_token.type], next_token))
        an_item=dict(line=str(next_token.line),column=str(next_token.column),text=str(next_token.text))
        items.append(an_item)
    except CompilerException as e:
        print "AAAAAAAA"
        lexer_errors.append(e)
        lexer.recover(e)

print 'tokens : ' , tokens
print 'lexer errors : ' , lexer_errors

 ############## PARSER PART ##############

parser = ProjectParser(stream)
parser.removeErrorListeners()
parser.addErrorListener(ProjectParserErrorListener());
project_tree = parser.program()
project_printer = ProjectPrintListener(file_name)
project_walker = ParseTreeWalker()
project_walker.walk(project_printer, project_tree)
project_bytecode = project_printer.get_bytecode()
parser_errors = []
parser_errors = parser._listeners[-1].errors
print 'parser errors : ' , parser_errors
if not lexer_errors and not parser_errors:
    if not os.path.exists('output'):
        os.mkdir('output')
    bytecode_file = os.path.join('output', file_name + '.bc')

    with open(bytecode_file, 'w') as f:
        f.write(project_bytecode)

    p = subprocess.Popen(['java', '-jar', 'jasmin.jar', '-d', 'output', bytecode_file], 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = p.communicate()
    if p[0]:
        print p[0]
    if p[1]:
        print p[1]
tokens_form = TokensForm()