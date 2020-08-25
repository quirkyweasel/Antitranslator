from src import *


class Application:
    def __init__(self):
        create_folder("input")
        create_folder("output")
        self.input_file_list = get_input_file_list()
        self.translation_depth = 128
        self.output_language = "ru"
        self.ignore_ass_styles = {"Credits", "Lyrics OP1 Jap", "Credits2", "Credits_Episode_10", "Lyrics OP2 Jap"}
        self.language_list = generate_language_list(depth=self.translation_depth, end_language=self.output_language)
        self.reset_language_list = True

    def run(self):
        for file_path in self.input_file_list:
            print(get_file_name(file_path), "start")
            file = FileController(file_path, input_to_output(file_path), ignore_ass_styles=self.ignore_ass_styles)
            input_data = file.load_data()
            output_data = Translation(input_data, self.language_list).translate()
            create_folder(input_to_output(get_directory(file_path)))
            file.save_data(output_data)
            print(get_file_name(file_path), "complete")
            with open("output\\log.txt", "a") as output_config:
                generate_log(output_config, file_path, self.language_list)
            if self.reset_language_list:
                self.language_list = generate_language_list(depth=self.translation_depth,
                                                            end_language=self.output_language)


if __name__ == "__main__":
    application = Application()
    application.run()
