import os
from typing import List, Tuple
import subprocess

from theory import Note


class Notation:
    """
    Represents a musical notation.

    Args:
        path (str): The path where the notation file will be saved.
        notes (List[Note]): The list of notes to be included in the notation.

    Attributes:
        path (str): The path where the notation file will be saved.
        notes (List[Note]): The list of notes to be included in the notation.
        convert (dict): A dictionary mapping note modifiers to LilyPond syntax.
        file_path (str): The file path of the generated notation file.
        image_path (str): The file path of the generated notation image.
    """

    def __init__(self, path: str, notes: List[Note]):
        self.path: str = path
        self.notes: List[Note] = notes
        self.convert = {"#": "is", "b": "es"}
        self.file_path, self.image_path = self.generate_notation()

    def generate_notation(self) -> Tuple[str, str]:
        """
        Generates the notation file and image.

        Returns:
            Tuple[str, str]: The file path of the notation file and the image file.
        """
        version_txt = '\\version "2.24.3"\n'
        relative = "\\relative {\n"
        note_txt = ""
        for note in self.notes:
            note_txt += f" {note.name[0].lower()}"
            if len(note.name) > 1:
                note_txt += f"{self.convert[note.name[1]]}"
            if note.name == self.notes[1].name:
                note_txt += "'"

        text = version_txt + relative + note_txt + "\n}"
        fpath = os.path.join(self.path, "temp.txt")

        with open(fpath, "w") as file:
            file.write(text)
        self.run()

        return fpath, os.path.join(self.path, "temp.png")

    def run(self):
        """
        Runs the LilyPond command to generate the notation image.
        """
        subprocess.run(
            [
                "lilypond",
                "-o",
                os.path.join(self.path, "temp"),
                "-fpng",
                os.path.join(self.path, "temp.txt"),
            ]
        )
