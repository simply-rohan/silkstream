"""
# dbclient
A simple but pwerful way to manage local databases in Python!
"""

import os
import threading
import json

lock = threading.Lock()


class Directory:
    def __init__(self, path) -> None:
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        self.path = path

    def __getitem__(self, item):
        # Determine of item is a file or directory
        # all_files = [
        #    name.replace(".json", "") for name in all_items if os.path.isfile(os.path.join(self.path, name))
        # ]
        filenames = [
            name.replace(".json", "") for name in next(os.walk(self.path))[2]
        ]  # [] if no file

        # TODO: The system of checking if the target is a file is a rushed and cheeky
        # It's purpose it to allow users to enter the entry name with out having to add the .json suffix

        if item in filenames:
            return File(os.path.join(self.path, item.replace(".json", "") + ".json"))
        else:
            return Directory(os.path.join(self.path, item))

    def __setitem__(self, item, value: dict):
        # Only to be used on files
        with lock:
            all_folders = [
                folder
                for folder in os.listdir(self.path)
                if os.path.isdir(os.path.join(self.path, folder))
            ]
            if item not in all_folders:
                with open(
                    os.path.join(self.path, item.replace(".json", "") + ".json"), "w"
                ) as file:
                    json.dump(value, file)

    def __repr__(self):
        return self.path + " Quick Look: \n\t" + "\n\t".join(os.listdir(self.path))


class File(dict):
    def __init__(self, path) -> None:
        self.path = path

        with lock:
            with open(self.path, "r") as file:
                super().__init__(json.load(file))

    def push(self):
        with lock:
            with open(self.path, "w") as file:
                json.dump(super().copy(), file, indent=4)
