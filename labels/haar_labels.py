from images.image import Image


class HaarLabel(Image):
    """
    Allows to save data in proper format for the Haar-Cascade model.

    Methods:
    ----------
    save_data_to_file
    """

    def __init__(self, path: str):
        super().__init__(path)

    def __prepare_data(self):
        string = ""
        string += f"{self.path} {len(self.list_of_bounding_boxes)} "

        for bbox in self.list_of_bounding_boxes:
            string += (
                f"{bbox.top_left_x} "
                f"{bbox.top_left_y} "
                f"{bbox.bbox_width} "
                f"{bbox.bbox_height} "
            )

        string = string.strip() + "\n"
        return string

    def save_data_to_file(self, file_path: str):
        """
        Allows you to save formatted labels to a file.
        """
        if not isinstance(file_path, str):
            raise TypeError(
                "The file_path attribute must be of type string, not "
                f"{type(file_path).__name__}.")

        with open(file=file_path, mode="a", encoding="utf8") as file:
            file.write(self.__prepare_data())
