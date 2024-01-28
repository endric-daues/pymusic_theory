import math
from abc import abstractmethod
from itertools import product
from typing import Dict, List

from theory import Note, TheoryMaster

theory = TheoryMaster()


class Instrument:
    """
    Represents a musical instrument.

    Attributes:
        name (str): The name of the instrument.
        notes (Dict[Note, List[int]]): A dictionary mapping notes to a list of integers
        representing the positions where the note can be played.
    """

    def __init__(self, name: str):
        self.name = name
        self.notes: Dict[Note, List[int]] = {}

    @abstractmethod
    def _initiate(self):
        """
        Abstract method to initialize the instrument.
        """

    @abstractmethod
    def play(self, notes: List[Note]) -> List[int]:
        """
        Abstract method to play a list of notes on the instrument.

        Args:
            notes (List[Note]): The list of notes to be played.
        """


class Piano(Instrument):
    """This class represents a piano instrument.
    Args:
        num_keys (int): The number of keys on the piano. Default is 88.
        low_note (Note): The lowest note on the piano. Default is A0.
    Attributes:
        num_keys (int): The number of keys on the piano.
        low_note (Note): The lowest note on the piano.
        keys (Dict[int, Note]): A dictionary mapping key
                                numbers to notes on the piano.
        notes (Dict[Note, int]): A dictionary mapping notes
                                 to key numbers on the piano.

    """

    def __init__(self, num_keys: int = 88, low_note: Note = Note("A", 27.5)):
        super().__init__("piano")
        self.low_note = low_note
        self.num_keys = num_keys
        self.keys: Dict[int, Note] = {}
        self.notes: Dict[Note, int] = {}
        self._initiate()

    def _initiate(self):
        """
        Initialize the keys and notes mapping for the piano.
        """
        note = self.low_note
        for i, note_name in enumerate(
            theory.note_stream(self.low_note.name, n=self.num_keys)
        ):
            if i != 0:
                note = Note(note_name, theory.get_pitch(note.pitch, 1))
            self.keys[i] = note
            self.notes[note] = i

    def play(self, notes: List[Note]) -> List[int]:
        """
        Play a list of notes on the piano and return the corresponding key numbers.

        Args:
            notes (List[Note]): The notes to be played.

        Returns:
            List[int]: The key numbers corresponding to the played notes.
        """
        return [self.notes.get(note) for note in notes]


class Guitar(Instrument):
    """
    Represents a guitar instrument.

    Args:
        nstrings (int): The number of strings on the guitar. Default is 6.
        frets (int): The number of frets on the guitar. Default is 24.
        tuning (List[Note]): The tuning of the guitar strings.
        Default is standard tuning.

    Attributes:
        nstrings (int): The number of strings on the guitar.
        frets (int): The number of frets on the guitar.
        tuning (List[Note]): The tuning of the guitar strings.
        strings (Dict[int, Note]): A dictionary mapping positions
        to notes on the guitar strings.
        notes (Dict[Note, List[int]]): A dictionary mapping notes to
        their positions on the guitar.
    """

    def __init__(
        self,
        nstrings: int = 6,
        frets: int = 24,
        tuning: List[Note] = [
            Note("E", 82.41),
            Note("A", 110.00),
            Note("D", 146.83),
            Note("G", 196.00),
            Note("B", 246.94),
            Note("E", 329.63),
        ],  # standard tuning
    ):
        super().__init__("guitar")
        self.nstrings = nstrings
        self.frets = frets
        self.tuning = tuning
        self.strings: Dict[int, Note] = {}
        self.notes: Dict[Note, List[int]] = {}
        self._initiate()

    def _initiate(self):
        for string, open_string_note in enumerate(self.tuning):
            for fret in range(self.frets):
                position = (string * self.frets) + fret
                note = Note(
                    theory.notes[
                        (theory.notes.index(open_string_note.name) + fret) % 12
                    ],
                    theory.get_pitch(open_string_note.pitch, fret),
                )
                self.strings[position] = note

                if note not in self.notes:
                    self.notes[note] = [position]
                else:
                    self.notes[note].append(position)

    def play(self, notes: List[Note]) -> List[List[int]]:
        """
        Returns the positions of the given notes on the guitar.

        Args:
            notes (List[Note]): The notes to be played on the guitar.

        Returns:
            List[List[int]]: A list of positions for each note in the input list.
        """
        return [self.notes.get(note) for note in notes]
