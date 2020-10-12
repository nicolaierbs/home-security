import shutil
import subprocess
import twilio_connector
import os
import ip
import configparser

config_section = 'IMAGES'
params = configparser.ConfigParser()
params.read('parameters.ini')

image_path = params.get(config_section, 'path')


def get_disk_space():
    total, used, free = shutil.disk_usage(image_path)
    return str(free // (2**30)) + 'GB/' + str(total // (2**30)) + 'GB'


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


def main():
    twilio_connector.send_whatsapp(
        'Your ' + ip.ip() + ' order of ' + get_disk_space()
        + ' has shipped and should be delivered on '
        + str(image_count(image_path)) + '. Details: ' + path_size(image_path))


if __name__ == "__main__":
    main()
