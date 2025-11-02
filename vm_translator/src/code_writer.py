from pathlib import Path
from typing import List


class CodeWriter:
  def __init__(self, output_file: Path):
    self.output_path = output_file

  def write_file(self, instructions: List[str]):
    with open(self.output_path, "w") as file:
      number_of_lines = len(instructions)
      for i, instruction in enumerate(instructions):
        line_number = i + 1
        file.write(instruction + '\n') if line_number < number_of_lines else file.write(instruction)
