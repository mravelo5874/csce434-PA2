#!/usr/bin/env python3
# coding=utf-8
import SymbolTable

# --------------------------------
#   Marco Ravelo
#   CSCE 434 - Compiler Design
#   Assignment #2 - 2/10/2021 
#   file: Assembler.py
# --------------------------------

# Resources used:
#   NONE

# --------------------------------
#   CHAR LIST
# --------------------------------
whitespace = ' \n\t\r\v\f'
alpha_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
alphaNums_chars = '01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
nums_chars = '01234567890'
valid_chars = '01234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'

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

opcodes = {
    'HALT':    0,
    'PUSH':    1,
    'RVALUE':  2,
    'LVALUE':  3,
    'POP':     4,
    'STO':     5,
    'COPY':    6,
    'ADD':     7,
    'SUB':     8,
    'MPY':     9,
    'DIV':     10,
    'MOD':     11,
    'NEG':     12,
    'NOT':     13,
    'OR':      14,
    'AND':     15,
    'EQ':      16,
    'NE':      17,
    'GT':      18,
    'GE':      19,
    'LT':      20,
    'LE':      21,
    'LABEL':   22,
    'GOTO':    23,
    'GOFALSE': 24,
    'GOTRUE':  25,
    'PRINT':   26,
    'READ':    27,
    'GOSUB':   28,
    'RET':     29
}


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

class MyAssember:
    # --------------------------------
    #   INITIALIZER
    # --------------------------------

    def __init__(self, opts=[]):
        self.print = False
        
        for opt in opts:
            # options for assembler
            if (opt == '-print'):
                self.print = True

    def start(self, lines):
        self.lines = lines
        # combine all text into a single string
        self.text = ''
        for element in lines:
            self.text += element
        self.pos = 0
        self.line = 1
        self.location_counter = 0
        self.length = len(self.text)
        self.table = SymbolTable.SymbolTable()

        try:
            self.first_pass()
        except AssemberError as Error:
            print(Error)

    # --------------------------------
    #   FIRST PASS
    # --------------------------------

    def first_pass(self):

        while (self.pos < self.length):
            # ge next word in text
            word = self.get_next_word()
            self.print_msg('word found: %s' % word)

            # add to symbol table if word is a lexeme
            if (word not in opcodes and not self.is_num(word)):
                self.table.add_symbol(word, 'UNDEF', self.location_counter)
                self.location_counter += 1

        self.table.print_table()


    # --------------------------------
    #   TRANSLATOR
    # --------------------------------

    def translate(self, word):
        return 'None'


    # --------------------------------
    #   HELPER METHODS
    # --------------------------------

    # skips over whitespace
    def ignore_whitespace(self):
        # skip any whitespace chars
        while (self.pos < self.length and self.text[self.pos] in whitespace):
            # increment line number when encountering a \n char
            if (self.text[self.pos] == '\n'):
                self.line += 1
            self.pos += 1
        return

    # gets the next word separated by whitespace
    def get_next_word(self):
        self.ignore_whitespace()

        # create word until whitespace detected or EOF
        temp_pos = self.pos
        while (temp_pos < self.length and self.text[temp_pos] not in whitespace):
            temp_pos += 1
        
        word_found = self.text[self.pos:temp_pos]

        # determine if word is vaild
        for char in word_found:
            if (char not in valid_chars):
                raise AssemberError(self.pos, self.line, 'INVALID WORD', 'invalid char found \'%s\'' % char)

        self.pos = temp_pos
        return word_found

    # return true if word is a number, else false
    def is_num(self, word):
        for char in word:
            if (char not in nums_chars):
                return False
        return True

    # prints msg with position and line number
    def print_msg(self, msg):
        if (not self.print):
            return
        print ('line: %i\tpos: %i\t\t%s' % (self.line, self.pos, msg))
