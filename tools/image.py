import os

import cv2
import numpy as np

from tools.coordinate import Coordinate


class Image:
    """
    An instance of the Image class stores information about an image.

    Attributes:
    ----------
    height: int
        The image's height.

    width: int
        The image's width.

    path: str
        The path to the image.

    list_of_coordinates: list
        A list with marked coordinates. The list must contain objects
        of type Coordinate.

    Methods:
    ----------
    append_coordinate
    """

    def __init__(self, path: str):
        self.path = path
        self.list_of_coordinates = []

    @property
    def height(self):
        return cv2.imread(self.path).shape[0]

    @property
    def width(self):
        return cv2.imread(self.path).shape[1]

    @property
    def list_of_coordinates(self):
        return self._list_of_coordinates

    @list_of_coordinates.setter
    def list_of_coordinates(self, value):
        if isinstance(value, list):
            self._list_of_coordinates = value

        else:
            raise TypeError(
                "The list_of_coordinates parameter must be of type list, "
                f"not {type(value).__name__}.")

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, given_path):
        if isinstance(given_path, str):
            if os.path.exists(given_path):
                if (given_path.split(sep=".")[-1] in (
                        "jpg", "jpeg", "png", "bmp")):
                    self._path = given_path

            else:
                raise FileNotFoundError(
                    "The path does not exist.")

        else:
            raise TypeError(
                "The path attribute must be of type str, "
                f"not {type(given_path).__name__}.")

    def append_coordinate(self, coord: Coordinate):
        """
        Adds an instance of the Coordinate class to the object's 
        list_of_coordinates.

        Parameters
        ----------
        coord:
            An instance of class Coordinate.

        Returns
        -------
        None
        """
        if isinstance(coord, Coordinate):
            if coord.x > self.width:
                raise ValueError(
                    "x-coordinate cannot be greater than image width.")

            if coord.y > self.height:
                raise ValueError(
                    "y-coordinate cannot be greater than image height.")

            if (coord.x <= self.width and coord.y <= self.height):
                self.list_of_coordinates.append(coord)

        else:
            raise TypeError(
                "The coord parameter must be of type Coordinate, "
                f"not {type(coord).__name__}.")


class ImageDraw(Image):
    """
    An instance of the ImageDraw class stores information about an 
    image and allows you to perform drawing operations on it. Most 
    operations depend on stored instance attributes.

    Attributes:
    ----------
    height: int
        The image's height.

    width: int
        The image's width.

    path: str
        The path to the image.

    list_of_coordinates: list
        A list with marked coordinates. The list must contain objects
        of type Coordinate.

    Methods:
    ----------
    draw_coordinates
    draw_rectangles
    """

    coordinate_color = [255, 255, 255]
    rectangle_color = [100, 100, 255]

    def __init__(self, path: str):
        super().__init__(path)

    def draw_coordinates(self) -> np.ndarray:
        """
        Draws coordinates from object's list_of_coordinates on the image.

        Returns
        -------
        img:
            np.ndarray - an image with the coordinates applied.
        """
        img = cv2.imread(self.path)

        for coord in self.list_of_coordinates:
            cv2.circle(
                img=img,
                center=(coord.x, coord.y),
                radius=5,
                color=ImageDraw.coordinate_color,
                thickness=-1
            )
        return img

    def draw_rectangles(self) -> np.ndarray:
        """
        Draws rectangles around selected objects.

        The function takes objects from object's list_of_coordinates and 
        groups them into groups of 2 elements each. These elements are 
        opposite corners of the rectangle (e.g. bottom left corner and 
        top right corner). In case of an odd number of coordinates, the 
        last element of the list is skipped.

        Returns
        -------
        np.ndarray - an image with the rectangles applied.
        """

        img = cv2.imread(self.path)

        def draw(list_of_coords):
            for coord_1, coord_2 in list_of_coords:
                cv2.rectangle(
                    img=img,
                    pt1=(coord_1.x, coord_1.y),
                    pt2=(coord_2.x, coord_2.y),
                    color=ImageDraw.rectangle_color,
                    thickness=5)
            return img

        if len(self.list_of_coordinates) % 2 == 0:
            list_of_coordinates = np.array(
                self.list_of_coordinates).reshape(-1, 2)
            return draw(list_of_coordinates)

        else:
            list_of_coordinates = np.array(
                self.list_of_coordinates[:-1]).reshape(-1, 2)
            return draw(list_of_coordinates)
