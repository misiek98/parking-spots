import unittest

from tools.coordinate import Coordinate


class TestCoordinates(unittest.TestCase):
    def setUp(self):
        self.coord = Coordinate(x=3, y=5)

    def test_x_setter_bool(self):
        with self.assertRaises(
                TypeError,
                msg="To pass the test you must set the x attribute as "
                "boolean."):
            self.coord.x = True

    def test_y_setter_bool(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="To pass the test you must set the y attribute as "
                "boolean"):
            self.coord.y = True

    def test_x_setter_str(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the x attribute as "
                "string."):
            self.coord.x = "some string"

    def test_y_setter_str(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the y attribute as "
                "string."):
            self.coord.y = "some string"

    def test_x_setter_float(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the x attribute as float."):
            self.coord.x = 0.1

    def test_y_setter_float(self):
        with self.assertRaises(
                expected_exception=TypeError,
                msg="to pass the test you must set the y attribute as float."):
            self.coord.y = 0.1

    def test_x_setter_negative_value(self):
        with self.assertRaises(
                expected_exception=ValueError,
                msg="to pass the test x must be negative."):
            self.coord.x = -1

    def test_y_setter_negative_value(self):
        with self.assertRaises(
                expected_exception=ValueError,
                msg="to pass the test y must be negative."):
            self.coord.y = -1
