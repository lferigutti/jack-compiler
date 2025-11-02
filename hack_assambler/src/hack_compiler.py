import os
import tomllib

class HackCompiler:
    """
    This function expects a correct
    """
    A_BINARY_LENGTH = 15
    C_LENGTH = 8
    CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    TABLE_FILE_PATH = os.path.join(CURRENT_DIRECTORY, "config", "control_table.toml")

    def __init__(self):
        self.tables = {}
        self._load_tables_from_file()
        self.comp_table = self.tables.get("comp")
        self.jump_table = self.tables.get("jump")
        self.dest_table = self.tables.get("dest")

    def _load_tables_from_file(self):
        with open(self.TABLE_FILE_PATH, 'rb') as f:
            self.tables = tomllib.load(f)


    def compile(self, instruction:str):
        if instruction.startswith('@'):
            return f"0{self._compile_a_instruction(instruction)}"
        else:
            return f"111{self._compile_c_instruction(instruction)}"


    def _compile_a_instruction(self, instruction:str):
        number = int(instruction.strip('@'))
        binary_number = bin(number)[2:]
        length = len(binary_number)
        zeros = ''.join('0') * (self.A_BINARY_LENGTH - length)
        return f'{zeros}{binary_number}'


    def _compile_c_instruction(self, instruction:str):
        c_parsed = self._parse_c_instruction(instruction)
        comp_part = self.comp_table.get(c_parsed.get('comp'))
        dest_part = self.dest_table.get(c_parsed.get('dest'))
        jump_part = self.jump_table.get(c_parsed.get('jump'))
        return f'{comp_part}{dest_part}{jump_part}'


    def _parse_c_instruction(self, instruction:str):
        """Extract key/value pairs from a simple YAML-like line."""
        # Extract dest part
        instruction = instruction.split('=')
        if len(instruction) == 2:
            dest = instruction[0]
            rest = instruction[1]
        else:
            dest = 'null'
            rest = instruction[0]

        # extract jump part
        inst = rest.split(';')
        if len(inst) == 2:
            comp = inst[0]
            jump = inst[1]
        else:
            comp = rest
            jump = 'null'
        return {'comp': comp, 'jump': jump, 'dest': dest}


        


