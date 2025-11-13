from typing import List

from vm_translator.src.command import Command
from vm_translator.src.assembly_expressions import AssemblyExpressions
from vm_translator.src.models import BranchingCommand


class VMTranslator:
  assembly_expressions = AssemblyExpressions()

  def __init__(self, file_name: str):
    self.label_counter = 0
    self.file_name = file_name

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
    elif command.is_branching():
      return self._translate_branching_commands(command)
    elif command.is_function():
      return self._translate_function_command(command)
    elif command.is_return():
      return self._translate_return_command(command)
    else:
      raise SyntaxError(f"Command {command.command_type.value} not implemented yet.")

  def _translate_arithmetic_command(self, command: Command) -> List[str]:
    if command.is_add():
      return ["@SP", "A=M-1", "D=M", "A=A-1", "M=D+M", "@SP", "M=M-1"]
    elif command.is_sub():
      return ["@SP", "A=M-1", "D=M", "A=A-1", "M=M-D", "@SP", "M=M-1"]
    elif command.is_eq_lt_gt():
      self.label_counter += 1
      jump_command = self.assembly_expressions.jump(command.arg1)
      return ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", f"@{command.arg1.value.upper()}_TRUE_{self.label_counter}",
              f"D;{jump_command}", "@SP",
              "A=M-1", "M=0", f"@END_{self.label_counter}", "0;JMP",
              f"({command.arg1.value.upper()}_TRUE_{self.label_counter})",
              "@SP", "A=M-1",
              "M=-1", f"(END_{self.label_counter})"]
    elif command.is_not_neg():
      operation = self.assembly_expressions.get_operation(command.arg1)
      return ["@SP", "A=M-1", f"M={operation}M"]
    elif command.is_and_or():
      operation = self.assembly_expressions.get_operation(command.arg1)
      return ["@SP", "AM=M-1", "D=M", "A=A-1", f"M=D{operation}M"]
    else:
      raise SyntaxError(f"Arithmetic Command '{str(command)}' is not valid. Arg {command.arg1} does not exist.")

  def _translate_push_command(self, command: Command) -> List[str]:
    if command.is_constant_segment():
      return [f'@{command.arg2}', "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1"]
    elif command.is_common_segment() or command.is_temp_segment():
      segment = self.assembly_expressions.segment(command.arg1)
      value = "M" if command.is_common_segment() else 'A'
      return [f"@{segment}", f"D={value}", f"@{command.arg2}", "A=D+A", "D=M", "@SP", "M=M+1", "A=M-1", "M=D"]
    elif command.is_static_segment():
      return [f"@{self.file_name}.{command.arg2}", "D=M", "@SP", "M=M+1", "A=M-1", "M=D"]
    elif command.is_pointer_segment():
      segment = self.assembly_expressions.get_pointer_mapping(command.arg2)
      return [f"@{segment}", "D=M", "@SP", "M=M+1", "A=M-1", "M=D"]
    else:
      raise SyntaxError(f"Push Command '{str(command)}' is not valid. Segment {command.arg1} does not exist.")

  def _translate_pop_command(self, command: Command) -> List[str]:
    if command.is_common_segment() or command.is_temp_segment():
      segment = self.assembly_expressions.segment(command.arg1)
      value = "M" if command.is_common_segment() else 'A'
      return [f"@{segment}", f"D={value}", f"@{command.arg2}", "D=D+A", "@SP", "M=M-1", "A=M+1", "M=D", "A=A-1", "D=M",
              "A=A+1", "A=M", "M=D"]
    elif command.is_static_segment():
      return [f"@{self.file_name}.{command.arg2}", "D=A", "@SP", "M=M-1", "A=M+1", "M=D", "A=A-1", "D=M",
              "A=A+1", "A=M", "M=D"]
    elif command.is_pointer_segment():
      segment = self.assembly_expressions.get_pointer_mapping(command.arg2)
      return ["@SP", "AM=M-1", "D=M", f"@{segment}", "M=D"]
    else:
      raise SyntaxError(f"Pop Command '{str(command)}' is not valid. Segment {command.arg1} does not exist.")

  def _translate_branching_commands(self, command: Command) -> List[str]:
    label = f"{command.arg2}.{self.file_name}"
    if command.arg1 == BranchingCommand.LABEL:
      return [f"({label})"]
    elif command.arg1 == BranchingCommand.GOTO:
      return [f"@{label}", "0;JMP"]
    elif command.arg1 == BranchingCommand.IF_GOTO:
      return ["@SP", "AM=M-1", "D=M", f"@{label}", "D;JNE"]
    else:
      raise SyntaxError(f"Branching Command '{str(command)}' is not valid.")

  def _translate_function_command(self, command: Command) -> List[str]:
    function_name = command.arg1
    n_vars = int(command.arg2)

    def _push_local_vars(n_local_vars: int):
      if n_local_vars < 0:
        raise SyntaxError(f"Number of variables cannot be lower than 0. You input {n_local_vars}")

      if n_local_vars == 0:
        return []
      elif n_local_vars == 1:
        return ["@LCL", "A=M", "M=0"]
      else:
        return ["A=A+1", "M=0"]

    assembly_commands = [f"({function_name})"]
    for i in range(1, n_vars + 1):
      assembly_commands.extend(_push_local_vars(i))

    return assembly_commands

  def _translate_return_command(self, command: Command) -> List[str]:

    # endFrame = LCL
    assembly_command = ["@LCL", "D=M", "@R13", "M=D"]
    # retAddr = *(endFrame - 5)
    assembly_command.extend(["@5", "D=D-A", "@R14", "M=D"])
    # *ARG = pop()
    assembly_command.extend(["@SP", "A=M-1", "D=M", "@ARG", "A=M", "M=D", "D=A"])
    # SP = ARG +1
    assembly_command.extend(["@SP", "M=D+1"])
    # THAT = *(endFrame - 1)
    assembly_command.extend(["@R13", "A=M-1", "D=M", "@THAT", "M=D"])
    # THIS = *(endFrame - 2)
    assembly_command.extend(["@R13", "D=M", "@2", "A=D-A", "D=M", "@THIS", "M=D"])
    # ARG = *(endFrame - 3)
    assembly_command.extend(["@R13", "D=M", "@3", "A=D-A", "D=M", "@ARG", "M=D"])
    # LCL = *(endFrame - 4)
    assembly_command.extend(["@R13", "D=M", "@4", "A=D-A", "D=M", "@LCL", "M=D"])
    # goto retAddr
    assembly_command.extend(["@R14", "A=M", "0;JMP"])

    return assembly_command
