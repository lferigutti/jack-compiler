from vm_translator.src.models import MemorySegment


class AssemblyExpressions:
  segment_strings_mapping = {
    MemorySegment.ARG: 'ARG',
    MemorySegment.LCL: 'LCL',
    MemorySegment.THIS: 'THIS',
    MemorySegment.THAT: 'THAT'
  }

  @staticmethod
  def load_constant(constant: int):
    return [f'@{constant}', "D=A"]

  def segment(self, segment):
    segment = self.segment_strings_mapping.get(segment)
    if not segment:
      raise SyntaxError(f"The segment {segment} does not exist")
    return segment
