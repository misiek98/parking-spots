import os

import cv2
import numpy as np

from images.coordinate import Coordinate
from images.bounding_box import BoundingBox


class Image:
    """
    An instance of an Image class stores information about an image.

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

    list_of_bounding_boxes: list
        A list with image bounding boxes. The list must contain 
        objects of type BoundingBox.

    Methods:
    ----------
    append_coordinate
    remove_last_coordinate
    """

    def __init__(self, path: str):
        self.path = path
        self.list_of_coordinates = []
        self.list_of_bounding_boxes = []

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
            if len(value) == 0:
                self._list_of_coordinates = value
            else:
                for coord in value:
                    if not isinstance(coord, Coordinate):
                        raise TypeError(
                            "The coord parameter must be of type Coordinate, "
                            f"not {type(coord).__name__}.")

                self._list_of_coordinates = value

        else:
            raise TypeError(
                "The list_of_coordinates parameter must be of type list, "
                f"not {type(value).__name__}.")

    @property
    def list_of_bounding_boxes(self):
        self._list_of_bounding_boxes.clear()

        try:
            list_of_bboxes = np.array(
                self.list_of_coordinates).reshape(-1, 2)
            self._list_of_bounding_boxes = [
                BoundingBox(group)
                for group in list_of_bboxes
            ]

            return self._list_of_bounding_boxes

        except ValueError:
            print("Odd number of coordinates, last coordinate "
                  "has been skipped.")
            list_of_bboxes = np.array(
                self.list_of_coordinates[:-1]).reshape(-1, 2)
            self._list_of_bounding_boxes = [
                BoundingBox(group)
                for group in list_of_bboxes
            ]

            return self._list_of_bounding_boxes

    @list_of_bounding_boxes.setter
    def list_of_bounding_boxes(self, value):
        if not isinstance(value, (list, np.ndarray)):
            raise TypeError(
                "The list_of_bounding_boxes must be of type list or "
                f"np.ndarray, not {type(value).__name__}")

        self._list_of_bounding_boxes = value

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

    def remove_last_coordinate(self):
        """
        Removes last coordinate from the list_of_coordiantes.
        """
        self.list_of_coordinates.pop()


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
    clean_image
    draw_coordinates
    draw_bounding_boxes
    """

    __coordinate_color = [255, 255, 255]
    __rectangle_color = [155, 100, 255]

    def __init__(self, path: str):
        super().__init__(path)

    def clean_image(self) -> np.ndarray:
        """
        Loads and returns an image without bboxes or coordinates.
        """
        return cv2.imread(self.path)

    def draw_coordinates(self, image: np.ndarray) -> np.ndarray:
        """
        Draws coordinates from object's list_of_coordinates on the image.

        Parameters:
        ----------
        image: np.ndarray
            Loaded image on which you want to draw coordinates.

        Returns
        -------
        image:
            np.ndarray - an image with the coordinates applied.
        """

        if not isinstance(image, np.ndarray):
            raise TypeError(
                "The image parameter must be of type np.ndarray, not "
                f"{type(image).__name__}. Load the image using cv2.imread.")

        for coord in self.list_of_coordinates:
            cv2.circle(
                img=image,
                center=(coord.x, coord.y),
                radius=5,
                color=ImageDraw.__coordinate_color,
                thickness=-1
            )
        return image

    def __draw_rectangles(self, img: np.ndarray) -> np.ndarray:
        for bbox in self.list_of_bounding_boxes:
            cv2.rectangle(
                img=img,
                pt1=(bbox.top_left_x, bbox.top_left_y),
                pt2=(bbox.top_left_x + bbox.bbox_width,
                     bbox.top_left_y + bbox.bbox_height),
                color=ImageDraw.__rectangle_color,
                thickness=5)
        return img

    def draw_bounding_boxes(self, image: np.ndarray) -> np.ndarray:
        """
        Draws rectangles around selected objects.

        The function takes objects from object's list_of_coordinates and 
        groups them into groups of 2 elements each. These elements are 
        opposite corners of the rectangle (e.g. bottom left corner and 
        top right corner). In case of an odd number of coordinates, the 
        last element of the list is skipped.

        Parameters:
        ----------
        image: np.ndarray
            Loaded image on which you want to draw bounding_boxes.

        Returns
        -------
        np.ndarray - an image with the rectangles applied.
        """
        if not isinstance(image, np.ndarray):
            raise TypeError(
                "The image parameter must be of type np.ndarray, not "
                f"{type(image).__name__}. Load the image using cv2.imread.")

        return self.__draw_rectangles(img=image)
