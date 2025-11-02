from typing import List

from vm_translator.src.command import Command
from vm_translator.src.models import CommandType


class VMTranslator:

  def translate(self, commands: List[Command]) -> List[str]:
    output = []
    for command in commands:
      command_translated = self._translate_command(command)
      output.append(command_translated)
    return output

  def _translate_command(self, command: Command) -> str:
    if command.command_type == CommandType.ARITHMETIC:
      return self.translate_arithmetic_command(command)
    elif command.command_type == CommandType.PUSH or command.command_type == CommandType.POP:
      return self.translate_push_pop_command(command)
    else:
      raise NotImplemented(f"Command {command.command_type} not implemented yet.")

  @staticmethod
  def translate_arithmetic_command(command: Command) -> str:
    return str(command)

  @staticmethod
  def translate_push_pop_command(command: Command) -> str:
    return str(command)
