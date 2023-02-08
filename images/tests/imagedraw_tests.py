import unittest

import cv2
import numpy as np

from images.image import ImageDraw
from images.coordinate import Coordinate


class TestImageDraw(unittest.TestCase):
    ImageDraw_instance = ImageDraw(path="/home/misiek/Pulpit/python/"
                                   "parking_spots/data/file.bmp")
    image = cv2.imread(ImageDraw_instance.path)

    coords = []
    for random_value in range(5):
        width = np.random.randint(0, ImageDraw_instance.width+1)
        height = np.random.randint(0, ImageDraw_instance.height+1)
        coords.append(Coordinate(x=width, y=height))

    for coord in coords:
        ImageDraw_instance.append_coordinate(coord=coord)

    try:
        list_of_opposite_corners = np.array(coords).reshape(-1, 2)
    except ValueError:
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
             "bottom_right_corner": bottom_right_corner}
        )

    def test_draw_coordinates_check_pixel_color(self):
        img = TestImageDraw.ImageDraw_instance.draw_coordinates(
            image=TestImageDraw.image)

        for pixel in TestImageDraw.ImageDraw_instance.list_of_coordinates:
            comparison = np.all(
                [img[pixel.y, pixel.x],
                 np.array(TestImageDraw.ImageDraw_instance._ImageDraw__coordinate_color)]
            )
            if not comparison:
                raise ValueError(
                    "The pixel values are not the same.")

    def test_draw_bounding_boxes_check_corners_color(self):
        img = TestImageDraw.ImageDraw_instance.draw_bounding_boxes(
            image=TestImageDraw.image)

        for corner in TestImageDraw.list_of_corners:
            for _, value in corner.items():
                comparison = np.all(
                    [img[value.y, value.x],
                     np.array(TestImageDraw.ImageDraw_instance._ImageDraw__rectangle_color)]
                )
                if not comparison:
                    raise ValueError(
                        "The pixel values are not the same.")
