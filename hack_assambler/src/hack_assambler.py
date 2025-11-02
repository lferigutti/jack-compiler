from src.hack_compiler import HackCompiler
from src.parser import Parser
from src.symbol_table import SymbolTable


class HackAssambler:
    def __init__(self, path):
        self.path = path
        self.parser=Parser(path)
        self.file_parsed = None
        self.file_parsed_cleaned = None
        self.compiler = HackCompiler()
        self.file_compiled = None
        self.symbol_table = SymbolTable()
        self.pointer_ram_address = 16


    def parse(self):
        self.file_parsed = self.parser.parse()

    def compile(self):
        self._set_labels_for_symbol_table()
        file_compiled = []
        for instruction in self.file_parsed_cleaned:
            if instruction.startswith('@'):
                instruction = self._replace_symbol_in_instruction(instruction)
            print(instruction)
            bin_instruction = self.compiler.compile(instruction)
            file_compiled.append(bin_instruction)

        self.file_compiled = file_compiled


    def _replace_symbol_in_instruction(self, instruction:str)->str:
        instruction_list = instruction.split('@')
        if len(instruction_list) > 1:
            a_value = instruction_list[1]
            if not a_value.isdigit():
                return f"@{self._replace_symbol_by_number(a_value)}"
            else:
                return f"@{a_value}"
        else:
            raise NameError(f"{instruction} is not a valid symbol")


    def _replace_symbol_by_number(self, symbol:str)->str:
        value = self.symbol_table.get_symbol_value(symbol)
        if not value:
            self.symbol_table.add_symbol(symbol, self.pointer_ram_address)
            value = self.pointer_ram_address
            self.pointer_ram_address += 1
        return value


    def _set_labels_for_symbol_table(self):
        clean_file = []
        deleted_lines = 0
        for i, instruction in enumerate(self.file_parsed):
            if instruction.startswith("(") and instruction.endswith(")"):
                label = instruction.strip("(").strip(")")
                line = i - deleted_lines
                self.symbol_table.add_symbol(label, line)
                deleted_lines += 1
                continue
            clean_file.append(instruction)
        self.file_parsed_cleaned = clean_file

    def print_compiled_file(self):
        if not self.file_compiled:
            raise NameError("File not compiled. Compile it first.")
        for instruction in self.file_compiled:
            print(instruction)

    def store_file(self):
        if not self.file_compiled:
            raise NameError("File not compiled. Compile it first.")
        
        input_path = self.path
        if input_path.endswith('.asm'):
            output_path = input_path.replace('.asm', '.hack')
        else:
            output_path = input_path + '.hack'
        
        with open(output_path, "w") as file:
            number_of_lines = len(self.file_compiled)
            for  i,instruction in enumerate(self.file_compiled):
                line_number = i+1
                file.write(instruction + '\n') if line_number < number_of_lines else file.write(instruction)

