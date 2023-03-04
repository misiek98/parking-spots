import unittest
from collections import namedtuple

from parameterized import parameterized

from models_api.linear_clusterization.linear_function import LinearFunction
from images.coordinate import Coordinate
from images.bounding_box import BoundingBox


class TestLinearFunction(unittest.TestCase):
    distance = namedtuple("distance",
                          "point_index point_to_line_distance")

    @parameterized.expand(
        [
            (
                "angle_10_bbox_center_5_5",
                10,
                [BoundingBox([Coordinate(0, 0), Coordinate(10, 10)])],
                42,
                4.11836
            ),
            (
                "angle_30_bbox_center_158_415",
                30,
                [BoundingBox([Coordinate(0, 0), Coordinate(316, 830)])],
                42,
                323.77866
            ),
            (
                "angle_110_bbox_center_357_174",
                110,
                [BoundingBox([Coordinate(0, 0), Coordinate(714, 348)])],
                42,
                1154.84944
            ),
        ]
    )
    def test_b(self, name, angle, list_of_bounding_boxes, seed, value):
        line = LinearFunction(angle=angle,
                              list_of_bounding_boxes=list_of_bounding_boxes,
                              seed=seed)
        self.assertAlmostEqual(line.b, value, 2)

    @parameterized.expand(
        [
            (
                "angle_10",
                10,
                [BoundingBox([Coordinate(0, 0), Coordinate(10, 10)]),
                 BoundingBox([Coordinate(0, 0), Coordinate(316, 830)]),
                 BoundingBox([Coordinate(0, 0), Coordinate(714, 348)])],
                42,
                [distance(0, 105), distance(1, 271), distance(2, 0)]
            ),
            (
                "angle_38",
                38,
                [BoundingBox([Coordinate(0, 0), Coordinate(10, 10)]),
                 BoundingBox([Coordinate(0, 0), Coordinate(316, 830)]),
                 BoundingBox([Coordinate(0, 0), Coordinate(714, 348)])],
                42,
                [distance(0, 83), distance(1, 312), distance(2, 0)]
            ),
            (
                "angle_75",
                75,
                [BoundingBox([Coordinate(0, 0), Coordinate(10, 10)]),
                 BoundingBox([Coordinate(0, 0), Coordinate(316, 830)]),
                 BoundingBox([Coordinate(0, 0), Coordinate(714, 348)])],
                42,
                [distance(0, 296), distance(1, 254), distance(2, 0)]
            ),
        ]
    )
    def test_private__calculate_distance(
            self, name, angle, list_of_bounding_boxes, seed, result):
        line = LinearFunction(angle=angle,
                              list_of_bounding_boxes=list_of_bounding_boxes,
                              seed=seed)

        self.assertEqual(line.list_of_distances, result)
