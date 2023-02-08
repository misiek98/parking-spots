import unittest

from parameterized import parameterized

from labels.YOLOv5_labels import YOLOv5Label
from images.coordinate import Coordinate


class TestYOLOv5(unittest.TestCase):
    yolo_labels = YOLOv5Label("./data/file.bmp")

    @parameterized.expand(
        [
            ("x_center_400", [Coordinate(100, 100),
             Coordinate(700, 800)], 400 / yolo_labels.width),
            ("x_center_500", [Coordinate(400, 300),
             Coordinate(600, 700)], 500 / yolo_labels.width)
        ]
    )
    def test_calculate_x_center(self, name, list_of_coordinates, result):
        label = TestYOLOv5.yolo_labels
        label.list_of_coordinates = list_of_coordinates

        self.assertAlmostEqual(
            label.list_of_bounding_boxes[0].x_center / label.width,
            result)

    @parameterized.expand(
        [
            ("y_center_450", [Coordinate(100, 100),
             Coordinate(700, 800)], 450 / yolo_labels.height),
            ("y_center_500", [Coordinate(400, 300),
             Coordinate(600, 700)], 500 / yolo_labels.height)
        ]
    )
    def test_calculate_y_center(self, name, list_of_coordinates, result):
        label = TestYOLOv5.yolo_labels
        label.list_of_coordinates = list_of_coordinates

        self.assertAlmostEqual(
            label.list_of_bounding_boxes[0].y_center / label.height,
            result)
