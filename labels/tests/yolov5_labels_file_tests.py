import os
import unittest

from labels.YOLOv5_labels import YOLOv5Label
from images.coordinate import Coordinate


class TestYOLOv5LabelsFile(unittest.TestCase):
    yolo_labels = YOLOv5Label("./data/file.bmp")
    yolo_labels.list_of_coordinates = [
        Coordinate(679, 762), Coordinate(931, 864)
    ]

    print("Creating file with yolo labels...")
    with open(file="./training/labels/yolov5_labels/file_test.txt",
              mode="a", encoding="utf8") as file:
        for bbox in yolo_labels.list_of_bounding_boxes:
            x_center = ((bbox.top_left_x + bbox.bbox_width/2) /
                        yolo_labels.width)
            y_center = ((bbox.top_left_y + bbox.bbox_height/2) /
                        yolo_labels.height)
            width = bbox.bbox_width / yolo_labels.width
            height = bbox.bbox_height / yolo_labels.height

            file.write(
                "0 "
                f"{x_center} "
                f"{y_center} "
                f"{width} "
                f"{height}\n"
            )

    def tearDown(self):
        os.remove("./training/labels/yolov5_labels/file_test.txt")
        print("File has been removed.")

    def test_prepare_data(self):
        with open(file="./training/labels/yolov5_labels/file_test.txt",
                  mode="r", encoding="utf8") as file:
            labels_from_file = []
            for line in file:
                labels_from_file.append(line.strip())

        self.assertEqual(
            first=labels_from_file,
            second=[
                TestYOLOv5LabelsFile.yolo_labels._YOLOv5Label__prepare_data().
                strip()])
