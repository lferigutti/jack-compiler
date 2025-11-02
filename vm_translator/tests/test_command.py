import unittest
from vm_translator.src.command import Command
from vm_translator.src.models import CommandType, ArithmeticCommandTypes, MemorySymbol


class TestCommand(unittest.TestCase):
    """Test cases for the Command class"""

    def test_arithmetic_command_creation(self):
        """Test creating an arithmetic command"""
        cmd = Command(
            command_type=CommandType.ARITHMETIC,
            arg1=ArithmeticCommandTypes.ADD
        )
        self.assertEqual(cmd.command_type, CommandType.ARITHMETIC)
        self.assertEqual(cmd.arg1, ArithmeticCommandTypes.ADD)
        self.assertIsNone(cmd.arg2)

    def test_push_command_creation(self):
        """Test creating a push command"""
        cmd = Command(
            command_type=CommandType.PUSH,
            arg1=MemorySymbol.CONSTANT,
            arg2=7
        )
        self.assertEqual(cmd.command_type, CommandType.PUSH)
        self.assertEqual(cmd.arg1, MemorySymbol.CONSTANT)
        self.assertEqual(cmd.arg2, 7)

    def test_pop_command_creation(self):
        """Test creating a pop command"""
        cmd = Command(
            command_type=CommandType.POP,
            arg1=MemorySymbol.LCL,
            arg2=0
        )
        self.assertEqual(cmd.command_type, CommandType.POP)
        self.assertEqual(cmd.arg1, MemorySymbol.LCL)
        self.assertEqual(cmd.arg2, 0)

    def test_str_arithmetic_command(self):
        """Test string representation of arithmetic commands"""
        cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
        self.assertEqual(str(cmd), "add")

        cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.SUB)
        self.assertEqual(str(cmd), "sub")

        cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.NEG)
        self.assertEqual(str(cmd), "neg")

    def test_str_push_command(self):
        """Test string representation of push commands"""
        cmd = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 7)
        self.assertEqual(str(cmd), "push constant 7")

        cmd = Command(CommandType.PUSH, MemorySymbol.LCL, 0)
        self.assertEqual(str(cmd), "push local 0")

        cmd = Command(CommandType.PUSH, MemorySymbol.ARG, 2)
        self.assertEqual(str(cmd), "push argument 2")

    def test_str_pop_command(self):
        """Test string representation of pop commands"""
        cmd = Command(CommandType.POP, MemorySymbol.LCL, 0)
        self.assertEqual(str(cmd), "pop local 0")

        cmd = Command(CommandType.POP, MemorySymbol.THAT, 5)
        self.assertEqual(str(cmd), "pop that 5")

    def test_repr(self):
        """Test repr representation"""
        cmd = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 7)
        repr_str = repr(cmd)
        self.assertIn("Command", repr_str)
        self.assertIn("CommandType.PUSH", repr_str)
        self.assertIn("MemorySymbol.CONSTANT", repr_str)
        self.assertIn("7", repr_str)

    def test_eq_same_commands(self):
        """Test equality of identical commands"""
        cmd1 = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 7)
        cmd2 = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 7)
        self.assertEqual(cmd1, cmd2)

    def test_eq_different_commands(self):
        """Test inequality of different commands"""
        cmd1 = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 7)
        cmd2 = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 8)
        self.assertNotEqual(cmd1, cmd2)

        cmd3 = Command(CommandType.POP, MemorySymbol.CONSTANT, 7)
        self.assertNotEqual(cmd1, cmd3)

        cmd4 = Command(CommandType.PUSH, MemorySymbol.LCL, 7)
        self.assertNotEqual(cmd1, cmd4)

    def test_eq_with_non_command(self):
        """Test equality with non-Command objects"""
        cmd = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 7)
        self.assertNotEqual(cmd, "not a command")
        self.assertNotEqual(cmd, 42)
        self.assertNotEqual(cmd, None)

    def test_is_arithmetic(self):
        """Test is_arithmetic method"""
        cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
        self.assertTrue(cmd.is_arithmetic())

        cmd = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 7)
        self.assertFalse(cmd.is_arithmetic())

    def test_is_push(self):
        """Test is_push method"""
        cmd = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 7)
        self.assertTrue(cmd.is_push())

        cmd = Command(CommandType.POP, MemorySymbol.LCL, 0)
        self.assertFalse(cmd.is_push())

        cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
        self.assertFalse(cmd.is_push())

    def test_is_pop(self):
        """Test is_pop method"""
        cmd = Command(CommandType.POP, MemorySymbol.LCL, 0)
        self.assertTrue(cmd.is_pop())

        cmd = Command(CommandType.PUSH, MemorySymbol.CONSTANT, 7)
        self.assertFalse(cmd.is_pop())

        cmd = Command(CommandType.ARITHMETIC, ArithmeticCommandTypes.ADD)
        self.assertFalse(cmd.is_pop())

    def test_all_arithmetic_commands(self):
        """Test all arithmetic command types"""
        arithmetic_ops = [
            (ArithmeticCommandTypes.ADD, "add"),
            (ArithmeticCommandTypes.SUB, "sub"),
            (ArithmeticCommandTypes.NEG, "neg"),
            (ArithmeticCommandTypes.EQ, "eq"),
            (ArithmeticCommandTypes.GT, "gt"),
            (ArithmeticCommandTypes.LT, "lt"),
            (ArithmeticCommandTypes.AND, "and"),
            (ArithmeticCommandTypes.OR, "or"),
            (ArithmeticCommandTypes.NOT, "not"),
        ]

        for op, expected_str in arithmetic_ops:
            with self.subTest(op=op):
                cmd = Command(CommandType.ARITHMETIC, op)
                self.assertEqual(str(cmd), expected_str)
                self.assertTrue(cmd.is_arithmetic())

    def test_all_memory_segments(self):
        """Test all memory segment types"""
        segments = [
            MemorySymbol.LCL,
            MemorySymbol.ARG,
            MemorySymbol.THIS,
            MemorySymbol.THAT,
            MemorySymbol.TEMP,
            MemorySymbol.POINTER,
            MemorySymbol.STATIC,
            MemorySymbol.CONSTANT,
        ]

        for segment in segments:
            with self.subTest(segment=segment):
                cmd = Command(CommandType.PUSH, segment, 0)
                self.assertIn(segment.value, str(cmd))
                self.assertTrue(cmd.is_push())


if __name__ == '__main__':
    unittest.main()
