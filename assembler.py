#!/usr/bin/env python3
# coding=utf-8

# --------------------------------
#   Marco Ravelo
#   CSCE 434 - Compiler Design
#   Assignment #2 - 2/10/2021 
#   file: assembler.py
# --------------------------------

# Resources used:

    # --------------------------------
    #   NUMERIC OPCODES
    # --------------------------------
        #   HALT    0
        #   PUSH    1
        #   RVALUE  2
        #   LVALUE  3
        #   POP     4
        #   STO     5
        #   COPY    6
        #   ADD     7
        #   SUB     8
        #   MPY     9
          
        #   DIV     10
        #   MOD     11
        #   NEG     12
        #   NOT     13
        #   OR      14
        #   AND     15
        #   EQ      16
        #   NE      17
        #   GT      18
        #   GE      19

        #   LT      20
        #   LE      21
        #   LABEL   22
        #   GOTO    23
        #   GOFALSE 24
        #   GOTRUE  25
        #   PRINT   26
        #   READ    27
        #   GOSUB   28
        #   RET     29


# --------------------------------
#   ASSEMBLER ERROR
# --------------------------------

class AssemberError(Exception):
    def __init__(self, pos, line, err, msg):
        self.pos = pos
        self.line = line
        self.err = err
        self.msg = msg

    def __str__(self):
        return 'AssemberError[%s]: %s at line: %i pos: %i' % (self.err, self.msg, self.line, self.pos)

# --------------------------------
#   ASSEMBLER
# --------------------------------

class Assember:
    # --------------------------------
    #   INITIALIZER
    # --------------------------------

    def __init__(self, opts=[]):
        self.print = False
        
        for opt in opts:
            # options for assembler
            if (opt == '-print'):
                self.print = True

        pass

    def start(self, text):
        self.text = text
        self.pos = 0
        self.line = 0
        self.length = len(text)

        try:
            self.main_loop()
        except AssemberError as Error:
            print(Error)

    # --------------------------------
    #   MAIN_LOOP
    # --------------------------------

    def main_loop(self):

        output = []

        while (self.pos < self.length):
            # ge next word in text
            word = self.get_next_word()
            self.print_msg('word found: %s' % word)

            # check for new line char
            
            # translate
            code = self.translate(word)

            # add to output
            output.append(code)
        
        return output

    # --------------------------------
    #   TRANSLATOR
    # --------------------------------

    def translate(self, word):
        return 'None'


    # --------------------------------
    #   HELPER METHODS
    # --------------------------------

    def get_next_word(self):
        return "None"

    def print_msg(self, msg):
        if (not self.print):
            return
        print ('line: %i\tpos: %i\t\t%s' % (self.line, self.pos, msg))
