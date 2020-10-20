import shutil
import subprocess
import gmail_connector
import os
import configparser
from time import time
from datetime import datetime

config_section = 'STORAGE'
params = configparser.ConfigParser()
params.read('parameters.ini')

image_path = params.get(config_section, 'path')
delete_delay_detection = params.getint(config_section, 'delay_detection')
delete_delay_no_detection = params.getint(config_section, 'delay_no_detection')


def get_disk_space():
    total, used, free = shutil.disk_usage(image_path)
    return str(free // (2**30)) + 'GB von ' + str(total // (2**30)) + 'GB'


def path_size(path):
    """disk usage in human readable format (e.g. '2,1GB')"""
    return subprocess.check_output(['du','-sh', path]).split()[0].decode('utf-8')


def image_count(path):
    count = 0
    new_path, directories, files = next(os.walk(path))
    count += len(files)
    for directory in directories:
        count += image_count(path + '/' + directory)
    return count


def delete_old_files(path, delay):
    new_path, directories, files = next(os.walk(path))
    for file in files:
        age = time() - float(os.path.getmtime(path + '/' + file))
        age = age/3600/24
        if file.endswith('.jpg') and age > delay:
            os.remove(path + '/' + file)
    for directory in directories:
        delete_old_files(path + '/' + directory, delay)


def latest_image(path):
    new_path, directories, files = next(os.walk(path))
    latest_time = 0
    latest_image_path = None
    for file in files:
        if file.endswith('.jpg') and float(os.path.getmtime(path + '/' + file)) > latest_time:
            latest_time = float(os.path.getmtime(path + '/' + file))
            latest_image_path = path + '/' + file
    for directory in directories:
        directory_latest_time, directory_latest_image_path = latest_image(path + '/' + directory)
        if directory_latest_time > latest_time:
            latest_time = directory_latest_time
            latest_image_path = directory_latest_image_path
    return latest_time, latest_image_path


def main():
    delete_old_files(image_path + 'detection/', delete_delay_detection)
    delete_old_files(image_path + 'no_detection/', delete_delay_no_detection)
    current = latest_image(image_path)
    last_image_timestamp = datetime.fromtimestamp(int(current[0])).strftime('%d.%m. %H:%M')
    content = 'Fahrstuhl Update: ' + get_disk_space() + ' frei bei ' + str(image_count(image_path))\
              + ' Bildern (letztes Bild um ' + last_image_timestamp + ')'
    gmail_connector.send_mail(content, current[1])


if __name__ == "__main__":
    main()
