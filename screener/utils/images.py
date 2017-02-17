from os.path import join as path_join

from PIL import Image
from six import StringIO

from screener.settings import (
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT
)

WINDOW_BOX = (0, 0, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT)
IMAGE_EXT = 'jpg'
IMAGE_TYPE = 'JPEG'
IMAGE_QUALITY = 95


def save_as_jpg(image_date, folder, filename):
    image = Image.open(StringIO(image_date))
    cropped_image = image.crop(WINDOW_BOX)
    new_filename = '{fname}.{ext}'.format(fname=filename, ext=IMAGE_EXT)
    file_path = path_join(folder, new_filename)
    cropped_image.save(file_path, IMAGE_TYPE, optimize=True,
                       quality=IMAGE_QUALITY)
