import torch

from images.bounding_box import BoundingBox
from images.coordinate import Coordinate


class YoloModel:
    """

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

    def detect(self, frame):
        """
        Allows to make detections on the given object 'frame'.

        Attributes:
        ----------
        frame: image
            An image on which you want to make a detection.

        Returns:
        -------
        A list with BoundingBox objects around the each detected object.
        """

        list_of_bboxes = []
        detection = self.model(frame).xyxy[0].numpy()

        for x_min, y_min, x_max, y_max, _, _ in detection:
            x_min = int(x_min)
            y_min = int(y_min)
            x_max = int(x_max)
            y_max = int(y_max)

            list_of_bboxes.append(
                BoundingBox([Coordinate(x_min, y_min),
                            Coordinate(x_max, y_max)])
            )

        return list_of_bboxes
