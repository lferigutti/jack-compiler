#!/usr/bin/env python3
"""
VM Translator - Translates VM code to Hack assembly language
"""

import argparse
import os
import sys
from pathlib import Path

from vm_translator.src.code_writer import CodeWriter
from vm_translator.src.vm_parser import Parser
from vm_translator.src.vm_translator_class import VMTranslator


def load_env_file(env_path=".env"):
  """Load environment variables from .env file"""
  if not os.path.exists(env_path):
    return

  with open(env_path, "r") as f:
    for line in f:
      line = line.strip()
      # Skip empty lines and comments
      if not line or line.startswith("#"):
        continue
      # Parse KEY=VALUE
      if "=" in line:
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip()


def main():
  """Main entry point for the VM translator"""
  # Load .env file for local debugging
  # load_env_file("/Users/leonardoferigutti/Documents/nand2Tetris/nand2tetris/vm_translator/.env")

  parser = argparse.ArgumentParser(
    description="Translate VM code to Hack assembly language"
  )

  parser.add_argument(
    "input",
    type=str,
    nargs="?",
    help="Input .vm file or directory containing .vm files",
    default=None,
  )

  parser.add_argument(
    "-o",
    "--output",
    type=str,
    help="Output .asm file (default: input filename with .asm extension)",
    default=None,
  )

  args = parser.parse_args()

  # Use input argument or fall back to INPUT_PATH environment variable
  input_str = args.input or os.getenv("INPUT_PATH")
  print(input_str)

  if not input_str:
    print(
      "Error: No input provided. Use argument or set INPUT_PATH environment variable",
      file=sys.stderr,
    )
    sys.exit(1)

  input_path = Path(input_str)
  if not input_path.exists():
    print(f"Error: Input path '{input_str}' does not exist", file=sys.stderr)
    sys.exit(1)

  # Determine output path
  if args.output:
    output_path = Path(args.output)
  else:
    if input_path.is_file():
      output_path = input_path.with_suffix(".asm")
    else:
      output_path = input_path / f"{input_path.name}.asm"

  print(f"Input: {input_path}")
  print(f"Output: {output_path}")
  translate(input_path, output_path)


def get_file_name(input_path: Path):
  return input_path.name.split(".")[0]


def get_files_from_dir(input_path: Path):
  return list(input_path.glob("*.vm"))


def translate(input_path: Path, output_path):
  if input_path.is_dir():
    files = get_files_from_dir(input_path)
  else:
    files = [input_path]

  translation = []
  if len(files) >= 1:
    translator_init = VMTranslator()
    translation.extend(translator_init.get_bootstrap_code())
  for file in files:
    parser = Parser(file)
    file_name = get_file_name(file)
    parsed_file = parser.parse()
    translator = VMTranslator(file_name=file_name)
    translation.extend(translator.translate(parsed_file))

  code_writer = CodeWriter(output_file=output_path)
  code_writer.write_file(translation)


if __name__ == "__main__":
  main()
