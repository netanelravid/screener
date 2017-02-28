from screener.exceptions import DuplicateFile
from screener.settings import DONE_PRINT
from screener.utils.images import (
    save_as_jpg,
    IMAGE_EXT,
)

logger = None
LOGGER_NAME = __name__


def screenshot_single_target(browser, url, folder, filename):
    if not browser.get(url=url):
        return
    logger.info(u"Saving image for target {url}".format(url=url))
    print(u"Screenshoting {url}".format(url=url))
    try:
        save_as_jpg(
            image_date=browser.target_screenshot,
            folder=folder,
            filename=filename
        )
    except DuplicateFile:
        logger.warning(u"Image '{name}.{ext}' already exist".format(
            name=filename,
            ext=IMAGE_EXT,
        ))
        return

    # Printing success
    log_msg = u"Image '{name}' for url {url} saved successfully".format(
        name=filename,
        url=url
    )
    logger.info(log_msg)
    print(u'Saving {done}'.format(done=DONE_PRINT))
