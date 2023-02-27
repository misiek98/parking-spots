import torch
import numpy

from images.bounding_box import BoundingBox
from images.coordinate import Coordinate


class YoloModel:
    """
    A simple YOLOv5 API.

    Attributes:
    ----------
    path_to_model: str
        A path to YOLOv5 model.

    model: models.common.AutoShape
        A loaded YOLOv5 model.

    Methods:
    -------
    detect(frame):
        Allows to make detections on the given object 'frame'.
    """

    def __init__(self, path_to_model: str):
        self.path_to_model = path_to_model
        self.model = None

    @property
    def path_to_model(self):
        return self._path_to_model

    @path_to_model.setter
    def path_to_model(self, value):
        if not isinstance(value, str):
            raise TypeError(
                "The path_to_model parameter must be of type string, not "
                f"{type(value).__name__}.")
        self._path_to_model = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if not value:
            self._model = torch.hub.load(
                repo_or_dir='ultralytics/yolov5',
                model='custom',
                path=self.path_to_model,
                force_reload=True)

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
        if not isinstance(model_output, numpy.ndarray):
            raise TypeError(
                "The model_output parameter must be of type numpy array, "
                f"not {type(model_output).__name__}.")

        list_of_bboxes = []

        for x_min, y_min, x_max, y_max, _, _ in model_output:
            x_min = int(x_min)
            y_min = int(y_min)
            x_max = int(x_max)
            y_max = int(y_max)

            list_of_bboxes.append(
                BoundingBox([Coordinate(x_min, y_min),
                            Coordinate(x_max, y_max)])
            )

        return list_of_bboxes

    def detect(self, frame):
        """
        Allows to make detections on the given 'frame' object.

        Attributes:
        ----------
        frame: image
            An image on which you want to make a detection.

        Returns:
        -------
        A list with BoundingBox objects around the each detected object.
        """

        detection = self.model(frame).xyxy[0].numpy()
        return self.__prepare_data(detection)
