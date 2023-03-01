import numpy as np

from images.bounding_box import BoundingBox
from models_api.linear_clusterization.linear_function import LinearFunction
from models_api.linear_clusterization.factors import Factor


class LinearClusterization:
    """
    Contains methods for linear clustering.

    Attributes:
    ----------
    list_of_bounding_boxes: list
        A list that stores BoundingBox objects.

    angle_step: int
        A value by which the current angle changes in compare to the 
        previous one. Must be greater than or equal to 1 and less than 
        or equal to 180.

    seed: int
        Allows to reproduce a result.

    areas: list
        A list that stores sublists with BoundingBox objects. Those
        sublists determine different clusters.


    Methods:
    -------
    fit(factor)
        Runs training and determines areas (clusters).
    """

    def __init__(self, list_of_bounding_boxes: list, angle_step: int,
                 seed=42, areas=[]):
        self.list_of_bounding_boxes = list_of_bounding_boxes.copy()
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
        A list that stores a LinearFunction objects.
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
        Sorts distances from points to the line in ascending order.

        Attributes:
        ----------
        line: LinearFunction
            An instance of the LinearFunction class with its requirements.
        """

        if not isinstance(line, LinearFunction):
            raise TypeError(
                "The line parameter must be of type LinearFunction, not "
                f"{type(line).__name__}.")

        return sorted(line.list_of_distances,
                      key=lambda x: x.point_to_line_distance)

    def __only_distances(self, list_of_distances):
        """
        A list that stores only distances from points to the line, 
        without indexes.
        """

        if not isinstance(list_of_distances, list):
            raise TypeError(
                "The list_of_distances parameter must be of type list, not "
                f"{type(list_of_distances).__name__}.")

        for element in list_of_distances:
            if not isinstance(element, tuple):
                raise TypeError(
                    "Elements inside the list_of_distances must be of type "
                    f"tuple, not {type(list_of_distances).__name__}.")

        return [distance.point_to_line_distance
                for distance in list_of_distances]

    def __determine_areas(self, factor):
        """
        For each line from list_of_lines_different_angles this function
        determines different areas.

        Parameters:
        ----------
        factor: Factor 
            A name of method from the Factor class.

        Returns:
        -------
        A list with determined areas.
        """

        areas = []

        for index, point_to_line_distances in enumerate(
                self. __list_of_lines_different_angles):
            sorted_list_of_distances = self.__sort_distances(
                point_to_line_distances)
            only_distances = self.__only_distances(sorted_list_of_distances)

            match factor:
                case "max_mean":
                    fac = Factor(only_distances).max_mean()

                case _:
                    raise AttributeError(
                        """The specified factor name does not exist, 
                        select one of the coefficients from the list:\n
                            max_mean
                        """)

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
        Returns a list that stores number of elements in each area.

        Parameters:
        ----------
        areas:
            Determined clusters.
        """

        return [
            len(area)
            for area in areas]

    def __max_area_length(self, areas_length):
        """
        Returns a value that determiens the maximum number of elements 
        in the area.

        Parameters:
        ----------
        areas_length:
            A list that stores number of elements in each area.
        """

        return max(areas_length)

    def __get_areas_max_length_index(self, areas_length, max_area_length):
        """
        Returns index(es) of the area(s) with the maximum number of 
        elements.

        Parameters:
        ----------
        areas_length: list
            A list that stores number of elements in each area.

        max_area_length: int
            Maximum number of elements
        """

        return np.where(
            np.array(areas_length) == max_area_length)[0]

    def __find_minimum_distances(self, areas_index_max_length, det_areas):
        """
        In case of the multiple areas with the same number of elements, 
        this method calculates the total distance from points to the 
        line.

        Parameters:
        ----------
        areas_index_max_length:
            A list that contains index(es) with the maximum number of 
            elements.

        det_areas:
            Determined areas.
        """

        distances = []

        for index in areas_index_max_length:
            line = self.__list_of_lines_different_angles[index]
            distance = sum([
                point.point_to_line_distance
                for point in line.list_of_distances
                if point.point_index in det_areas[index]
            ])

            distances.append(distance)

        return distances

    def __find_best_area(self, areas):
        """
        Returns the list position of the area with the shortest distance
        from points to the line.

        Parameters:
        ----------
        areas:
            A list with total distances from points to the line.
        """

        return areas.index(min(areas))

    def fit(self, factor):
        """
        A method that starts the training.

        Parameters:
        ----------
        factor: str
            A name of the method from the Factor class.
        """

        while len(self.list_of_bounding_boxes) != 0:
            # determining areas for the each line
            determined_areas = self.__determine_areas(factor)
            # determining a number of elements in the area for the
            # each line
            areas_length = self.__areas_length(determined_areas)
            # determining maximum length of the area
            max_area_length = self.__max_area_length(areas_length)
            # determining index(es) of areas with the largest number
            # of elements
            area_max_length_index = self.__get_areas_max_length_index(
                areas_length, max_area_length)
            # for each area with the largest number of elements calculate
            # the total distance from these points to the line
            area_min_distance = self.__find_minimum_distances(
                area_max_length_index, determined_areas)
            # determining the index of area with the least distance
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
