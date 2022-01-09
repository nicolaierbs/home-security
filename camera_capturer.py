import cv2
import logging
from logging.handlers import RotatingFileHandler
import time
from datetime import datetime
from pathlib import Path
import detector
import configparser
import sys
import random

params = configparser.ConfigParser()
params.read('parameters.ini')

image_path = params.get('STORAGE', 'path')
no_people_scale_factor = params.getfloat('IMAGES', 'no_people_scale_factor')
people_scale_factor = params.getfloat('IMAGES', 'people_scale_factor')
sleep_time = params.getint('IMAGES', 'sleep')


def configure_logger():
    logger = logging.getLogger('standard_logger')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = RotatingFileHandler('debug.log', maxBytes=1024*1024, backupCount=5)
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


def hierarchical_file(date, detection=False):
    if detection:
        path = image_path + 'detection/' + date.strftime("%Y/%m/%d/%H/")
    else:
        path = image_path + 'no_detection/' + date.strftime("%Y/%m/%d/%H/")
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
        time.sleep(sleep_time)
        if captured:
            log.debug('Image captured')
            if detector.detect_faces(img) or detector.detect_people(img):
                log.info('Detected people')
                cv2.imwrite(hierarchical_file(datetime.now(), detection=True), resize_image(img, people_scale_factor))
            elif random.random() > 0.5:
                cv2.imwrite(hierarchical_file(datetime.now(), detection=False), resize_image(img, no_people_scale_factor))
        else:
            log.error('No image captured')
            sys.exit(1)


log = configure_logger()
log.info('Started camera_capturer')
take_images()
log.info('End camera-capturer')
