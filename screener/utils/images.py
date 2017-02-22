from os.path import (
    join as path_join,
    isfile
)

from PIL import Image
from six import StringIO

from screener.settings import (
    SCREENSHOT_WIDTH,
    SCREENSHOT_HEIGHT,
    init_logger)
from screener.utils.decorators import validate_path

WINDOW_BOX = (0, 0, SCREENSHOT_WIDTH, SCREENSHOT_HEIGHT)
IMAGE_EXT = 'jpg'
IMAGE_TYPE = 'JPEG'
IMAGE_QUALITY = 95

logger = init_logger(__name__)


@validate_path
def save_as_jpg(image_date, folder, filename):
    new_filename = '{fname}.{ext}'.format(fname=filename, ext=IMAGE_EXT)
    file_path = path_join(folder, new_filename)
    if isfile(file_path):
        raise IOError('File already exist')
    image = Image.open(StringIO(image_date))
    logger.debug('Cropping and saving image')
    cropped_image = image.crop(WINDOW_BOX)
    cropped_image.save(
        file_path,
        IMAGE_TYPE,
        optimize=True,
        quality=IMAGE_QUALITY
    )
