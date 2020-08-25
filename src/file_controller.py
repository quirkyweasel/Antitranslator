import pysubs2


class FileController:
    def __init__(self, file_path: str, destination_path: str, ignore_ass_styles=frozenset()):
        self.file_path = file_path
        self.destination_path = destination_path
        self.file_format = file_path[file_path.rfind('.') + 1:]
        self.normal_lines = list()
        self.ignore_lines = list()
        self.normal_lines_order = list()
        self.ignore_lines_order = list()
        self.ignore_ass_styles = ignore_ass_styles

    def load_data(self):
        if self.file_format == "txt":
            with open(self.file_path, 'r', encoding="utf-8") as input_file:
                input_data = input_file.read().splitlines()
            for i in range(len(input_data)):
                if not input_data[i].startswith("#"):
                    self.normal_lines.append(input_data[i])
                    self.normal_lines_order.append(i)
                else:
                    self.ignore_lines.append(input_data[i])
                    self.ignore_lines_order.append(i)
        elif self.file_format == "ass" or self.file_format == "srt":
            input_file = pysubs2.load(self.file_path)
            for i in range(len(input_file)):
                line = input_file[i]
                if line.is_comment is False and line.style not in self.ignore_ass_styles:
                    self.normal_lines.append(line.plaintext)
                    self.normal_lines_order.append(i)
                else:
                    self.ignore_lines.append(line.plaintext)
                    self.ignore_lines_order.append(i)
        return self.normal_lines

    def save_data(self, output_data):
        self.normal_lines = output_data
        full_data = self._combine_data()
        if self.file_format == "txt":
            with open(self.destination_path, 'w', encoding="utf-8") as output_file:
                output_file.write("\n".join(full_data))
        elif self.file_format == "ass" or self.file_format == "srt":
            output_file = pysubs2.load(self.file_path)
            for line in output_file:
                line.text = full_data.pop(0)
            output_file.save(self.destination_path)

    def _combine_data(self):
        full_data = list()
        while len(self.normal_lines_order + self.ignore_lines_order) > 0:
            if len(self.normal_lines_order) > 0 and len(self.ignore_lines_order) > 0:
                if self.normal_lines_order[0] < self.ignore_lines_order[0]:
                    full_data.append(self.normal_lines.pop(0))
                    self.normal_lines_order.pop(0)
                else:
                    full_data.append(self.ignore_lines.pop(0))
                    self.ignore_lines_order.pop(0)
            elif len(self.normal_lines_order) > 0:
                full_data += self.normal_lines
                self.normal_lines_order = list()
            else:
                full_data += self.ignore_lines
                self.ignore_lines_order = list()
        return full_data
