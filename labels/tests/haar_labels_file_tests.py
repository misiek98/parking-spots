import os
import unittest

from images.coordinate import Coordinate
from labels.haar_labels import HaarLabel


class TestHaarLabel(unittest.TestCase):
    def setUp(self):
        haar_labels = HaarLabel("./data/file.bmp")
        haar_labels.list_of_coordinates = [
            Coordinate(10, 5), Coordinate(5, 25),
            Coordinate(12, 6), Coordinate(6, 13)
        ]

        print("Creating file with haar labels...")
        with open(file="./training/labels/haar_labels.txt", mode="a") as file:
            for bbox in haar_labels.list_of_bounding_boxes:
                path = haar_labels.path
                x = bbox.top_left_x
                y = bbox.top_left_y
                width = bbox.bbox_width
                height = bbox.bbox_height

                file.write(
                    f"{path} {len(haar_labels.list_of_bounding_boxes)} {x}"
                    f" {y} {width} {height}\n")

    def tearDown(self):
        os.remove("./training/labels/haar_labels.txt")
        print("File has been removed.")

    def test_save_data_to_file(self, path="./training/labels/haar_labels.txt"):
        elements = []
        with open(path, "r") as file:
            for line in file:
                elements.append(line.strip())

        self.assertEqual(
            first=elements,
            second=["./data/file.bmp 5 5 5 20", "./data/file.bmp 6 6 6 7"])
