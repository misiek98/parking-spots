import numpy as np
import cv2

from images.coordinate import Coordinate
from images.bounding_box import BoundingBox


class ParkingArea:
    """
    Stores an information about the parking area: its endpoints, total
    and occupied parking spots. Also allows you to draw the area and
    check if an object is inside the area.

    Methods:
    -------
    occupy_parking_spot
    is_in_area
    draw_area
    forget_detected_cars
    """

    __color = [255, 255, 0]

    def __init__(self, area: list, img_width: int, img_height: int):
        self.area = area
        self.img_width = img_width
        self.img_height = img_height
        self.occupied_parking_spots = 0

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, value):
        if not isinstance(value, list):
            raise TypeError(
                "The area attribute must be of type list, not "
                f"{type(value).__name__}.")

        for bbox in value:
            if not isinstance(bbox, BoundingBox):
                raise TypeError(
                    "Elements inside the area list must be of type "
                    f"BoundingBox, not {type(bbox).__name__}.")

        self._area = value

    @property
    def number_of_parking_spots(self):
        return len(self.area) - 1

    @property
    def img_width(self):
        return self._img_width

    @img_width.setter
    def img_width(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "The img_width attribute must be of type int, not "
                f"{type(value).__name__}.")

        self._img_width = value

    @property
    def img_height(self):
        return self._img_height

    @img_height.setter
    def img_height(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "The img_height attribute must be of type int, not "
                f"{type(value).__name__}.")

        self._img_height = value

    def __calculate_angles(self):
        """
        Calculates the line slope between bottom right corner of the
        frame and the object's BoundingBox center.
        """

        return [
            int(
                np.degrees(
                    np.arctan(
                        (self.img_height-bbox.top_left_y)
                        / bbox.top_left_x
                    )
                )
            )
            for bbox in self.area
        ]

    def __sort_bboxes_by_angle(self):
        """
        Sorts the list of BoundingBoxes by angle.
        """

        return [
            bbox
            for angle, bbox in sorted(
                zip(self.__calculate_angles(), self.area),
                key=lambda pair: pair[0])
        ]

    @property
    def top_left_coordinate(self):
        return Coordinate(x=self.__sort_bboxes_by_angle()[-1].top_left_x,
                          y=(self.__sort_bboxes_by_angle()[-1].top_left_y))

    @property
    def top_right_coordinate(self):
        return Coordinate(x=(self.__sort_bboxes_by_angle()[-1].top_left_x
                             + self.__sort_bboxes_by_angle()[-1].bbox_width),
                          y=self.__sort_bboxes_by_angle()[-1].top_left_y)

    @property
    def bottom_left_coordinate(self):
        return Coordinate(x=self.__sort_bboxes_by_angle()[0].top_left_x,
                          y=(self.__sort_bboxes_by_angle()[0].top_left_y
                             + self.__sort_bboxes_by_angle()[0].bbox_height))

    @property
    def bottom_right_coordinate(self):
        return Coordinate(x=(self.__sort_bboxes_by_angle()[0].top_left_x
                             + self.__sort_bboxes_by_angle()[0].bbox_width),
                          y=(self.__sort_bboxes_by_angle()[0].top_left_y
                             + self.__sort_bboxes_by_angle()[0].bbox_height))

    def __numeric_area(self):
        """
        Returns the coordinates of the area in numerical form.
        """

        return np.array([
            [self.top_left_coordinate.x, self.top_left_coordinate.y],
            [self.top_right_coordinate.x, self.top_right_coordinate.y],
            [self.bottom_right_coordinate.x, self.bottom_right_coordinate.y],
            [self.bottom_left_coordinate.x, self.bottom_left_coordinate.y]
        ])

    def is_in_area(self, point: Coordinate):
        """
        Checks if the point is inside the area.

        Parameters:
        ----------
        point: Coordinate
            The point you want to check if is inside the area.
        """

        if not isinstance(point, Coordinate):
            raise TypeError(
                "The point parameter must be of type Coordinate, "
                f"not {type(point).__name__}.")

        return cv2.pointPolygonTest(
            contour=self.__numeric_area(),
            pt=(point.x, point.y),
            measureDist=False
        )

    @property
    def occupied_parking_spots(self):
        return self._occupied_parking_spots

    def occupy_parking_spot(self):
        """
        Determines one parking spot as occupied.
        """

        self.occupied_parking_spots += 1

    @occupied_parking_spots.setter
    def occupied_parking_spots(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "The occupied_parking_spots must be of type int, "
                f"not {type(value).__name__}.")

        self._occupied_parking_spots = value

    def forget_detected_cars(self):
        """
        Sets the area's occupied_parking_spots attribute to 0.
        """

        self.occupied_parking_spots = 0

    def draw_area(self, img: np.ndarray):
        """
        Draws the area on the provided image.

        Parameters:
        ----------
        img: np.ndarray
            The image.
        """

        return cv2.polylines(
            img=img,
            pts=[self.__numeric_area()],
            isClosed=True,
            color=[255, 100, 100],
            thickness=3)
