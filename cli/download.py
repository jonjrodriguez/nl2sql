from ConfigParser import ConfigParser
import os
import re
import shutil
import sys
import zipfile
import requests


def download(path, force):
    config = ConfigParser()
    config.read(['config.example.cfg', 'config.cfg'])

    base_path = os.path.abspath(path)

    if not config.has_section('PATHS'):
        config.add_section('PATHS')

    config.set('PATHS', 'base', base_path)

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    if force:
        clear_directory(base_path)

    for _, url in config.items('DOWNLOADS'):
        download_file(url, base_path)

    extract_stanford_jars(base_path, config)
    extract_stanford_models(config)

    with open('config.cfg', 'wb') as config_file:
        config.write(config_file)


def extract_stanford_jars(base_path, config):
    file_name = os.path.basename(config.get('DOWNLOADS', 'corenlp'))
    file_path = os.path.join(base_path, file_name)
    extract_path = os.path.splitext(file_path)[0]

    if os.path.isdir(extract_path) and len(os.listdir(extract_path)) > 1:
        print "\n   File %s is already extracted.\n" % file_name
        return

    extracted = extract_zip(file_path, base_path,
                            r'.*/stanford-corenlp-(\d+)(\.(\d+))+(-models)?\.jar')

    config.set('PATHS', 'stanford_jar',
               "%(base)s/" + [path for path in extracted if path.find('models') < 0][0])

    config.set('PATHS', 'models_jar',
               "%(base)s/" + [path for path in extracted if path.find('models') > -1][0])


def extract_stanford_models(config):
    models_path = config.get('PATHS', 'models_jar')
    models_raw_jar = config.get('PATHS', 'models_jar', True)

    extract_path = os.path.splitext(models_path)[0]
    extract_raw_path = os.path.splitext(models_raw_jar)[0]

    if os.path.isdir(extract_path) and len(os.listdir(extract_path)) > 1:
        print "\n   Stanford models have already been extracted.\n"
        return

    extract_zip(models_path, extract_path)

    config.set('PATHS', 'stanford_models', "%s/edu/stanford/nlp/models" % extract_raw_path)


def download_file(url, base_path):
    file_name = os.path.basename(url)
    file_path = os.path.join(base_path, file_name)

    if os.path.isfile(file_path):
        print "\n   File %s is already downloaded.\n" % file_name
        return

    response = requests.get(url, stream=True)
    length = response.headers.get('content-length')

    if length is None or response.status_code == 404:
        print "\n   File %s doesn't exist.\n" % file_name
        return

    with open(file_path, "wb") as output:
        print "\n   Downloading %s from %s\n" % (file_name, url)
        downloaded = 0

        for chunk in response.iter_content(chunk_size=4096):
            if chunk:
                downloaded += len(chunk)
                output.write(chunk)
                done = 50 * downloaded / int(length)
                sys.stdout.write("\r    [%s%s]" % ('=' * done, ' ' * (50 - done)))
                sys.stdout.flush()

    print "\n"


def extract_zip(file_path, extract_path, pattern=None):
    extracted = []
    with zipfile.ZipFile(file_path) as zip_file:
        if pattern is None:
            print "\n   Extracting %s to %s" % (os.path.basename(file_path), extract_path)
            zip_file.extractall(extract_path)
        else:
            for info in zip_file.infolist():
                if re.match(pattern, info.filename):
                    extracted.append(info.filename)
                    print "\n   Extracting %s to %s" % (info.filename, extract_path)
                    zip_file.extract(info, extract_path)

    return extracted


def clear_directory(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)

        if os.path.isdir(file_path):
            shutil.rmtree(file_path)

        if os.path.isfile(file_path) and not file_name.startswith('.'):
            os.remove(file_path)
