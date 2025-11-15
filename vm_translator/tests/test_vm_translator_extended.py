import unittest
from vm_translator.src.vm_translator_class import VMTranslator
from vm_translator.src.command import Command
from vm_translator.src.models import CommandType


class TestVMTranslatorExtended(unittest.TestCase):
  """Additional unit tests for VMTranslator covering bootstrap, function, call and return translation."""

  def setUp(self):
    self.translator = VMTranslator(file_name="ExtendedTest")

  def test_get_bootstrap_code_default(self):
    code = self.translator.get_bootstrap_code()
    # Should start with bootstrap comment
    self.assertTrue(code[0].startswith("// bootstrap code"))
    # SP initialization sequence should be present
    self.assertIn("@256", code)
    self.assertIn("@SP", code)
    # Should contain a call to Sys.init (return label and jump)
    # label_counter should have incremented due to call
    self.assertEqual(self.translator.label_counter, 1)
    # Return label format
    return_labels = [line for line in code if line.startswith("(RETURN_Sys.init_")]
    self.assertEqual(len(return_labels), 1)

  def test_get_bootstrap_code_custom_stack(self):
    code = self.translator.get_bootstrap_code(stack_init_position=300)
    self.assertIn("@300", code)

  def test_get_bootstrap_code_negative_raises(self):
    with self.assertRaises(SyntaxError):
      self.translator.get_bootstrap_code(stack_init_position=-1)

  def test_translate_function_zero_locals(self):
    cmd = Command(CommandType.FUNCTION, "Main.test", 0)
    asm = self.translator._translate_function_command(cmd)
    self.assertEqual(asm, ["(Main.test)"])

  def test_translate_function_with_locals(self):
    cmd = Command(CommandType.FUNCTION, "Main.test", 3)
    asm = self.translator._translate_function_command(cmd)
    # First element is label
    self.assertEqual(asm[0], "(Main.test)")
    # There should be 3 local initializations (each produces 4 instructions)
    # Total length = 1 (label) + 3 * 4
    self.assertEqual(len(asm), 13)
    # Verify pattern of pushing 0
    zero_inits = [instr for instr in asm if instr == "M=0"]
    self.assertEqual(len(zero_inits), 3)

  def test_translate_call_command_single(self):
    cmd = Command(CommandType.CALL, "Sys.init", 0)
    initial_counter = self.translator.label_counter
    asm = self.translator._translate_call_command(cmd)
    self.assertEqual(self.translator.label_counter, initial_counter + 1)
    # Return label should be last element enclosed in parentheses
    self.assertTrue(asm[-1].startswith("(RETURN_Sys.init_"))
    # ARG repositioning should use @5 when nArgs = 0 (5 + nArgs)
    self.assertIn("@5", asm)

  def test_translate_call_command_multiple_unique_labels(self):
    cmd1 = Command(CommandType.CALL, "Foo.bar", 2)
    cmd2 = Command(CommandType.CALL, "Foo.bar", 2)
    asm1 = self.translator._translate_call_command(cmd1)
    asm2 = self.translator._translate_call_command(cmd2)
    self.assertNotEqual(asm1[-1], asm2[-1])

  def test_translate_return_command_structure(self):
    cmd = Command(CommandType.RETURN, None, None)
    asm = self.translator._translate_return_command(cmd)
    # Starts saving endFrame
    self.assertEqual(asm[0], "@LCL")
    # Contains retAddr load placeholder register R14
    self.assertIn("@R14", asm)
    # Ends with jump to retAddr
    self.assertEqual(asm[-2], "A=M")
    self.assertEqual(asm[-1], "0;JMP")


if __name__ == '__main__':
  unittest.main()
