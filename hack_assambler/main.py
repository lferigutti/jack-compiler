import os.path
from src.hack_assambler import HackAssambler

def main():
    path = "/Users/leonardoferigutti/Documents/nand2Tetris/hack-assambler/tests/test_files"
    add_file = os.path.join(path, "Pong.asm")
    assambler = HackAssambler(add_file)
    assambler.parse()
    print(assambler.file_parsed)
    assambler.compile()
    print(assambler.file_parsed_cleaned)
    assambler.print_compiled_file()
    assambler.store_file()

if __name__ == "__main__":
    main()