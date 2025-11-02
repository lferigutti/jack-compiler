import os
import tomllib

class SymbolTable:
    CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    TABLE_FILE_PATH = os.path.join(CURRENT_DIRECTORY, "config", "symbolic_defaults.toml")

    def __init__(self):
        self._default_table = {}
        self._load_table_from_file()
        self.table = self._default_table.get("symbols")


    def _load_table_from_file(self):
        with open(self.TABLE_FILE_PATH, 'rb') as f:
            self._default_table = tomllib.load(f)


    def get_symbol_value(self, symbol):
        return self.table.get(symbol)


    def add_symbol(self, symbol, value):
        if symbol not in self.table.keys():
            self.table[symbol] = value
        else:
            raise KeyError(f"Symbol {symbol} already exists")

