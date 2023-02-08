import unittest

from parameterized import parameterized

from images.bounding_box import BoundingBox
from images.coordinate import Coordinate


class TestBoundingBox(unittest.TestCase):
    @parameterized.expand(
        [
            ("single coordinate", [Coordinate(x=5, y=10)]
             ),
            ("three coordinates", [Coordinate(x=10, y=13),
                                   Coordinate(x=5, y=1),
                                   Coordinate(x=7, y=13)]
             ),
            ("five coordinates", [Coordinate(x=10, y=13),
                                  Coordinate(x=5, y=1),
                                  Coordinate(x=7, y=13),
                                  Coordinate(x=11, y=15),
                                  Coordinate(x=27, y=54)]
             )
        ]
    )
    def test_incorrect_number_of_coordinates(self, name, group):
        with self.assertRaises(ValueError):
            BoundingBox(group_of_coords=group)

    @parameterized.expand(
        [
            ("x 10", Coordinate(x=10, y=5), Coordinate(x=15, y=4), 10),
            ("x 15", Coordinate(x=25, y=5), Coordinate(x=15, y=4), 15),
            ("x 38", Coordinate(x=147, y=5), Coordinate(x=38, y=4), 38),
        ]
    )
    def test_determining_top_left_x(self, name, coord_1, coord_2, left_corner_x):
        self.assertEqual(BoundingBox(
            [coord_1, coord_2]).top_left_x, left_corner_x)

    @parameterized.expand(
        [
            ("y 327", Coordinate(x=10, y=341), Coordinate(x=15, y=327), 327),
            ("y 270", Coordinate(x=25, y=283), Coordinate(x=15, y=270), 270),
            ("y 4", Coordinate(x=147, y=15), Coordinate(x=38, y=4), 4),
        ]
    )
    def test_determining_ttop_left_y(self, name, coord_1, coord_2, left_corner_y):
        self.assertEqual(BoundingBox(
            [coord_1, coord_2]).top_left_y, left_corner_y)

    @parameterized.expand(
        [
            ("width 5", Coordinate(x=10, y=341), Coordinate(x=15, y=327), 5),
            ("width 270", Coordinate(x=25, y=283), Coordinate(x=15, y=270), 10),
            ("width 4", Coordinate(x=147, y=15), Coordinate(x=38, y=4), 109),
        ]
    )
    def test_calculate_width(self, name, coord_1, coord_2, width):
        self.assertEqual(BoundingBox(
            [coord_1, coord_2]).bbox_width, width)

    @parameterized.expand(
        [
            ("height 5", Coordinate(x=10, y=341), Coordinate(x=15, y=327), 14),
            ("height 270", Coordinate(x=25, y=283),
             Coordinate(x=15, y=270), 13),
            ("height 4", Coordinate(x=147, y=15), Coordinate(x=38, y=4), 11),
        ]
    )
    def test_calculate_height(self, name, coord_1, coord_2, height):
        self.assertEqual(BoundingBox(
            [coord_1, coord_2]).bbox_height, height)

    @parameterized.expand(
        [
            ("x_center_400", Coordinate(100, 100), Coordinate(700, 600), 400),
            ("x_center_450", Coordinate(0, 0), Coordinate(900, 400), 450),
            ("x_center_171", Coordinate(342, 218), Coordinate(0, 0), 171)
        ]
    )
    def test_calculate_x_center(self, name, coord_1, coord_2, x_center):
        self.assertEqual(BoundingBox(
            [coord_1, coord_2]).x_center, x_center)

    @parameterized.expand(
        [
            ("y_center_350", Coordinate(100, 100), Coordinate(700, 600), 350),
            ("y_center_200", Coordinate(0, 0), Coordinate(900, 400), 200),
            ("y_center_109", Coordinate(342, 218), Coordinate(0, 0), 109)
        ]
    )
    def test_calculate_y_center(self, name, coord_1, coord_2, y_center):
        self.assertEqual(BoundingBox(
            [coord_1, coord_2]).y_center, y_center)
