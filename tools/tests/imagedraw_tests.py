import unittest

import numpy as np

from tools.image import ImageDraw
from tools.coordinate import Coordinate


class TestImageDraw(unittest.TestCase):
    img = ImageDraw(path="/home/misiek/Pulpit/python/"
                    "parking_spots/data/file.bmp")

    coords = []
    for random_value in range(5):
        width = np.random.randint(0, img.width+1)
        height = np.random.randint(0, img.height+1)
        coords.append(Coordinate(x=width, y=height))

    for coord in coords:
        img.append_coordinate(coord=coord)

    if len(coords) % 2 == 0:
        list_of_opposite_corners = np.array(coords).reshape(-1, 2)
    else:
        list_of_opposite_corners = np.array(coords[:-1]).reshape(-1, 2)

    list_of_corners = []
    for corners in list_of_opposite_corners:
        rectangle_corners = {}
        top_left_corner = Coordinate(
            x=min(corners[0].x, corners[1].x),
            y=min(corners[0].y, corners[1].y)
        )

        top_right_corner = Coordinate(
            x=max(corners[0].x, corners[1].x),
            y=min(corners[0].y, corners[1].y)
        )
        bottom_left_corner = Coordinate(
            x=min(corners[0].x, corners[1].x),
            y=max(corners[0].y, corners[1].y)
        )
        bottom_right_corner = Coordinate(
            x=max(corners[0].x, corners[1].x),
            y=max(corners[0].y, corners[1].y)
        )
        list_of_corners.append(
            {"top_left_corner": top_left_corner,
             "top_right_corner": top_right_corner,
             "bottom_left_corner": bottom_left_corner,
             "bottom_right_corner": bottom_right_corner
             }
        )

    def test_draw_coordinates_check_image_color(self):
        image = TestImageDraw.img.draw_coordinates()
        for pixel in TestImageDraw.img.list_of_coordinates:
            comparison = np.all(
                [image[pixel.y, pixel.x],
                 np.array(TestImageDraw.img.coordinate_color)]
            )
            if not comparison:
                raise ValueError(
                    "The colors are not the same.")

    def test_draw_rectangles_check_corners_color(self):
        image = TestImageDraw.img.draw_rectangles()

        for corner in TestImageDraw.list_of_corners:
            for _, value in corner.items():
                comparison = np.all(
                    [image[value.y, value.x],
                     np.array(TestImageDraw.img.rectangle_color)]
                )
                if not comparison:
                    raise ValueError(
                        "The colors are not the same.")
