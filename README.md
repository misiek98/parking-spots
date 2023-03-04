This is the previous version of the project, which was created almost a year ago.


# Parking-Spot-Detector
Parking-Spot-Detector is an implementation of a semi-automatic method for determining the occupancy of parking spaces. For this purpose, I've created a Haar-Cascade model that has been combined with the YOLOv3 model by Darknet [[4]](https://github.com/pjreddie/darknet).


# Workflow

## Haar-Cascade
After receiving a frame from parking camera, I made some experiments (e.g. detecting edges, binarizing etc.). Finally I've decided to develop a Haar–Cascade model which is responsible for detecting parking lines.\
The work began with the development of a few auxiliary methods to facilitate the development of the model. After that, all parking lines were marked.

![1](https://user-images.githubusercontent.com/76869717/167130691-0dd0b34f-039f-427b-b9b7-183c15f7e287.png)

I carried out many tests to find the best configuration. To judge if the model detects lines correctly, I developed a function that selected around 60 of the best solutions from more than 1,200 parameter combinations. Then they were evaluated manually and the best model parameters were selected.

![2](https://user-images.githubusercontent.com/76869717/167130715-3405ea1f-fd19-4abb-8ad3-9b998caf9afd.png)

However, the main goal of this project was to determine the number of free parking spaces on the basis of the videoframe. I prepared a short video to evaluate the effectiveness of the application.
On the first frame that shows empty parking lot, Haar-Model detects parking lines. If any line were missed, it's possible to mark it manually (this is a semi-automatic part of the method).

![3](https://user-images.githubusercontent.com/76869717/167130738-1f0f0c08-5f51-4c1c-a53f-bbdd5ee4d2c3.jpg)

The image above shows the result of a random parameterization of the Haar algorithm. The result can be improved by using simple keyboard shortcuts:
- *Double left mouse button*: mark new point (mouse callback),
- *w*: remove selected rectangles,
- *r*: remove last marked point,
- *d*: draw missing rectangles (requires new marked points),
- *n*: automatically specifying parking zones and proceed to determining the parking occupancy.

The corrected result is shown in the following figure:

![5](https://user-images.githubusercontent.com/76869717/167130866-4ab910fe-0383-4443-82a5-e620e66f329c.png)

When all lines are marked, the contours of the parking zones are selected. It allows to distinguish the parking zones from - for example - the access roads.

![6](https://user-images.githubusercontent.com/76869717/167130898-1de0b601-fe1d-4566-97ab-2a2309e61c6f.png)

## Combining with YOLOv3

When all zones were defined, the YOLOv3 algorithm detects only cars. After that rest of the application checks if the centers of the detected vehicles are within the zones. If so, one of the parking spot is considered as occupied.

![7](https://user-images.githubusercontent.com/76869717/167130922-d3566bd2-c626-432c-9cbb-c3dce8c9c09e.png)


# Possible improvements

- Increase the number of training samples for the detection of parking lines,
- implement a GUI instead of keyboard shortcuts.


# Conclusion

Even with a small number of samples, I was able to create a Haar-Cascade model that works decently. With a larger dataset, I could certainly get even better results.\
A similar method can be used in many cases. You can test it by cloning the repository [[4]](https://github.com/pjreddie/darknet) and downloading the weights ([link](https://pjreddie.com/media/files/yolov3.weights)). 


# Sources:
[1] Viola P., M., Rapid Object Detection Using a Boosted Cascade of Simple Features. [Article](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.415.8118).\
[2] Redmon J., Divvala S., Girshick R., Farhadi A., You Only Look Once: Unified, Real-Time Object Detection. [Article](https://pjreddie.com/media/files/papers/yolo_1.pdf).\
[3] Redmon J., Farhadi A., YOLOv3: An Incremental Improvement. [Article](https://pjreddie.com/media/files/papers/YOLOv3.pdf).\
[4] [Darknet repository](https://github.com/pjreddie/darknet).
