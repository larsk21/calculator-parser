# calculator-parser

## AST

abstract syntax tree data structure

unknown operation is used to build incomplete syntax trees in case of errors

## Debug

example call to lexer and parser used for debugging

## Helper

for functions that don't belong somewhere else

## Input

encapsulates an array of characters or tokens

supports accessing the last read items

## Lexer

lexer

input: code, output: tokens

## Parser

parser

input: tokens, output: AST

## Token

represents a token with a token type and an optional value

position in the code is stored for error messages
