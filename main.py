from my_lexer import lexer
from my_parser import parser
from interpreter import beta_reduction, interpret
import cmd

PROMPT = '>>>'
INTRO_STR = \
"""
Welcome to PL(Python based Lambda expression Interpreter) developed by Yikai Zhang & Fan Nie, <https://github.com/FKCSP/PLI>
"""

class main_loop(cmd.Cmd):
    def __init__(self, *args, **kwargs):
        cmd.Cmd.__init__ (self)
        self.prompt = PROMPT
        self.intro = INTRO_STR

    def default(self, s):
        input_str = parser.parse(s)
        reduced_term = interpret(input_str)
        # reduced_term = beta_reduction(input_str)
        print(reduced_term)

    def do_EOF(self, line):
        print("Bye!")
        return True

if __name__ == '__main__':
    main_loop().cmdloop()
