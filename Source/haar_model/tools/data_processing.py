import os

import cv2
import numpy

from .other_functions import load_config

config = load_config(
    r'C:\Users\Misiek\Desktop\Python\MGR\Source\haar_model\haar_config.json')


class Point:
    """ 
    Class Point contains X and Y coordinates.

    x: x coordinate.
    y: y coordinate.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point(
            abs(self.x - other.x),
            abs(self.y - other.y)
        )


class DataProcessingMethods(Point):
    """
    The methods below allow you to prepare data for a Haar-Cascade 
    algorithm. 
    """

    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @staticmethod
    def prepare_vector_data(list_of_points: list) -> None:
        """
        This method prepares data from list_of_points to generate a .vec 
        file that will be used to train a Haar Cascade model.

        list_of_points: list that contains Point objects.

        The list should consists of an even number of points (if not, 
        there is an error). The iteration starts from the second element 
        of the list. To create an area, you need 2 points - an initial 
        point with the smallest x and y coordinates (top left corner) 
        and the width and height of that area. The width and height of 
        the area are calculated and stored in a list at the iterated 
        position. Finally, we go 2 steps further in the loop and repeat 
        the operation.
        """
        for iteration, _ in enumerate(list_of_points):
            if (iteration % 2 == 1):
                width_and_height = (list_of_points[iteration]
                                    - list_of_points[iteration - 1])

                if (list_of_points[iteration - 1].x
                        > list_of_points[iteration].x):
                    list_of_points[iteration
                                   - 1].x = list_of_points[iteration].x
                if (list_of_points[iteration - 1].y
                        > list_of_points[iteration].y):
                    list_of_points[iteration
                                   - 1].y = list_of_points[iteration].y

                list_of_points[iteration] = width_and_height

    @staticmethod
    def save_marked_area(list_of_points: list, img: numpy.ndarray) -> None:
        """
        This method cuts out the marked part(s) of the image and save 
        it to neg folder.

        list_of_points: list that contains Point objects.
        img: copy of the image.
        """
        NEGATIVE_IMAGES_DIR = config['negDir']
        for iteration, _ in enumerate(list_of_points):
            if (iteration % 2 == 1):
                top_left_x = min(list_of_points[iteration - 1].x,
                                 list_of_points[iteration].x)
                top_left_y = min(list_of_points[iteration - 1].y,
                                 list_of_points[iteration].y)
                bottom_right_x = max(list_of_points[iteration - 1].x,
                                     list_of_points[iteration].x)
                bottom_right_y = max(list_of_points[iteration - 1].y,
                                     list_of_points[iteration].y)

                cv2.imwrite(
                    filename=os.path.join(
                        NEGATIVE_IMAGES_DIR,
                        f'file{len(os.listdir(NEGATIVE_IMAGES_DIR))}.jpg'),
                    img=img[top_left_y:bottom_right_y,
                            top_left_x:bottom_right_x]
                )

    @staticmethod
    def draw_rectangles(
            list_of_points: list, img: numpy.ndarray) -> numpy.ndarray:
        """
        This method draws rectangles around marked objects.

        list_of_points: list that contains Point objects.
        img: copy of the image that you want to draw rectangles.
        """
        for iteration, _ in enumerate(list_of_points):
            if (iteration % 2 == 1):
                cv2.putText(
                    img=img,
                    text=str(int((iteration - 1)/2)),
                    org=(
                        list_of_points[iteration - 1].x - 15,
                        list_of_points[iteration - 1].y - 5),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=.5,
                    color=(0, 100, 255),
                    thickness=2
                )

                image = cv2.rectangle(
                    img=img,
                    pt1=(
                        list_of_points[iteration - 1].x,
                        list_of_points[iteration - 1].y),
                    pt2=(
                        list_of_points[iteration].x,
                        list_of_points[iteration].y),
                    color=(0, 50, 255),
                    thickness=1
                )

        return image

    @staticmethod
    def draw_points(img: numpy.ndarray, list_of_points: list) -> numpy.ndarray:
        """
        Function draw_points draws a marked points from list_of_points 
        on the image.

        img: copy of the image.
        list_of_points: list that contains Point objects.
        """
        for point in list_of_points:
            cv2.circle(
                img=img,
                center=(point.x, point.y),
                radius=2,
                color=(255, 255, 255),
                thickness=-1
            )

        return img


def get_position(event, x: int, y: int, flags: list, param: list) -> None:
    """
    Function get_position does a few things. When you double click left  
    mouse button function will  
    draw a small circle at this point and add their coordinates  
    (saved in class Point) to the listOfPoints list.

    event: induced action
    x: x coordinate
    y: y coordinate
    flags and params were required to this function but weren't used.
    """
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(
            img=param[0],
            center=(x, y),
            radius=2,
            color=(255, 255, 255),
            thickness=-1
        )

        param[1].append(Point(x=x, y=y))
