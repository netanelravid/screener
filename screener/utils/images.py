from os.path import join as path_join

from PIL import Image
from six import StringIO

from screener.settings import (
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT,
)
from screener.utils.decorators import validate_path

WINDOW_BOX = (0, 0, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT)
IMAGE_EXT = 'jpg'
IMAGE_TYPE = 'JPEG'
IMAGE_QUALITY = 95

logger = None
LOGGER_NAME = __name__


@validate_path(ext=IMAGE_EXT)
def save_as_jpg(image_date, folder, filename):
    new_filename = '{fname}.{ext}'.format(fname=filename, ext=IMAGE_EXT)
    file_path = path_join(folder, new_filename)
    image = Image.open(StringIO(image_date))
    logger.debug('Cropping and saving image')
    cropped_image = image.crop(WINDOW_BOX)
    cropped_image.save(
        file_path,
        IMAGE_TYPE,
        optimize=True,
        quality=IMAGE_QUALITY
    )
