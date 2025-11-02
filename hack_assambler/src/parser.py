
class Parser:
    def __init__(self, file:str):
        self.file_str = file

    def parse(self):
        clean_file = []
        with open(self.file_str, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith("//"):
                    continue
                elif line == "":
                    continue
                else:
                    line_clean = self._clean_line(line)
                    clean_file.append(line_clean)
            return clean_file


    def _clean_line(self, line:str):
        line = line.strip()
        return line
