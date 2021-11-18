import os.path
from timer import Timer

swap_suffix = ".swp"
EXTENSION = ".txt"


def save_content(filepath, content_iter):
    with open(filepath, "w") as f:
        for line in content_iter:
            f.write(line)
            f.write("\n")


class TargetFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tmp_filepath = filepath + swap_suffix

    def save_content(self, content, to_swap=False):
        filepath = self._filepath(to_swap)
        save_content(filepath, content)

    def _filepath(self, use_swap):
        if use_swap:
            return self.tmp_filepath
        else:
            return self.filepath

    def load_content(self, document, from_swap=False):
        filepath = self._filepath(from_swap)
        with open(filepath, "r") as f:
            for line in f:
                document.append_line(list(line.rstrip()))


class FileManager:
    def __init__(self, general_config):
        self.current_file = None
        self.config = general_config["files"]

        self.swap_timer = Timer(5000)
        self.tmp_timer = Timer(1000)

    def manual_save(self, document):
        if self.current_file is not None:
            self.current_file.save_content(document.to_content_iter(), to_swap=False)

    def update(self, document):
        ## Maybe save to tmp file, and to swap
        if self.swap_timer.update() and self.current_file is not None:
            self.current_file.save_content(document.to_content_iter(), to_swap=True)
            self.swap_timer.drain()

        if self.tmp_timer.update():
            save_content(self.config["temp_file_path"], document.to_content_iter())
            self.tmp_timer.drain()

    def load_file(self, filename, document):
        filepath = os.path.join(self.config["file_directory"], filename)
        file = TargetFile(filepath)
        document.clear(hard=True)
        file.load_content(document)
        self.current_file = file

    def find_files(self):
        with os.scandir(self.config["file_directory"]) as scan_dir:
            files = [f.name for f in scan_dir if f.is_file()]
        files = [f for f in files if f.endswith(EXTENSION)]
        return files
