import unittest
import tempfile
from pathlib import Path
from vm_translator.src.vm_parser import Parser
from vm_translator.src.command import Command
from vm_translator.src.models import CommandType, ArithmeticCommandTypes, MemorySegment


class TestParser(unittest.TestCase):
  """Test cases for the Parser class"""

  def setUp(self):
    """Create a temporary directory for test files"""
    self.temp_dir = tempfile.mkdtemp()

  def _create_test_file(self, content: str) -> Path:
    """Helper to create a temporary .vm file with given content"""
    file_path = Path(self.temp_dir) / "test.vm"
    with open(file_path, 'w') as f:
      f.write(content)
    return file_path

  def test_parse_arithmetic_command(self):
    """Test parsing a single arithmetic command"""
    file_path = self._create_test_file("add\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.ARITHMETIC)
    self.assertEqual(commands[0].arg1, ArithmeticCommandTypes.ADD)

  def test_parse_push_command(self):
    """Test parsing a push command"""
    file_path = self._create_test_file("push constant 7\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.PUSH)
    self.assertEqual(commands[0].arg1, MemorySegment.CONSTANT)
    self.assertEqual(commands[0].arg2, 7)

  def test_parse_pop_command(self):
    """Test parsing a pop command"""
    file_path = self._create_test_file("pop local 0\n")
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 1)
    self.assertEqual(commands[0].command_type, CommandType.POP)
    self.assertEqual(commands[0].arg1, MemorySegment.LCL)
    self.assertEqual(commands[0].arg2, 0)

  def test_parse_multiple_commands(self):
    """Test parsing multiple commands"""
    content = """push constant 7
                  push constant 8
                  add
        """
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 3)
    self.assertTrue(commands[0].is_push())
    self.assertTrue(commands[1].is_push())
    self.assertTrue(commands[2].is_arithmetic())

  def test_ignore_empty_lines(self):
    """Test that empty lines are ignored"""
    content = """push constant 7
    add
    """
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 2)

  def test_ignore_comments(self):
    """Test that comment lines are ignored"""
    content = """// This is a comment
      push constant 7
      // Another comment
      add
      """
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 2)

  def test_strip_whitespace(self):
    """Test that leading/trailing whitespace is handled"""
    content = """  push constant 7  
      add  
    """
    file_path = self._create_test_file(content)
    parser = Parser(file_path)
    commands = parser.parse()

    self.assertEqual(len(commands), 2)

  def test_invalid_arithmetic_command(self):
    """Test that invalid arithmetic commands raise SyntaxError"""
    file_path = self._create_test_file("invalid\n")
    parser = Parser(file_path)

    with self.assertRaises(SyntaxError):
      parser.parse()

  def test_invalid_memory_command(self):
    """Test that invalid memory commands raise SyntaxError"""
    file_path = self._create_test_file("invalid constant 7\n")
    parser = Parser(file_path)

    with self.assertRaises(SyntaxError):
      parser.parse()

  def test_invalid_memory_segment(self):
    """Test that invalid memory segments raise SyntaxError"""
    file_path = self._create_test_file("push invalid 7\n")
    parser = Parser(file_path)

    with self.assertRaises(SyntaxError):
      parser.parse()


if __name__ == '__main__':
  unittest.main()
