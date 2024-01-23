import math
from itertools import product
from typing import Generator, List, Tuple, Optional

from fretboard.fretboard import Fretboard
from instruments import Guitar
from IPython.display import SVG, display
from theory import Note, TheoryMaster

theory = TheoryMaster()


class GuitarAnalyzer(Guitar):
    """
    A class that analyzes guitar positions and distances.

    Args:
        nstrings (int): The number of strings on the guitar. Default is 6.
        frets (int): The number of frets on the guitar. Default is 24.
        tuning (List[Note]): The tuning of the guitar strings. Default is standard tuning.

    Attributes:
        nstrings (int): The number of strings on the guitar.
        frets (int): The number of frets on the guitar.
        tuning (List[Note]): The tuning of the guitar strings.
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
        super().__init__(nstrings, frets, tuning)
        self.fretboard_style = {}

    def get_coordinates(self, position: int) -> Tuple[int, int]:
        """
        Returns the coordinates (string, fret) of a given position on the guitar.

        Args:
            position (int): The position on the guitar.

        Returns:
            Tuple[int, int]: The coordinates (string, fret) of the position.
        """
        return (position // self.frets, position % self.frets)

    def get_finger_combination(
        self, positions: List[int]
    ) -> Generator[Tuple[int, int], None, None]:
        """
        Yields the coordinates (string, fret) for the given positions on the guitar.

        Args:
            positions (List[int]): The positions on the guitar.

        Yields:
            Generator[Tuple[int, int], None, None]: The coordinates (string, fret) for each position.
        """
        least_distance_combination = self.compute_least_distance_combination(positions)

        for position in least_distance_combination:
            yield self.get_coordinates(position)

    def get_equivalence_classes(self, notes: List[Note]) -> Generator[int, None, None]:
        """
        Yields all positions on the guitar for the given notes.

        Args:
            notes (List[Note]): The notes to find positions for.

        Yields:
            Generator[int, None, None]: The positions on the guitar for each note.
        """
        positions = []
        for note in notes:
            positions += [
                self.notes[_note] for _note in self.notes if _note.name == note.name
            ]

        for equivalence_class in positions:
            for position in equivalence_class:
                yield self.strings[position]

    def euclidean_distance(
        self, point1: Tuple[int, int], point2: Tuple[int, int]
    ) -> float:
        """
        Computes the Euclidean distance between two points.

        Args:
            point1 (Tuple[int, int]): The coordinates of the first point.
            point2 (Tuple[int, int]): The coordinates of the second point.

        Returns:
            float: The Euclidean distance between the two points.
        """
        x1, y1 = point1
        x2, y2 = point2
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance

    def compute_distance(self, position_1: int, position_2: int) -> float:
        """
        Computes the distance between two positions on the guitar.

        Args:
            position_1 (int): The first position.
            position_2 (int): The second position.

        Returns:
            float: The distance between the two positions.
        """
        position_1_coords = (position_1 // self.frets + 1, position_1 % self.frets)
        position_2_coords = (position_2 // self.frets + 1, position_2 % self.frets)

        return self.euclidean_distance(position_1_coords, position_2_coords)

    def compute_least_distance_combination(
        self, positions_list: List[List[int]]
    ) -> List[int]:
        """
        Computes the combination of positions with the least total distance.

        Args:
            positions_list (List[List[int]]): A list of positions for each note.

        Returns:
            List[int]: The combination of positions with the least total distance.
        """
        combinations = list(product(*positions_list))
        least_distance = float("inf")
        least_distance_combination = None
        for combination in combinations:
            total_distance = sum(
                [
                    self.compute_distance(combination[i], combination[i + 1])
                    for i in range(len(combination) - 1)
                ]
            )
            if total_distance < least_distance:
                least_distance = total_distance
                least_distance_combination = combination

        return least_distance_combination

    def visualize_fretboard(
        self,
        notes: [List[Note]],
        path: str,
        color: str = "dodgerblue",
        save: bool = True,
        frets: Tuple[int, int] = (1, 12),
        fb: Optional[Fretboard] = None,
    ):
        """
        Visualizes the fretboard with markers for the given notes.

        Args:
            notes (List[List[Note]]): The notes to be visualized on the fretboard.
            path (str): The path to save the visualization.
            color (str, optional): The color of the markers. Defaults to "dodgerblue".
            save (bool, optional): Whether to save the visualization or not. Defaults to True.
            frets (Tuple[int, int], optional): The range of frets to be displayed. Defaults to (1, 12).
            fb (Optional[Fretboard], optional): The Fretboard object to use for visualization. Defaults to None.

        Returns:
            Optional[Fretboard]: The Fretboard object if `save` is False, otherwise None.
        """
        if fb is None:
            fb = Fretboard(frets=frets, style=self.fretboard_style)
        for equivalence_class in notes:
            for note in self.notes[equivalence_class]:
                string, fret = self.get_coordinates(note)
                fb.add_marker(
                    string=string,
                    fret=fret,
                    label=equivalence_class.name,
                    color=color,
                )

        if not save:
            return fb

        fb.save(path)
        display(SVG(path))
