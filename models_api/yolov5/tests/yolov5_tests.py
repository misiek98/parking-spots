import unittest

from models_api.yolov5.yolo_model import YoloModel
from images.bounding_box import BoundingBox


class TestYoloModel(unittest.TestCase):
    model = YoloModel("/home/misiek/Pulpit/python/parking_spots/yolov5s.pt")

    def test_detect_output(self):
        output = TestYoloModel.model.detect(
            "https://www.uwe.ac.uk/-/media/uwe/images/life/parking-for-staff-"
            "410x230.jpg?mh=231&la=en&h=230&w=410&mw=413&hash="
            "2FB3A53992E539089CB78C09C6704F1F")

        if not isinstance(output, list):
            raise TypeError(
                "The model outut should be of type list, not "
                f"{type(output).__name__}.")

        for obj in output:
            if not isinstance(obj, BoundingBox):
                raise TypeError(
                    "Output list should contain objects of type BoundingBox, "
                    f"not {type(obj).__name__}.")
