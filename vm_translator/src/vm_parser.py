from vm_translator.src.command import Command
from vm_translator.src.models import CommandType, ArithmeticCommandTypes, MemoryCommand, MemorySegment
from typing import List
from pathlib import Path


class Parser:
  def __init__(self, file_path: Path):
    self.file_path = file_path

  def parse(self) -> List[Command]:
    clean_file = []
    with open(self.file_path, "r") as file:
      lines = file.readlines()
      for line in lines:
        line = line.strip()
        if not line or line.startswith("//"):
          continue
        else:
          command = self._parse_line(line)
          clean_file.append(command)
      return clean_file

  def _parse_line(self, line) -> Command:
    args = line.split(" ")
    if len(args) == 1:
      try:
        return Command(
          command_type=CommandType.ARITHMETIC,
          arg1=ArithmeticCommandTypes(args[0])
        )
      except Exception as e:
        raise SyntaxError(f"Invalid VM command syntax. Error: {e}")
    elif len(args) == 3:
      try:
        command_type = self._get_memory_type(args[0])
        arg1 = MemorySegment(args[1])
        arg2 = int(args[2])
        return Command(
          command_type=command_type,
          arg1=arg1,
          arg2=arg2
        )
      except Exception as e:
        raise SyntaxError(f"Invalid VM command syntax. Error: {e}")
    else:
      raise SyntaxError("Invalid VM command syntax")

  @staticmethod
  def _get_memory_type(memory_arg):
    if memory_arg == MemoryCommand.POP.value:
      return CommandType.POP
    elif memory_arg == MemoryCommand.PUSH.value:
      return CommandType.PUSH
    else:
      raise SyntaxError("Invalid Memory Command Type, it should be either push or pop")
