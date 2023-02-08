import os

import cv2

from images.coordinate import get_coordinate
from images.image import ImageDraw
from labels.haar_labels import HaarLabel
from labels.YOLOv5_labels import YOLOv5Label


list_of_images = [
    os.path.join(os.getcwd(), "data", image)
    for image in os.listdir("./data")
    if image.split(".")[-1] in ["bmp", "jpeg", "jpg", "png"]
]

for img_path in list_of_images:
    image_properties = ImageDraw(img_path)
    img = cv2.imread(image_properties.path)

    while True:
        cv2.namedWindow(image_properties.path)
        cv2.setMouseCallback(
            window_name=image_properties.path,
            on_mouse=get_coordinate,
            param=[img, image_properties])

        if (cv2.waitKey(1) == ord("a")):
            img = image_properties.draw_coordinates(img)

        if (cv2.waitKey(1) == ord("s")):
            img = image_properties.draw_bounding_boxes(img)

        if (cv2.waitKey(1) == ord("d")):
            img = image_properties.clean_image()

        if (cv2.waitKey(1) == ord("r")):
            image_properties.remove_last_coordinate()
            img = image_properties.clean_image()
            img = image_properties.draw_coordinates(img)

        if (cv2.waitKey(1) == ord("n")):
            haar_label = HaarLabel(image_properties.path)
            haar_label.list_of_coordinates = image_properties.\
                list_of_coordinates
            haar_label.save_data_to_file(
                file_path="./training/labels/haar_labels/haar.txt")

            file_name = image_properties.path.split("/")[-1].split(".")[0]
            yolov5_label = YOLOv5Label(image_properties.path)
            yolov5_label.list_of_coordinates = image_properties.\
                list_of_coordinates
            yolov5_label.save_data_to_file(
                file_path=f"./training/labels/yolov5_labels/{file_name}.txt")

            cv2.destroyWindow(image_properties.path)
            break

        cv2.imshow(image_properties.path, img)
