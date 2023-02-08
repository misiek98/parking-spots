import unittest

from images.coordinate import Coordinate
from images.image import Image


class TestImage(unittest.TestCase):
    def setUp(self):
        self.image = Image(path="data/file.bmp")

    def test_path_setter_bool(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the width attribute "
                "as bool."):
            self.image.path = True

    def test_path_setter_float(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the path attribute "
                "as float."):
            self.image.path = 0.1

    def test_path_setter_int(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the path attribute "
                "as int."):
            self.image.path = 5

    def test_list_of_coordinates_setter_bool(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the list_of_coordinates "
                "attribute as boolean."):
            self.image.list_of_coordinates = True

    def test_list_of_coordinates_setter_str(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the list_of_coordinates "
                "attribute as string."):
            self.image.list_of_coordinates = "some string"

    def test_list_of_coordinates_setter_float(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the list_of_coordinates "
                "attribute as float."):
            self.image.list_of_coordinates = 0.1

    def test_list_of_coordinates_setter_set(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the list_of_coordinates "
                "attribute as set."):
            self.image.list_of_coordinates = ()

    def test_list_of_coordinates_setter_dict(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the list_of_coordinates "
                "attribute as dictionary."):
            self.image.list_of_coordinates = {}

    def test_append_coordinate_greater_x(self):
        with self.assertRaises(
                expected_exception=ValueError,
                msg="to pass the test the coord.x attribute must be greater "
                "than image.width."):
            coord = Coordinate(x=2000, y=50)
            self.image.append_coordinate(coord=coord)

    def test_append_coordinate_greater_y(self):
        with self.assertRaises(
                expected_exception=ValueError,
                msg="to pass the test the coord.y attribute must be greater "
                "than image.height."):
            coord = Coordinate(x=100, y=1200)
            self.image.append_coordinate(coord=coord)

    def test_append_coordinate_coord_set(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you have to pass the object of "
                "type set."):
            self.image.append_coordinate(coord=(70, 20))

    def test_append_coordinate_coord_list(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you have to pass the object of "
                "type list."):
            self.image.append_coordinate(coord=[70, 20])
