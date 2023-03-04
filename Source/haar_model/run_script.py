import os

import cv2
import shutil

from tools.data_processing import DataProcessingMethods, get_position
from tools.other_functions import load_config

config = load_config(
    r'C:\Users\Misiek\Desktop\Python\MGR\Source\haar_model\haar_config.json')

list_of_points = []
IMAGE_SET = config['data']
# path_to_info_file contains points required to train haar_model
PATH_TO_INFO_FILE = config['parkingLinesInfoFile']
POS_IMAGE_DIR = config['posDir']

for image in os.listdir(IMAGE_SET):
    image_path = os.path.join(
        IMAGE_SET,
        image
    )
    img = cv2.imread(image_path)

    while True:
        cv2.namedWindow('Parking space')
        cv2.setMouseCallback(
            window_name='Parking space',
            on_mouse=get_position,
            param=[img, list_of_points]
        )

        cv2.imshow(
            winname='Parking space',
            mat=img.copy()
        )

        # by pressing 'n' program process data from listOfPoints,
        # save it to parking_lines.info file and copy image from data
        # dir to pos folder
        if (cv2.waitKey(1) == ord('n')):
            try:
                assert len(list_of_points) % 2 == 0

                DataProcessingMethods.prepare_vector_data(
                    list_of_points=list_of_points
                )

                with open(PATH_TO_INFO_FILE, 'a') as file:
                    file.write(
                        f'{POS_IMAGE_DIR} {int(len(list_of_points) / 2)} ')
                    for coordinate in list_of_points:
                        file.write(f'{coordinate.x} {coordinate.y} ')
                    file.write('\n')

                list_of_points.clear()
                print(f'File was saved: {PATH_TO_INFO_FILE}')

                shutil.copyfile(
                    src=image_path,
                    dst=os.path.join(
                        POS_IMAGE_DIR,
                        image
                    )
                )
                break

            except AssertionError:
                print("Insufficient number of points, data wasn't saved")
                list_of_points.clear()
                break

        # by pressing 'c' program cuts out the marked part(s) of
        # the image and saves it to the neg folder.
        if (cv2.waitKey(1) == ord('c')):
            try:
                assert len(list_of_points) % 2 == 0

                img = cv2.imread(image_path)
                DataProcessingMethods.save_marked_area(
                    list_of_points=list_of_points,
                    img=img
                )
                list_of_points.clear()
                break

            except AssertionError:
                print("Insufficient number of points, image wasn't saved")
                list_of_points.clear()
                break

        # by pressing 'd' program displays image with
        # drawn rectangles around marked objects
        if (cv2.waitKey(1) == ord('d')):
            try:
                assert len(list_of_points) % 2 == 0

                image_with_rectangles = cv2.imread(image_path)
                cv2.imshow(
                    winname='Marked objects',
                    mat=DataProcessingMethods.draw_rectangles(
                        list_of_points=list_of_points,
                        img=image_with_rectangles
                    )
                )

            except AssertionError:
                print('Insufficient number of points,',
                      'rectangles cannot be drawn.')

        # by pressing 'r' program removes last point from listOfPoints
        # and from image
        if (cv2.waitKey(1) == ord('r')):
            img = cv2.imread(image_path)

            if (len(list_of_points) > 0):
                list_of_points.pop()
            DataProcessingMethods.draw_points(
                img=img,
                list_of_points=list_of_points
            )
