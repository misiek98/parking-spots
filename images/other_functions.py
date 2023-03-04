import cv2
import numpy as np


def prepare_place_for_informations(img: np.ndarray,
                                   from_height: int,
                                   to_height: int,
                                   from_width: int,
                                   to_width: int):
    """
    Draws a black area on provided image on which you can put text.

    Parameters:
    ----------
    img: np.ndarray
        The image on which you can put an information.

    from_height: int
        The height coordinate from which you want to draw black area.

    to_height: int
        The height coordinate to which you want to draw black area.

    from_width: int
        The width coordinate from which you want to draw black area.

    to_width: int
        The width coordinate to which you want to draw black area.
    """

    if not isinstance(from_height, int):
        raise TypeError(
            "The from_height parameter must be of type int, not "
            f"{type(from_height).__name__}.")

    if not isinstance(to_height, int):
        raise TypeError(
            "The to_height parameter must be of type int, not "
            f"{type(to_height).__name__}.")

    if not isinstance(from_width, int):
        raise TypeError(
            "The from_width parameter must be of type int, not "
            f"{type(from_width).__name__}.")

    if not isinstance(to_width, int):
        raise TypeError(
            "The to_width parameter must be of type int, not "
            f"{type(to_width).__name__}.")

    img[from_height:to_height, from_width:to_width] = 0


def write_parking_information(img: np.ndarray,
                              text: str,
                              text_place: tuple,
                              color: tuple):
    """
    Puts the text information on the provided image.

    Parameters:
    ----------
    img: np.ndarray
        The image on which you want to put an information.

    text: str
        A message content you want to put on the image.

    text_place: tuple
        Text coordinates.

    color: tuple
        Text color.
    """

    if not isinstance(img, np.ndarray):
        raise TypeError(
            "The img parameter must be of type np.ndarray, "
            f"not {type(img).__name__}.")

    if not isinstance(text, str):
        raise TypeError(
            "The text parameter must be of type str, "
            f"not {type(text).__name__}.")

    if not isinstance(text_place, tuple):
        raise TypeError(
            "The text_place parameter must be of type tuple, "
            f"not {type(text_place).__name__}.")

    if not isinstance(color, tuple):
        raise TypeError(
            "The color parameter must be of type tuple, "
            f"not {type(color).__name__}.")

    if not len(color) == 3:
        raise ValueError(
            f"The lenght of the color tuple must be 3, not {len(color)}")

    for pixel_value in color:
        if not 255 >= pixel_value >= 0:
            raise ValueError(
                "The values inside the color tuple must be greater than "
                "or equal to 0 but less than or equal to 255.")

    cv2.putText(
        img=img,
        text=text,
        org=text_place,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.7,
        color=color,
        thickness=2
    )
