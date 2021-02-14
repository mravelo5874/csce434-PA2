#!/usr/bin/env python3
# coding=utf-8
from enum import Enum

# --------------------------------
#   Marco Ravelo
#   CSCE 434 - Compiler Design
#   Assignment #2 - 2/10/2021 
#   file: SymbolTable.py
# --------------------------------

# Resources used:

# --------------------------------
#   SYMBOL ERROR
# --------------------------------

class SymbolError(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return 'SymbolError: %s' % self.msg

class SymbolType(Enum):
    INT = 0
    CODE = 1

class TableEntry():
    def __init__(self, lexeme, symbol_type, address):
        self.lexeme = lexeme
        self.symbol_type = symbol_type
        self.address = address

class SymbolTable():

    def __init__(self):
        self.list = []
    
    # adds a symbol to the table
    def add_symbol(self, lexeme, symbol_type, address):
        # check to see if symbol already exists
        if (self.symbol_exists(lexeme)):
            raise SymbolError('symbol \'%s\' already exists in table (duplicate entry)')
            
        # add to list
        self.list.append(TableEntry(lexeme, symbol_type, address))

    # returns true if symbol already exists in the table
    def symbol_exists(self, symbol):
        for entry in self.list:
            if (symbol == entry.lexeme):
                return True
        return False

    # returns table entry if it exists in the table
    def find_symbol_lexeme(self, lexeme):
        if (not self.symbol_exists(lexeme)):
            raise SymbolError('symbol \'%s\' not found in symbol table')

        for entry in self.list:
            if (lexeme == entry.lexeme):
                return entry
        return None

    def find_symbol_address(self, address):
        return 0

    

