import numpy as np


class Factor:
    """
    Contains different metrics for the LinearClusterization algorithm.

    Attributes:
    ----------
    list_of_distances: list or tuple
        A list or tuple that stores distances from point to line.

    Methods:
    -------
    max_mean:
        Divides the maximum value of the list_of_distances by the 
        average value.
    """

    def __init__(self, list_of_distances):
        self.list_of_distances = list_of_distances

    @property
    def list_of_distances(self):
        return self._list_of_distances

    @list_of_distances.setter
    def list_of_distances(self, value):
        if not isinstance(value, (tuple, list)):
            raise TypeError(
                "The list_of_distances parameter must be of type tuple or "
                f"list, not {type(value).__name__}.")

        for distance in value:
            if not isinstance(distance, (int, float)):
                raise TypeError(
                    "Elements inside the list_of_distances must be of type"
                    f"int or float, not {type(distance).__name__}.")

        self._list_of_distances = value

    def max_mean(self) -> float:
        """
        Divides the maximum value of the list_of_distances by the 
        average value.

        Returns:
        -------
        float
        """

        return np.max(self.list_of_distances) / np.mean(self.list_of_distances)
