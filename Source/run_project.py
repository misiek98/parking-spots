from itertools import chain

import cv2
import numpy as np

from haar_model.tools.data_processing import DataProcessingMethods, Point, get_position
from haar_model.tools.other_functions import load_config

config = load_config(
    r'C:\Users\Misiek\Desktop\Python\MGR\Source\project_config.json'
)

with open(config['yoloNames']) as f:
    labels = [line.strip() for line in f]

network = cv2.dnn.readNetFromDarknet(
    config['yoloCfg'],
    config['yoloWeights']
)

PROBABILITY_MINIMUM = config['probabilityMinimum']
THRESHOLD = config['threshold']
video = cv2.VideoCapture(config['video'])

colours = np.random.randint(
    low=0,
    high=255,
    size=(len(labels), 3),
    dtype='uint8'
)

list_of_points = []
list_of_parking_areas = []

frame_number = 1
while True:
    ret, frame = video.read()
    if ret == False:
        cv2.waitKey(0)
        # break

    img = frame.copy()

    if (frame_number == 2):
        grayImage = cv2.cvtColor(
            src=img,
            code=cv2.COLOR_BGR2GRAY
        )
        lineDetector = cv2.CascadeClassifier(
            config['cascadeXML']
        )
        lineRegions = lineDetector.detectMultiScale(
            image=grayImage,
            scaleFactor=1.13,
            minNeighbors=3,
            minSize=(105, 27),
            maxSize=(270, 80),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Change from numpy array to my concept.
        for x, y, w, h in lineRegions:
            list_of_points.append(Point(x, y))
            list_of_points.append(Point(x + w, y + h))

        DataProcessingMethods.draw_rectangles(
            list_of_points=list_of_points,
            img=img
        )

        while True:
            cv2.namedWindow('Frame')
            cv2.setMouseCallback(
                window_name='Frame',
                on_mouse=get_position,
                param=[img, list_of_points]
            )
            cv2.imshow('Frame', img)

            # Press "w" to remove detected objects.
            # As an input take an rectangle(s) id separated by spaces.
            if (cv2.waitKey(1) == ord('w')):
                img = frame.copy()

                user_input = input(
                    'Choose a rectangle(s) id to drop (separated by spaces): ')
                user_input = [int(number) for number in user_input.split()]
                user_input = sorted(user_input, reverse=True)

                for idx in user_input:
                    list_of_points.pop(2*idx + 1)
                    list_of_points.pop(2 * idx)

                DataProcessingMethods.draw_rectangles(
                    list_of_points=list_of_points,
                    img=img
                )
                print(
                    f'Rectangle(s) number {user_input}',
                    'have been successfully removed!')

            # Press "r" to remove last marked point.
            if (cv2.waitKey(1) == ord('r')):
                img = frame.copy()

                if (len(list_of_points) > 0):
                    list_of_points.pop()

                if (len(list_of_points) % 2 != 0):
                    DataProcessingMethods.draw_rectangles(
                        list_of_points=list_of_points[:-1],
                        img=img
                    )
                    DataProcessingMethods.draw_points(
                        img=img,
                        list_of_points=list_of_points[-1:]
                    )
                else:
                    DataProcessingMethods.draw_rectangles(
                        list_of_points=list_of_points,
                        img=img
                    )

            # Press "d" to draw manually new rectangle(s).
            if (cv2.waitKey(1) == ord('d')):
                img = frame.copy()

                DataProcessingMethods.draw_rectangles(
                    list_of_points=list_of_points,
                    img=img
                )

            # Press "n" to automatically specify parking zones
            # After that, the program starts measuring the occupancy
            # of parking spaces
            if (cv2.waitKey(1) == ord('n')):
                # change from Point instances to NumPy array
                DataProcessingMethods.prepare_vector_data(
                    list_of_points=list_of_points
                )
                list_of_points = list(
                    chain.from_iterable(
                        (point.x, point.y)
                        for point in list_of_points
                    )
                )
                list_of_points = np.array(list_of_points).reshape(-1, 4)

                # Calculating the angles of the upper left corners
                # of rectangles
                angles = []
                for x, y, _, _ in list_of_points:
                    angles.append(
                        np.arctan((img.shape[0] - y) / x)
                    )
                angles = [int(np.degrees(angle)) for angle in angles]

                # Sort the angles in descending order
                rectangles_with_angles = []
                for (x, y, w, h), angle in zip(list_of_points, angles):
                    rectangles_with_angles.append((x, y, w, h, angle))

                rectangles_with_angles = np.array(
                    object=rectangles_with_angles,
                    dtype=[
                        ('x', int),
                        ('y', int),
                        ('w', int),
                        ('h', int),
                        ('angle', int)
                    ]
                )
                rectangles_with_angles = np.sort(
                    rectangles_with_angles,
                    order='angle'
                )
                rectangles_with_angles = rectangles_with_angles[::-1]

                # Automatic determination of parking zones
                for x, y, w, h, _ in rectangles_with_angles:
                    top_left = (x, y)
                    top_right = (x + w, y)
                    bottom_left = (x, y + h)
                    bottom_right = (x + w, y + h)
                    flag = True

                    rectangle = np.array(
                        (top_left, top_right, bottom_right, bottom_left)
                    )

                    if (len(list_of_parking_areas) == 0):
                        list_of_parking_areas.append([rectangle])

                    else:
                        for area in list_of_parking_areas:
                            is_in_parking_area = cv2.pointPolygonTest(
                                contour=area[-1],
                                pt=top_left,
                                measureDist=False
                            )
                            if (is_in_parking_area == 1):
                                area.append(rectangle)
                                flag = False
                                break

                        if flag:
                            list_of_parking_areas.append([rectangle])

                list_of_parking_areas = list(
                    chain.from_iterable(
                        (area[0], area[-1])
                        for area in list_of_parking_areas
                    )
                )

                list_of_parking_areas = list(
                    chain.from_iterable(
                        (element[3], element[1])
                        for element in list_of_parking_areas
                    )
                )
                list_of_parking_areas = np.array(
                    list_of_parking_areas).reshape(-1, 4, 2)
                for dim in list_of_parking_areas:
                    dim[[2, 3]] = dim[[3, 2]]

                cv2.destroyAllWindows()
                frame_number += 1
                break

    if (frame_number % 60 == 0):
        h, w = None, None
        layers_names_all = network.getLayerNames()
        layers_names_output = \
            [layers_names_all[i - 1]
             for i in network.getUnconnectedOutLayers()]

        if w is None or h is None:
            h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(
            image=frame,
            scalefactor=1 / 255.,
            size=(416, 416),
            swapRB=True,
            crop=False
        )

        network.setInput(blob)
        output_from_network = network.forward(layers_names_output)

        bounding_boxes = []
        confidences = []
        classIDs = []

        for result in output_from_network:
            for detected_objects in result:
                scores = detected_objects[5:]
                class_current = np.argmax(scores)
                confidence_current = scores[class_current]

                if (confidence_current > PROBABILITY_MINIMUM):
                    box_current = detected_objects[0:4] * \
                        np.array([w, h, w, h])

                    # The YOLO vector contains the center of the object.
                    # However, the application allows objects to be
                    # determined (uncomment lines 273 - 293), so I
                    # decided to recalculate the rectangle coordinates
                    # anyway.
                    x_center, y_center, box_width, box_height = box_current
                    x_min = int(x_center - box_width//2)
                    y_min = int(y_center - box_height//2)

                    bounding_boxes.append(
                        [x_min, y_min, int(box_width), int(box_height)])
                    confidences.append(float(confidence_current))
                    classIDs.append(class_current)

        results = cv2.dnn.NMSBoxes(
            bounding_boxes,
            confidences,
            PROBABILITY_MINIMUM,
            THRESHOLD
        )

        number_of_cars = 0
        if (len(results) > 0):
            for i in results.flatten():
                x_min = bounding_boxes[i][0]
                y_min = bounding_boxes[i][1]
                box_width = bounding_boxes[i][2]
                box_height = bounding_boxes[i][3]

                object_central_point = (
                    x_min + box_width//2,
                    y_min + box_height//2
                )

                for area in list_of_parking_areas:
                    is_in_parking_area = cv2.pointPolygonTest(
                        contour=area,
                        pt=object_central_point,
                        measureDist=False
                    )
                    if (is_in_parking_area == 1):
                        number_of_cars += 1
                        break

                # Draw the parking areas
                # for e in list_of_parking_areas:
                #     cv2.drawContours(
                #         image=frame,
                #         contours=[e],
                #         contourIdx=-1,
                #         color=(0, 255, 0),
                #         thickness=-1
                #     )

                # Mark each detected object
                # colour_box_current = colours[classIDs[i]].tolist()
                # cv2.rectangle(
                #     img=frame,
                #     pt1=(x_min, y_min),
                #     pt2=(x_min + box_width, y_min + box_height),
                #     color=colour_box_current,
                #     thickness=2
                # )
                # text_box_current = '{}: {:.4f}'.format(
                #     labels[int(classIDs[i])],
                #     confidences[i]
                # )
                # cv2.putText(
                #     img=frame,
                #     text=text_box_current,
                #     org=(x_min, y_min - 5),
                #     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                #     fontScale=0.5,
                #     color=colour_box_current,
                #     thickness=2
                # )

        # Highligh a place to display an information about
        # occupancy of parking spaces
        frame[:120, -500:] = 0

        total_number_of_parking_spots = (len(list_of_points)//2
                                         - len(list_of_parking_areas))
        number_of_occupied_parking_spots = number_of_cars
        number_of_free_parking_spots = (total_number_of_parking_spots
                                        - number_of_occupied_parking_spots)

        cv2.putText(
            img=frame,
            text=("Total number of parking spaces:"
                  f" {total_number_of_parking_spots}"),
            org=(frame.shape[1] - 480, 25),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.7,
            color=(100, 100, 255),
            thickness=2
        )
        cv2.putText(
            img=frame,
            text=("Number of free parking spaces:"
                  f" {number_of_free_parking_spots}"),
            org=(frame.shape[1] - 480, 65),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.7,
            color=(100, 255, 0),
            thickness=2
        )
        cv2.putText(
            img=frame,
            text=("Number of occupied parking spaces:"
                  f" {number_of_occupied_parking_spots}"),
            org=(frame.shape[1] - 480, 105),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.7,
            color=(0, 0, 255),
            thickness=2
        )

        cv2.imshow(
            winname='Frame',
            mat=frame)

        cv2.waitKey(1)
    frame_number += 1
