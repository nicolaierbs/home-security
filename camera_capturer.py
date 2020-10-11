import cv2
import logging
import time
from datetime import datetime
from pathlib import Path


def configure_logger():
    logger = logging.getLogger('simple_logger')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def hierarchical_file(date):
    path = 'images/' + date.strftime("%Y/%m/%d/%H/%M/")
    Path(path).mkdir(parents=True, exist_ok=True)
    return path + str(int(date.timestamp())) + '.jpg'


def take_images():
    # initialize the camera
    cam = cv2.VideoCapture(0)   # 0 -> index of camera
    log.info('Initialized camera capturing')
    captured = True
    while captured:
        captured, img = cam.read()
        time.sleep(1)
        if captured:
            log.debug('Image captured')
            # cv2.namedWindow("cam-test", cv2.WINDOW_AUTOSIZE)
            # cv2.imshow("cam-test", img)
            # cv2.waitKey(0)
            # cv2.destroyWindow("cam-test")

            path = hierarchical_file(datetime.now())
            log.info(path)
            # save image
            cv2.imwrite(path, img)
        else:
            log.error('No image captured')


log = configure_logger()
log.info('Started camera_capturer')
take_images()

log.info('End camera-capturer')
