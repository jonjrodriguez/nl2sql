import os
import shutil
import sys
import zipfile
import requests
from Config import Config

class Download(object):
    """
    Downloads and extracts the required files
    """
    def __init__(self, communicator, path):
        self.config = Config()
        self.comm = communicator
        self.path = os.path.abspath(path)

        self.config.set('PATHS', 'base', self.path)


    def run(self, force):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        if force:
            self.clear_directory()

        self.download_all()

        # extract stanford models
        file_path = self.config.get('PATHS', 'stanford_models_jar')
        folder_name = os.path.splitext(os.path.basename(file_path))[0]
        self.extract_zip(file_path, folder_name)

        self.config.write()


    def download_all(self):
        for _, url in self.config.items('DOWNLOADS'):
            file_path = self.download_file(url)
            if file_path.endswith('.zip'):
                self.extract_zip(file_path)


    def download_file(self, url):
        file_name = os.path.basename(url)
        file_path = os.path.join(self.path, file_name)

        if os.path.isfile(file_path):
            self.comm.say("File %s is already downloaded." % file_name)
            return file_path

        response = requests.get(url, stream=True)
        length = response.headers.get('content-length')

        if length is None or response.status_code == 404:
            self.comm.say("File %s doesn't exist." % file_name)
            return ""

        with open(file_path, "wb") as output:
            self.comm.say("Downloading %s from %s" % (file_name, url))
            downloaded = 0

            for chunk in response.iter_content(chunk_size=4096):
                if chunk:
                    downloaded += len(chunk)
                    output.write(chunk)
                    done = 50 * downloaded / int(length)
                    sys.stdout.write("\r    [%s%s]" % ('=' * done, ' ' * (50 - done)))
                    sys.stdout.flush()

        return file_path


    def clear_directory(self):
        for file_name in os.listdir(self.path):
            file_path = os.path.join(self.path, file_name)

            if os.path.isdir(file_path):
                shutil.rmtree(file_path)

            if os.path.isfile(file_path) and not file_name.startswith('.'):
                os.remove(file_path)


    def extract_zip(self, file_path, extract_folder=None):
        file_name = os.path.basename(file_path)
        path = os.path.dirname(file_path)

        if extract_folder:
            path = "%s/%s" % (path, extract_folder)

        extract_path = os.path.splitext(file_path)[0]

        if os.path.isdir(extract_path) and len(os.listdir(extract_path)) > 1:
            self.comm.say("File %s is already extracted." % file_name)
            return

        with zipfile.ZipFile(file_path) as zip_file:
            self.comm.say("Extracting %s to %s" % (file_name, path))
            zip_file.extractall(path)
