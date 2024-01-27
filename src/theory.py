from abc import abstractmethod
from typing import List, Literal


class Note:
    """
    Represents a musical note.

    Attributes:
        name (str): The name of the note.
        pitch (float): The pitch of the note.

    Methods:
        __str__(): Returns a string representation of the note.
        __eq__(other): Checks if the note is equal to another note.
        __ne__(other): Checks if the note is not equal to another note.
        __hash__(): Returns the hash value of the note.
    """

    def __init__(self, name: str, pitch: float):
        self.name: str = name
        self.pitch: float = pitch

    def __str__(self):
        return f"Note(name='{self.name}', pitch={self.pitch:.0f})"

    def __eq__(self, other):
        return round(self.pitch, 0) == round(other.pitch, 0)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name, round(self.pitch, 0)))


class Scale:
    """
    Represents a musical scale.

    Attributes:
        name (str): The name of the scale.
        base_note (Note): The base note of the scale.
        intervals (List[int]): The intervals of the scale.
        notes (List[Note]): The notes in the scale.

    Methods:
        generate_scale(): Generates the scale based on the base note and intervals.
        __iter__(): Returns an iterator for the scale.
        __str__(): Returns a string representation of the scale.

    """

    def __init__(self, name: str, base_note: Note, intervals: List[int]) -> List[Note]:
        self.name: str = name
        self.base_note: Note = base_note
        self.intervals: List[int] = intervals
        self.notes: List[Note] = []  # TODO: rethink this
        self.generate_scale()

    def generate_scale(self):
        """
        Generate a scale based on the base note and intervals.

        Returns:
            List[Note]: A list of notes in the scale.
        """
        theory = TheoryMaster()
        self.notes.append(self.base_note)
        current_note = self.base_note
        current_index = theory.notes.index(self.base_note.name)

        for interval in self.intervals[:-1]:
            next_pitch = theory.get_pitch(current_note.pitch, interval)
            current_index += interval
            next_note = Note(theory.notes[current_index % 12], next_pitch)
            self.notes.append(next_note)
            current_note = next_note

    def __getitem__(self, index: int):
        return self.notes[(index - 1) % len(self.notes)]

    def __iter__(self):
        return iter(self.notes)

    def __str__(self):
        return f"{[str(note) for note in self.notes]}"


class TheoryMaster:
    """
    A class for music theory constants and standard calculations.

    Attributes:
        notes_in_octave (int): The number of notes in an octave.
        notes (List[str]): The list of notes in the octave.
        major_intervals (List[int]): The intervals for a major scale.
        minor_intervals (List[int]): The intervals for a minor scale.
    """

    def __init__(self):
        self.notes_in_octave: int = 8
        self.notes: List[str] = [
            "C",
            "C#",
            "D",
            "Eb",
            "E",
            "F",
            "F#",
            "G",
            "G#",
            "A",
            "Bb",
            "B",
        ]
        self.modes = [
            "ionian",
            "dorian",
            "phrygian",
            "lydian",
            "mixolydian",
            "aeolian",
            "locrian",
        ]
        self.major_intervals: List[int] = [2, 2, 1, 2, 2, 2, 1]
        self.minor_intervals: List[int] = [2, 1, 2, 2, 1, 2, 2]
        self.dim_intervals: List[int] = [2, 1, 2, 1, 2, 1, 2]

    def get_mode_intervals(self, mode: str):
        """
        Returns the intervals of the specified mode.

        Args:
            mode (str): The mode for which to retrieve the intervals.

        Returns:
            list: A list of intervals representing the specified mode.

        Raises:
            ValueError: If an invalid mode is provided.
        """
        if mode not in self.modes:
            raise ValueError(f"Invalid mode: {mode}")
        else:
            return self.invert(self.major_intervals, self.modes.index(mode))

    def note_stream(self, starting_note: str, n: int = 12):
        """
        Generates a stream of musical notes starting from the given note.

        Args:
            starting_note (str): The starting note of the stream.
            n (int, optional): The number of notes to generate. Defaults to 12.

        Yields:
            str: The next note in the stream.

        """
        index = self.notes.index(starting_note)
        for _ in range(n):
            yield self.notes[index % 12]
            index += 1

    @abstractmethod
    def get_pitch(self, pitch: float, interval: int) -> float:
        """
        Calculates the pitch after applying the specified interval using equal temperament.

        Args:
            pitch (float): The initial pitch value in Hz.
            interval (int): The interval to apply to the pitch.

        Returns:
            float: pitch in Hz.
        """
        return ((2 ** (1 / 12)) ** interval) * pitch

    @abstractmethod
    def get_triad_intervals(
        self, interval: Literal["major", "minor"], inversion: int = 0
    ):
        """
        Get the intervals of a triad.

        Args:
            interval (Literal["major", "minor"]): The type of triad interval.
            inversion (int, optional): The inversion of the triad. Defaults to 0.

        Returns:
            List[int]: The intervals of the triad.

        Raises:
            ValueError: If an invalid triad type is provided.
        """
        if interval == "major":
            return self.invert([0, 4, 7], inversion)
        elif interval == "major_7":
            return self.invert([0, 4, 7, 11], inversion)
        elif interval == "minor":
            return self.invert([0, 3, 7], inversion)
        elif interval == "minor_7":
            return self.invert([0, 3, 7, 10], inversion)
        elif interval == "dom_7":
            return self.invert([0, 4, 7, 10], inversion)
        elif interval == "dim":
            return self.invert([0, 3, 6], inversion)
        else:
            raise ValueError(f"Invalid triad type: {interval}")

    @abstractmethod
    def invert(self, intervals: List[int], n: int):
        """
        Inverts the given list of intervals by adding 12 to each interval
        and appending it to the end of the note list.

        Args:
            intervals (List[int]): The list of intervals to be inverted.
            n (int): The number of times the inversion should be performed.

        Returns:
            List[int]: The inverted list of intervals.
        """
        for i in range(n):
            base = intervals.pop(0) + 12
            intervals.append(base)

        return intervals

    def get_triad(
        self,
        note: Note,
        intervals: List[int],
    ) -> List[Note]:
        """
        Get a triad based on a given note and intervals.

        Note: if the triad is inverted, the base note frequncy
        will not match any of the frequencies in the triad.

        Args:
            note (Note): The base note of the triad.
            intervals (List[int]): The intervals to apply to the base note.

        Returns:
            List[Note]: The triad notes.
        """
        return [
            Note(
                self.notes[(self.notes.index(note.name) + interval) % 12],
                self.get_pitch(note.pitch, intervals[i]),
            )
            for i, interval in enumerate(intervals)
        ]
