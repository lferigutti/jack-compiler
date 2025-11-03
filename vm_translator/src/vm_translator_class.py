from typing import List

from vm_translator.src.command import Command
from vm_translator.src.assembly_expressions import AssemblyExpressions
from vm_translator.src.models import CommandType


class VMTranslator:
  assembly_expressions = AssemblyExpressions()

  def translate(self, commands: List[Command], write_comment: bool = True) -> List[str]:
    output = []
    for command in commands:
      if write_comment:
        comment = f"// {str(command)}"
        output.append(comment)
      command_translated = self._translate_command(command)
      output.extend(command_translated)
    return output

  def _translate_command(self, command: Command) -> List[str]:
    if command.is_arithmetic():
      return self._translate_arithmetic_command(command)
    elif command.is_push():
      return self._translate_push_command(command)
    elif command.is_pop():
      return self._translate_pop_command(command)
    else:
      raise NotImplemented(f"Command {command.command_type} not implemented yet.")

  @staticmethod
  def _translate_arithmetic_command(command: Command) -> List[str]:
    if command.is_add():
      return ["@SP", "A=M-1", "D=M", "A=A-1", "M=D+M", "@SP", "M=M-1"]

    return list(str(command))

  @staticmethod
  def _translate_push_command(command: Command) -> List[str]:
    if command.is_constant_segment():
      return [f'@{command.arg2}', "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    return list(str(command))

  def _translate_pop_command(self, command: Command) -> list[str]:
    if command.is_common_segment():
      segment = self.assembly_expressions.segment(command.arg1)
      return [f"@{segment}", "D=M", f"@{command.arg2}", "D=D+A", "@SP", "M=M-1", "A=M+1", "M=D", "A=A-1", "D=M",
              "A=A+1", "A=M", "M=D"]
    return list(str(command))
