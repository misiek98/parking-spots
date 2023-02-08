from images.image import Image


class YOLOv5Label(Image):
    """
    Allows to save data in proper format for the YOLOv5 model.

    Methods:
    ----------
    save_data_to_file
    """

    def __init__(self, path: str):
        super().__init__(path)

    def __prepare_data(self):
        string = ""
        for bbox in self.list_of_bounding_boxes:
            x_center = bbox.x_center / self.width
            y_center = bbox.y_center / self.height
            width = bbox.bbox_width / self.width
            height = bbox.bbox_height / self.height

            string += (
                "0 "
                f"{x_center} "
                f"{y_center} "
                f"{width} "
                f"{height}\n")

        return string

    def save_data_to_file(self, file_path: str):
        with open(file=file_path, mode="a", encoding="utf8") as file:
            file.write(self.__prepare_data())
