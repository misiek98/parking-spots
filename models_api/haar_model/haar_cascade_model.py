import cv2
import numpy as np

from images.bounding_box import BoundingBox
from images.coordinate import Coordinate


class HaarCascade:
    """
    A simple Haar-Cascade API.

    Attributes:
    ----------
    path_to_model: str
        A path to Haar-Cascade model.

    model: models.common.AutoShape
        A loaded Haar-Cascade model.

    Methods:
    -------
    detect
    """

    def __init__(self, path_to_model: str):
        self.path_to_model = path_to_model

    @property
    def path_to_model(self):
        return self._path_to_model

    @path_to_model.setter
    def path_to_model(self, value):
        if not isinstance(value, str):
            raise TypeError(
                "The path_to_model attribute must be of type string, "
                f"not {type(value).__name__}.")

        self._path_to_model = value

    @property
    def model(self):
        return cv2.CascadeClassifier(self.path_to_model)

    def __convert_to_gray(self, frame):
        """
        Converts a photo to grayscale.
        """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def __prepare_data(self, model_output):
        """
        Changes model output from numpy array to list of bounding boxes.

        Attributes:
        ----------
        model_output: numpy.ndarray
            A model output

        Returns:
        -------
        A list with BoundingBox objects around the each detected object.
        """
        if not isinstance(model_output, list):
            raise TypeError(
                "The model_output parameter must be of type list "
                f"not {type(model_output).__name__}.")

        list_of_bboxes = []

        for x, y, w, h in model_output:
            list_of_bboxes.append(
                BoundingBox([Coordinate(int(x), int(y)),
                            Coordinate(int(x+w), int(y+h))])
            )

        return list_of_bboxes

    def detect(self,
               frame: np.ndarray,
               scale_factor: float,
               min_neighbors: int,
               min_size: tuple,
               max_size: tuple(),
               flags=cv2.CASCADE_SCALE_IMAGE):
        """
        Allows to make detections on the given 'frame' object.

        Attributes:
        ----------
        frame: image
            An image on which you want to make a detection.

        scale_factor: float
            Parameter specifying how much the image size is reduced at
            each image scale.

        min_neighbors: int
            Parameter specifying how many neighbors each candidate
            rectangle should have to retain it.

        min_size: tuple
            Minimum possible object size. Smaller objects are ignored.

        max_size: tuple
            Maximum possible object size.

        flags:
            Other flags. Default: cv2.CASCADE_SCALE_IMAGE

        Returns:
        -------
        A list with BoundingBox objects around the each detected object.
        """

        if not isinstance(scale_factor, float):
            raise TypeError(
                "The scale_factor attribute must be of type float, not "
                f"{type(scale_factor).__name__}.")

        if not isinstance(min_neighbors, int):
            raise TypeError(
                "The min_neighbors attribute must be of type int, not "
                f"{type(min_neighbors).__name__}.")

        # min_size validation
        if not isinstance(min_size, tuple):
            raise TypeError(
                "The min_size attribute must be of type tuple, not "
                f"{type(min_size).__name__}.")

        if not len(min_size) == 2:
            raise ValueError(
                "The min_size tuple must consist of 2 values, not "
                f"{len(min_size)}.")

        for value in min_size:
            if not isinstance(value, int):
                raise TypeError(
                    "The min_size tuple must contain only integers, "
                    f"not {type(value).__name__}.")

        # max_size validation
        if not isinstance(max_size, tuple):
            raise TypeError(
                "The max_size attribute must be of type tuple, not "
                f"{type(max_size).__name__}.")

        if not len(max_size) == 2:
            raise ValueError(
                "The max_size tuple must consist of 2 values, not "
                f"{len(max_size)}.")

        for value in max_size:
            if not isinstance(value, int):
                raise TypeError(
                    "The max_size tuple must contain only integers, "
                    f"not {type(value).__name__}.")

        detections = self.model.detectMultiScale(
            self.__convert_to_gray(frame),
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_size,
            maxSize=max_size,
            flags=flags
        )

        return self.__prepare_data(detections)
