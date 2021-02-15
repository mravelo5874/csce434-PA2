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

# instructions that precede int symbols
pre_int = {
    'PUSH',
    'RVALUE',
    'LVALUE'
}

# instructions that precede code symbols
pre_code = {
    'LABEL',
    'GOTO',
    'GOFALSE',
    'GOTRUE',
    'GOSUB'
}

# --------------------------------
#   ASSEMBLER ERROR
# --------------------------------

class AssemberError(Exception):
    def __init__(self, pos, line, pss, err, msg):
        self.pos = pos
        self.line = line
        self.err = err
        self.msg = msg
        self.pss = pss

    def __str__(self):
        return 'AssemberError[%s]: %s at line: %i pos: %i pass: %i' % (self.err, self.msg, self.line, self.pos, self.pss)

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
        self.pss = 0
        self.location_counter = 0
        self.length = len(self.text)
        self.prev_word = ''
        self.table = SymbolTable.SymbolTable()

        try:
            self.first_pass()
            self.second_pass()
        except AssemberError as AError:
            print (AError)
        except SymbolTable.SymbolError as SError:
            print (SError, end='')
            print (' at line: %i pos: %i pass: %i' % (self.line, self.pos, self.pss))

    # --------------------------------
    #   PASS METHODS
    # --------------------------------

    def first_pass(self):
        self.pss = 1
        self.print_msg('[starting pass 1]')

        word = 'start'

        while (self.pos <= self.length and word != 'HALT'):
            # get next word in text
            word = self.get_next_word()
            self.print_msg('word found: %s' % word)

            # add to symbol table if word is a lexeme
            if (word not in opcodes and not self.is_num(word)):
                symbol_type = self.symbol_type(word)
                self.table.add_symbol(word, symbol_type, self.location_counter)
                self.location_counter += 1

            self.prev_word = word

        self.table.print_table()

    def second_pass(self):
        self.pss = 2
        self.pos = 0
        self.line = 1
        self.print_msg('[starting pass 2]')

        code_list = []
        word = 'start'

        while (self.pos <= self.length and word != 'HALT'):
            # get next word in text
            word = self.get_next_word()

            # get second word if needed
            if (word in pre_int or word in pre_code):
                next_word = self.get_next_word()
                comp_line = '\'' + word + ' ' + next_word + '\''
            else:
                comp_line = '\'' + word + '\''
            
            # translate to machine code
            code = self.translate(word, next_word)
            code_list.append(code)
            self.print_msg('%s : %s' % (code, comp_line))


    # --------------------------------
    #   TRANSLATOR METHODS
    # --------------------------------

    def translate(self, opcode, operand=''):

        # bits 32-21 are zeros
        part1 = '000000000000'

        # bits 20-16 are op code
        part2 = self.opcode_bits(opcode)

        # bits 15-0 are operand (or zeros)
        if (operand != ''):
            part3 = self.operand_bits(operand)
        else:
            part3 = '0000000000000000'
        
        res = part1 + ' ' + part2  + ' ' + part3

        return res

    def opcode_bits(self, opcode):
        #print ('opcode: ', opcode)
        num = opcodes.get(opcode)
        #print ('num: ', num)
        bits = format(num, '05b')
        return bits


    def operand_bits(self, operand):
        print ('operand: ', operand)
        num = self.table.get_address(operand)
        print ('num: ', num)
        bits = format(num, '016b')
        return bits

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
                raise AssemberError(self.pos, self.line, self.pss, 'INVALID WORD', 'invalid char found \'%s\'' % char)

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

    # determine symbol type
    def symbol_type(self, symbol):
        if (self.prev_word in pre_int):
            return 'INT'
        elif (self.prev_word in pre_code):
            return 'CODE'
        else:
            raise AssemberError(self.pos, self.line, self.pss, 'INVALID SYMBOL', 'could not determine symbol type of \'%s\'' % symbol)
