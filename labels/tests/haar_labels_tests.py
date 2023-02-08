import unittest

from parameterized import parameterized

from labels.haar_labels import HaarLabel


class TestHaarLabel(unittest.TestCase):
    haar_labels = HaarLabel("./data/file.bmp")

    @parameterized.expand(
        [
            ("tuple", ()),
            ("dict", {})
        ]
    )
    def test_list_of_bounding_boxes_setter(self, name, value):
        with self.assertRaises(TypeError):
            TestHaarLabel.haar_labels.list_of_bounding_boxes = value

    @parameterized.expand(
        [
            ("list", [1, 2, 3]),
            ("int", 10),
            ("float", 0.11)
        ]
    )
    def test_save_data_to_file_file_path(self, name, value):
        with self.assertRaises(TypeError):
            TestHaarLabel.haar_labels.save_data_to_file(value)
