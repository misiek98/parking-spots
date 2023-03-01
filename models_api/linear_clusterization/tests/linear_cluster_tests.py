import unittest
from unittest.mock import patch

from parameterized import parameterized
import numpy as np

from models_api.linear_clusterization.linear_clusterization import\
    LinearClusterization
from images.coordinate import Coordinate
from images.bounding_box import BoundingBox


class TestLinearFunction(unittest.TestCase):
    with open("/home/misiek/Pulpit/python/parking_spots/models_api/"
              "linear_clusterization/tests/bboxes.txt", "r") as file:
        line = file.readline()

    bboxes = [int(coord) for coord in line.split(" ")]
    bboxes = np.array(bboxes).reshape(-1, 4)

    list_of_bounding_boxes = [
        BoundingBox(group_of_coords=[Coordinate(int(x), int(y)),
                                     Coordinate(int(x+w), int(y+h))])
        for x, y, w, h in bboxes
    ]

    @parameterized.expand(
        [
            (
                "angle_15",
                list_of_bounding_boxes,
                15,
                42,
                [[3], [3], [3], [3], [3, 2, 4, 1], [
                    3], [3], [3], [3], [3], [3], [3]]
            ),
            (
                "angle_45",
                list_of_bounding_boxes,
                45,
                42,
                [[3], [3], [3], [3]]
            )
        ]
    )
    def test_linear_clusterization_determine_areas(
            self, name, list_of_bounding_boxes, angle_step,
            seed, expected_result):

        linear_clusterization = LinearClusterization(
            list_of_bounding_boxes=list_of_bounding_boxes,
            angle_step=angle_step,
            seed=seed
        )

        self.assertEqual(
            first=linear_clusterization._LinearClusterization__determine_areas(
                "max_mean"),
            second=expected_result
        )
