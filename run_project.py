import cv2
import numpy as np

from models_api.linear_clusterization.linear_clusterization import \
    LinearClusterization
from models_api.yolov5.yolo_model import YoloModel

from images.bounding_box import BoundingBox
from images.coordinate import Coordinate
from images.area import ParkingArea

video = cv2.VideoCapture(
    "/home/misiek/Pulpit/python/cars_on_parking.mp4")

# lines_yolo_model = YoloModel("path_to_model")
cars_yolo_model = YoloModel(
    "/home/misiek/Pulpit/python/yolov5/yolov5s.pt")
cars_yolo_model.model.classes = [2]

# frame_number = 0
# # 1. Wykryj linie
# # 2. Utwórz strefy
# # 3. Wyznacz krańcowe bboxy i stwórz streefy
# # 4. Wykryj pojazdy
# # 5. Sprawdź czy pojazdy są wewnątrz strefy


frame_number = 0

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    img = frame.copy()

    if frame_number == 0:
        # print("Detecting parking lines...")
        # list_of_parking_lines = lines_yolo_model.detect(img)
        # print(f"Found {len(list_of_parking_lines)} parking lines.")
        # print()

        coords = "680 761 255 99 586 689 286 98 550 623 268 87 521 567 253 77 494 516 240 71 471 473 228 63 451 437 218 55 432 397 207 54 413 366 200 47 398 336 192 45 383 309 185 41 1255 660 272 124 1173 600 255 108 1104 547 238 95 1042 499 223 83 985 452 215 77 936 413 205 69 891 378 200 63 851 346 191 58 817 317 181 55 785 292 170 49 755 267 167 47 729 244 160 43 704 222 154 42 680 204 149 41 658 188 143 36 638 171 139 36 620 153 140 36 1432 415 169 58 1361 379 163 52 1298 345 162 51 1243 315 155 44 1186 287 154 41 1141 262 144 39 1097 239 140 38 1056 216 138 38 1020 196 133 37 987 179 125 32 954 162 124 31 923 144 123 31 895 132 118 28 869 117 116 27"
        coords = np.array([int(e) for e in coords.split(" ")]).reshape(-1, 4)

        list_of_parking_lines = []

        for x, y, w, h in coords:
            list_of_parking_lines.append(
                BoundingBox([Coordinate(int(x), int(y)),
                            Coordinate(int(x+w), int(y+h))])
            )

        print("Looking for areas...")
        linear_cluster = LinearClusterization(
            list_of_bounding_boxes=list_of_parking_lines,
            angle_step=1)

        linear_cluster.fit("max_mean")
        print(f"Found {len(linear_cluster.areas)} areas.")
        list_of_areas = [
            ParkingArea(area, frame.shape[1], img.shape[0])
            for area in linear_cluster.areas
        ]

    elif frame_number % 30 == 0:
        detected_cars = cars_yolo_model.detect(frame)
        print(f"Found {len(detected_cars)} cars.")

        for car in detected_cars:
            car_bbox_center = Coordinate(car.x_center, car.y_center)

            for area in list_of_areas:
                if area.is_in_area(car_bbox_center) == 1:
                    area.occupied_parking_spots += 1

        for area in list_of_areas:
            area.prepare_img(img)
            area.draw_area(img)
            area.print_information(img)

        cv2.imshow("img", img)
        cv2.waitKey(1)

    for area in list_of_areas:
        print(
            f"{area.occupied_parking_spots} cars in "
            f"{area.number_of_parking_spots} spots")
    print()
    print()

    for area in list_of_areas:
        # area.occupied_parking_spots = 0
        area.forget_detected_cars()

    frame_number += 1
