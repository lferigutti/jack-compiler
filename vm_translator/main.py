#!/usr/bin/env python3
"""
VM Translator - Translates VM code to Hack assembly language
"""
import argparse
import sys
from pathlib import Path

from vm_translator.src.code_writer import CodeWriter
from vm_translator.src.vm_parser import Parser
from vm_translator.src.vm_translator_class import VMTranslator


def main():
  """Main entry point for the VM translator"""
  parser = argparse.ArgumentParser(
    description='Translate VM code to Hack assembly language'
  )

  parser.add_argument(
    'input',
    type=str,
    help='Input .vm file or directory containing .vm files'
  )

  parser.add_argument(
    '-o', '--output',
    type=str,
    help='Output .asm file (default: input filename with .asm extension)',
    default=None
  )

  args = parser.parse_args()

  # Validate input path exists
  input_path = Path(args.input)
  if not input_path.exists():
    print(f"Error: Input path '{args.input}' does not exist", file=sys.stderr)
    sys.exit(1)

  # Determine output path
  if args.output:
    output_path = Path(args.output)
  else:
    if input_path.is_file():
      output_path = input_path.with_suffix('.asm')
    else:
      output_path = input_path / f"{input_path.name}.asm"

  print(f"Input: {input_path}")
  print(f"Output: {output_path}")
  translate(input_path, output_path)


def translate(input_path: Path, output_path):
  print("Starting the Translation")
  parser = Parser(input_path)
  parsed_file = parser.parse()
  translator = VMTranslator()
  translation = translator.translate(parsed_file)
  code_writer = CodeWriter(output_file=output_path)
  code_writer.write_file(translation)


if __name__ == '__main__':
  main()
