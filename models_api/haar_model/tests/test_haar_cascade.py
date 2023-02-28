import unittest

import cv2

from models_api.haar_model.haar_cascade_model import HaarCascade
from images.bounding_box import BoundingBox
from images.coordinate import Coordinate


class TestHaarModel(unittest.TestCase):
    haar_model = HaarCascade("")

    def test_is_in_grayscale(self):
        image = cv2.imread("/home/misiek/Pulpit/python/"
                           "parking_spots/data/file.bmp")

        image = TestHaarModel.haar_model._HaarCascade__convert_to_gray(image)

        image_shape = image.shape

        self.assertEqual(len(image_shape), 2)

    def test_prepare_data(self):
        model_output = [
            (1500, 1000, 200, 200),
            (0, 300, 47, 81)
        ]

        proper_output = [
            BoundingBox([Coordinate(1500, 1000),
                         Coordinate(1500+200, 1000+200)]),
            BoundingBox([Coordinate(0, 300), Coordinate(47, 300+81)])
        ]

        model_output = TestHaarModel.haar_model.\
            _HaarCascade__prepare_data(model_output)

        for my_output, model_result in zip(proper_output, model_output):
            # top left corner x
            self.assertEqual(my_output.top_left_x, model_result.top_left_x)

            # top left corner y
            self.assertEqual(my_output.top_left_y, model_result.top_left_y)

            # width
            self.assertEqual(my_output.bbox_width, model_result.bbox_width)

            # height
            self.assertEqual(my_output.bbox_height, model_result.bbox_height)
