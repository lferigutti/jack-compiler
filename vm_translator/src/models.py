from enum import Enum


class ArithmeticCommandTypes(Enum):
  ADD = 'add'
  SUB = 'sub'
  NEG = 'neg'
  EQ = 'eq'
  GT = 'gt'
  LT = 'lt'
  AND = 'and'
  OR = 'or'
  NOT = 'not'


class MemoryCommand(Enum):
  PUSH = 'push'
  POP = 'pop'


class CommandType(Enum):
  ARITHMETIC = "arithmetic"
  PUSH = 'push'
  POP = 'pop'


class MemorySymbol(Enum):
  SP = 'SP'
  LCL = 'local'
  ARG = 'argument'
  THIS = 'this'
  THAT = 'that'
  TEMP = 'temp'
  POINTER = 'pointer'
  STATIC = 'static'
  CONSTANT = 'constant'
