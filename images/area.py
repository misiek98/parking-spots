import numpy as np
import cv2

from images.coordinate import Coordinate
from images.bounding_box import BoundingBox


class ParkingArea:
    """
    Stores informations about a parking area: its endpoints, number of
    occupied parking spots and total number of parking spots. Also
    allows you to draw the area and check if an object is inside the
    area.

    Methods:
    -------
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

    @property
    def __color(self):
        return np.random.randint(0, 255, size=(1, 3)).tolist()[0]

    def __calculate_angles(self):
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
        return np.array([
            [self.top_left_coordinate.x, self.top_left_coordinate.y],
            [self.top_right_coordinate.x, self.top_right_coordinate.y],
            [self.bottom_right_coordinate.x, self.bottom_right_coordinate.y],
            [self.bottom_left_coordinate.x, self.bottom_left_coordinate.y]
        ])

    def is_in_area(self, point: Coordinate):
        """

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

    @occupied_parking_spots.setter
    def occupied_parking_spots(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "The occupied_parking_spots must be of type int, "
                f"not {type(value).__name__}.")

        self._occupied_parking_spots = value

    def forget_detected_cars(self):
        """

        """
        self.occupied_parking_spots = 0

    # def prepare_img(self, img):
    #     img[self.top_left_coordinate.y:self.top_left_coordinate.y - 30,
    #         self.top_left_coordinate.x:self.top_right_coordinate.x
    #         ] = 0
    #     return img

    def draw_area(self, img: np.ndarray):
        """

        """

        return cv2.polylines(
            img=img,
            pts=[self.__numeric_area()],
            isClosed=True,
            color=[255, 100, 100],
            thickness=3)

    def print_information(self, img: np.ndarray):
        """

        """
        return cv2.putText(
            img=img,
            text=(f"{self.occupied_parking_spots} car(s) in "
                  f"{self.number_of_parking_spots} spots."),
            org=(self.top_left_coordinate.x, self.top_left_coordinate.y-10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=[255, 100, 100],
            thickness=2)
