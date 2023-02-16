import numpy as np

from images.bounding_box import BoundingBox
from images.coordinate import Coordinate
from models.linear_clusterization.linear_function import LinearFunction


class LinearClusterization:
    """
    ABCDEF

    Attributes:
    ----------
    list_of_bounding_boxes: list
        abcdef

    angle_step: int
        sdasdasd

    seed: int
        dasdasdasd

    areas: list
        dasdasdasd

    Methods:
    -------
    fit()
      dasdasdas
    """

    def __init__(self, list_of_bounding_boxes: list, angle_step: int,
                 seed=42, areas=[]):
        self.list_of_bounding_boxes = list_of_bounding_boxes
        self.angle_step = angle_step
        self.seed = seed
        self.areas = areas

    @property
    def list_of_bounding_boxes(self):
        return self._list_of_bounding_boxes

    @list_of_bounding_boxes.setter
    def list_of_bounding_boxes(self, value):
        if not isinstance(value, list):
            raise TypeError(
                "The list_of_bounding_boxes parameter must be of type list, "
                f"not {type(value).__name__}.")

        for bbox in value:
            if not isinstance(bbox, BoundingBox):
                raise TypeError(
                    "Elements in the list_of_bounding_boxes must be of type "
                    f"BoundingBox, not {type(bbox).__name__}.")

        self._list_of_bounding_boxes = value

    @property
    def angle_step(self):
        return self._angle_step

    @angle_step.setter
    def angle_step(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "The angle_step parameter must be of type int, not "
                f"{type(value).__name__}.")

        if not 180 >= value > 0:
            raise ValueError(
                "The angle_step parameter must be greater than 0 but less than"
                " or equal 180.")

        self._angle_step = value

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "The seed parameter must be of type int, not "
                f"{type(value).__name__}.")

        self._seed = value

    @property
    def areas(self):
        return self._areas

    @areas.setter
    def areas(self, value):
        if not isinstance(value, list):
            raise TypeError(
                "The areas attribute must be of type list, not "
                f"{type(value).__name__}.")
        self._areas = value

    @property
    def __list_of_lines_different_angles(self):
        """
        dasdasdasd
        """
        angles = [angle
                  for angle in range(0, 181, self.angle_step)
                  if angle != 90]

        return [
            LinearFunction(angle=angle,
                           list_of_bounding_boxes=self.list_of_bounding_boxes,
                           seed=self.seed)
            for angle in angles]

    def __sort_distances(self, line):
        """
        dsadasdasdasdasd
        """

        return sorted(line.list_of_distances,
                      key=lambda x: x.point_to_line_distance)

    def __only_distances(self, line):
        """
        dsadasdasdasdasd
        """

        return [distance.point_to_line_distance
                for distance in line]

    def __determine_areas(self):
        """
        dsadasdasdasdasd
        """

        areas = []

        for index, point_to_line_distances in enumerate(
                self. __list_of_lines_different_angles):
            sorted_list_of_distances = self.__sort_distances(
                point_to_line_distances)
            only_distances = self.__only_distances(sorted_list_of_distances)
            fac = np.max(only_distances) / np.mean(only_distances)

            area = []

            for index, point_to_line_distances in enumerate(
                    sorted_list_of_distances):
                if (sorted_list_of_distances[index].
                        point_to_line_distance == 0):
                    area.append(sorted_list_of_distances[index].point_index)

                else:
                    if (sorted_list_of_distances[index-1].
                        point_to_line_distance == 0
                        and sorted_list_of_distances[index].
                            point_to_line_distance <= 2):
                        area.append(
                            sorted_list_of_distances[index].point_index)

                    else:
                        if (sorted_list_of_distances[index].
                            point_to_line_distance
                                <= sorted_list_of_distances[index-1].
                                point_to_line_distance * fac):
                            area.append(
                                sorted_list_of_distances[index].point_index)

                        else:
                            break

            areas.append(area)

        return areas

    def __areas_length(self, areas):
        """
        dsadasdasdasdasd
        """

        return [
            len(area)
            for area in areas]

    def __max_area_length(self, areas_length):
        """
        dsadasdasdasdasd
        """

        return max(areas_length)

    def __get_areas_max_length_index(self, areas_length, max_area_length):
        """
        dsadasdasdasdasd
        """

        return np.where(
            np.array(areas_length) == max_area_length)[0]

    def __find_minimum_distances(self, areas_index_max_length, det_areas):
        """
        dsadasdasdasdasd
        """

        distances = []

        for index in areas_index_max_length:
            line = self.__list_of_lines_different_angles[index]
            abc = det_areas
            distance = sum([
                point.point_to_line_distance
                for point in line.list_of_distances
                if point.point_index in abc[index]
            ])

            distances.append(distance)

        return distances

    def __find_best_area(self, areas):
        """
        dsadasdasdasdasd
        """

        return areas.index(min(areas))

    def fit(self):
        """
        dsadasdasdasdasd
        """

        while len(self.list_of_bounding_boxes) != 0:
            # list of determined areas for each line
            determined_areas = self.__determine_areas()
            # area length for each line
            areas_length = self.__areas_length(determined_areas)
            # max area length
            max_area_length = self.__max_area_length(areas_length)
            # index of max area length
            area_max_length_index = self.__get_areas_max_length_index(
                areas_length, max_area_length)
            # list of sum of distanes from points to the lines
            area_min_distance = self.__find_minimum_distances(
                area_max_length_index, determined_areas)
            # index of the shortest distance
            shortest_area_distance_index = self.__find_best_area(
                area_min_distance)

            area = []
            for bbox_index in sorted(
                    determined_areas[
                        area_max_length_index[shortest_area_distance_index]],
                    reverse=True):
                area.append(self.list_of_bounding_boxes[bbox_index])
                self.list_of_bounding_boxes.pop(bbox_index)

            self.areas.append(area)
