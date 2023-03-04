from datetime import datetime

import cv2

from models_api.linear_clusterization.linear_clusterization import \
    LinearClusterization
from models_api.yolov5.yolo_model import YoloModel
from images.coordinate import Coordinate
from images.area import ParkingArea
from images.other_functions import (write_parking_information,
                                    prepare_place_for_informations)

video = cv2.VideoCapture("path_to_video")

lines_yolo_model = YoloModel("path_to_model")
cars_yolo_model = YoloModel(
    "path_to_model")
cars_yolo_model.model.classes = [2]

frame_number = 0
while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    img = frame.copy()

    if frame_number == 0:
        print("Detecting parking lines...")
        list_of_parking_lines = lines_yolo_model.detect(img)
        print(f"Found {len(list_of_parking_lines)} parking lines.")
        print()

        print("Determining parking areas...")
        linear_cluster = LinearClusterization(
            list_of_bounding_boxes=list_of_parking_lines,
            angle_step=1)
        linear_cluster.fit("max_mean")

        print(f"Found {len(linear_cluster.areas)} areas.")
        list_of_areas = [
            ParkingArea(area, img.shape[1], img.shape[0])
            for area in linear_cluster.areas
        ]

        for area in list_of_areas:
            area.draw_area(img)

        print("Displaying area...")
        cv2.imshow("camera_view", img)
        cv2.waitKey(5000)
        print()

    elif frame_number % 30 == 0:
        detected_cars = cars_yolo_model.detect(img)
        print(datetime.now().strftime("%d.%m.%Y; %H:%M:%S"))
        print(f"Total number of found cars: {len(detected_cars)}.")

        for car in detected_cars:
            car_bbox_center = Coordinate(car.x_center, car.y_center)

            for area in list_of_areas:
                if area.is_in_area(car_bbox_center) == 1:
                    area.occupy_parking_spot()

        total_parking_spots = sum(area.number_of_parking_spots
                                  for area in list_of_areas)

        total_occupied_parking_spots = sum(area.occupied_parking_spots
                                           for area in list_of_areas)

        free_parking_spots = total_parking_spots - total_occupied_parking_spots

        print(f"{total_occupied_parking_spots} cars in "
              f"{total_parking_spots} parking spots.")
        print()

        prepare_place_for_informations(img, 0, 120, -500, -1)

        write_parking_information(
            img=img,
            text=("Total number of parking spots:"
                  f" {total_parking_spots}"),
            text_place=(img.shape[1] - 480, 25),
            color=(100, 100, 255))

        write_parking_information(
            img=img,
            text=("Number of free parking spots:"
                  f" {free_parking_spots}"),
            text_place=(img.shape[1] - 480, 65),
            color=(100, 255, 0))

        write_parking_information(
            img=img,
            text=("Number of occupied parking spots:"
                  f" {total_occupied_parking_spots}"),
            text_place=(img.shape[1] - 480, 105),
            color=(0, 0, 255))

        cv2.imshow("camera_view", img)
        cv2.waitKey(2000)

    for area in list_of_areas:
        area.forget_detected_cars()

    frame_number += 1
