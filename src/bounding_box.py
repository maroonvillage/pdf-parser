from typing import Tuple

class BoundingBox:
    """
    Represents a bounding box with an ID and two coordinate pairs.

    Attributes:
        id (str): A unique identifier for the bounding box.
        coordinates (Tuple[Tuple[float, float], Tuple[float, float]]): A tuple of two coordinate pairs,
                                                                       where each pair is a tuple of (x, y) floats.
    """
    def __init__(self, id: str, coordinates: Tuple[Tuple[float, float], Tuple[float, float]]):
        """Initializes a new BoundingBox object with the given ID and coordinates."""
        self.id = id
        self.coordinates = coordinates

    def __str__(self):
        """Returns a string representation of the BoundingBox."""
        (x0,y0), (x1,y1) = self.coordinates
        return f"BoundingBox(id='{self.id}', coordinates=((x0:{x0},y0:{y0}), (x1:{x1},y1:{y1})))"
    
    @property
    def x0(self):
        """Returns the x0 coordinate of the bounding box."""
        return self.coordinates[0][0]
    
    @property
    def y0(self) -> float:
        """Returns the y0 coordinate of the bounding box."""
        return self.coordinates[0][1]
    
    @property
    def x1(self):
        """Returns the x1 coordinate of the bounding box."""
        return self.coordinates[1][0]
    
    @property
    def y1(self):
        """Returns the y1 coordinate of the bounding box."""
        return self.coordinates[1][1]
    
    def __repr__(self):
       """Returns a detailed string representation of the BoundingBox."""
       return self.__str__()