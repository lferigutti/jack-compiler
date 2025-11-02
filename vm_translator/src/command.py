from vm_translator.src.models import CommandType, ArithmeticCommandTypes, MemoryCommand, MemorySymbol


class Command:
  def __init__(
      self,
      command_type: CommandType,
      arg1: ArithmeticCommandTypes | MemorySymbol,
      arg2: None | int = None
  ):
    self.command_type = command_type
    self.arg1 = arg1
    self.arg2 = arg2

  def __str__(self):
    parts = []
    if self.command_type != CommandType.ARITHMETIC:
      parts.append(self.command_type.value)
    parts.append(self.arg1.value)
    if self.arg2 is not None:
      parts.append(str(self.arg2))
    return ' '.join(parts)

  def __repr__(self):
    return f"Command(command_type={self.command_type!r}, arg1={self.arg1!r}, arg2={self.arg2!r})"
  
  def __eq__(self, value):
     if not isinstance(value, Command):
         return False
     return (self.command_type == value.command_type and
             self.arg1 == value.arg1 and
             self.arg2 == value.arg2)

  def is_arithmetic(self):
      return self.command_type == CommandType.ARITHMETIC
  
  def is_push(self):
      return self.command_type == CommandType.PUSH

  def is_pop(self):
      return self.command_type == CommandType.POP
