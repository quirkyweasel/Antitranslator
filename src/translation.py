import threading
from time import sleep
from mtranslate import translate


class Translation:
    MAX_THREADS = 1
    
    def __init__(self, input_data: list, language_list: list):
        self.input_data = input_data
        self.language_list = language_list
        self.output_data = list()
        self._remaining_tasks = list()
        self._complete_tasks = list()
        self._remaining_tasks_lock = threading.Lock()
        self._complete_tasks_lock = threading.Lock()

    def translate(self):
        self._remaining_tasks = list(enumerate(self.input_data))

        overseer_thread = threading.Thread(target=self._overseer_threader)
        overseer_thread.daemon = True
        overseer_thread.start()
        for _ in range(self.MAX_THREADS):
            t = threading.Thread(target=self._translator_threader)
            t.daemon = True
            t.start()
        overseer_thread.join()

        self._complete_tasks.sort()
        self.output_data = [task[1] for task in self._complete_tasks]

        return self.output_data

    def _overseer_threader(self):
        total_tasks = len(self._remaining_tasks)
        previous_progress = -1
        while True:
            with self._complete_tasks_lock:
                complete_tasks = len(self._complete_tasks)
            current_progress = round(complete_tasks / total_tasks * 100, 2)
            if current_progress > previous_progress:
                print(current_progress, "% complete", sep="")
            previous_progress = current_progress
            if complete_tasks == total_tasks:
                break
            sleep(1)

    def _translator_threader(self):
        while not len(self._remaining_tasks) == 0:
            task = self._remaining_tasks.pop()
            result = task[0], self._translate_text(task[1])
            with self._complete_tasks_lock:
                self._complete_tasks.append(result)
            sleep(1)

    def _translate_text(self, text: str):
        current_translation = text

        for current_destination in self.language_list:
            current_translation = translate(to_translate=current_translation, to_language=current_destination)


        return current_translation
