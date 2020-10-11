import cv2
import logging
import time
from datetime import datetime
from pathlib import Path
import detector
import ip


def configure_logger():
    logger = logging.getLogger('standard_logger')
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


def resize_image(img, scaling):
    width = int(img.shape[1] * scaling)
    height = int(img.shape[0] * scaling)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


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
            path = hierarchical_file(datetime.now())
            if detector.detect_faces(img) or detector.detect_people(img):
                log.info('Detected people')
                cv2.imwrite(path, img)
            else:
                cv2.imwrite(path, resize_image(img, 0.5))
        else:
            log.error('No image captured')


log = configure_logger()
log.info(ip.ip())
log.info('Started camera_capturer')
take_images()

log.info('End camera-capturer')
