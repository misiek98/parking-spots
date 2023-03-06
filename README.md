# parking-spots

The parking-spots project is an implementation of an automatic method for determining the occupancy of parking spaces. For this purpose, I've created an YOLOv5 [[3]](https://github.com/ultralytics/yolov5), [[4]](https://pytorch.org/hub/ultralytics_yolov5/) model that detects parking lines. For car detection I've decided to use the YOLOv5 model previously trained on COCO dataset.

![7](https://user-images.githubusercontent.com/76869717/167130922-d3566bd2-c626-432c-9cbb-c3dce8c9c09e.png)


# Workflow

## Preparation of tools
At the beginning a tools were created which store information and allow to perform operations on images. For this purpose the several classes have been created - Coordinate, Image, ImageDraw and BoundingBox.
- Coordinate stores x and y coordinates of the point,
- Image stores information about the size of the photo and the list with coordinates which allow to perform the operations on the image,
- ImageDraw allow to draw the coordinates and BoundingBox on the image,
- BoundingBox stores the information about the left-top corner of the bounding box - its length, height and center

## Creating templates of data labels
The HaarLabels and YOLOv5Labels classes were created, which allow processing the data about localization of the bounding box and saving them to a text file. Then the script was created for data labeling. Next, the several dozen of photos with parking lines were labeled and the results have been saved in /traininig/labels folder.

![labelS](https://user-images.githubusercontent.com/76869717/222917248-2fbf2016-dd17-49c3-b272-de16dfc4738c.png)

## Developing a linear clustering algorithm
In a few words, a line passes through the random-chosen BoundingBox center. The line is sloped at different angles. Then it is checked which line has the greatest number of points in its neighbor. These points are considered as a group and are removed from the list. The whole process is repeated until each point is assigned to a group.\
The algorithm works decently on relatively small number of parking spots (about 60), however it doesn't perform well on huge parking lot of shopping center. Currently we're focusing on algorithm improvement.

## Creating model interfaces
Classes YOLOv5Model and HaarModel were created and allow to detect objects with a single line of code. These models return a list of BoundingBox objects with recognized targets.

## Combining all elements into a working project
On the first video frame, the YOLOv5 model detects parking lines that separate parking spots.

![5](https://user-images.githubusercontent.com/76869717/167130866-4ab910fe-0383-4443-82a5-e620e66f329c.png)

Based on detected lines, the cluster algorithm determines parking areas and calculates the number of available parking spots.

![6](https://user-images.githubusercontent.com/76869717/167130898-1de0b601-fe1d-4566-97ab-2a2309e61c6f.png)

When all zones are defined, the other YOLOv5 model detects cars only. After that, rest of the application checks if the centers of the detected vehicles are within the zones. If so, one of the parking spot is considered as occupied. If not, it is most likely that the car is passing or standing on a forbidden spot. The information about occupied parking spots is displayed in the top right corner of the screen and is printed in the console.

![occupancy](https://user-images.githubusercontent.com/76869717/222917249-90378b07-7c3d-4f58-9fd6-5f161a06f39f.png)


# Possible improvements

- Increase the number of training samples for the detection of parking lines,
- implement a GUI instead of keyboard shortcuts.


# Sources:
[1] Viola P., M., Rapid Object Detection Using a Boosted Cascade of Simple Features. [Article](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.415.8118).\
[2] [YOLOv5 website](https://ultralytics.com/).\
[3] [YOLOv5 repository](https://github.com/ultralytics/yolov5).\
[4] [YOLOv5 torch website](https://pytorch.org/hub/ultralytics_yolov5/).
