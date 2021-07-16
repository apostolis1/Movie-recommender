import os.path
import requests
import gzip
import shutil
import pathlib


class TsvHandler:
    # A class to handle the download and extraction of .tsv files from https://datasets.imdbws.com/
    def __init__(self, url):
        # Example of download url: https://datasets.imdbws.com/title.basics.tsv.gz
        self.url = url
        data_dir = pathlib.Path(__file__).parent.parent.parent.resolve()
        self.download_location = os.path.join(data_dir, "data/temp")  # "../../data/temp"
        self.filename = self.url.split('/')[-1]
        self.download_full_path = os.path.join(self.download_location, self.filename)
        self.extract_filename = self.filename.replace(".gz", "")
        self.extract_fullpath = os.path.join(self.download_location, self.extract_filename)
        pass

    def create_temp_folder(self):
        if not os.path.isdir(self.download_location):
            os.mkdir(self.download_location)

    def download(self):
        self.create_temp_folder()
        print(f"Downloading {self.filename} from {self.url} ...")
        r = requests.get(self.url)
        with open(self.download_full_path, 'wb') as f:
            f.write(r.content)
        return

    def extract(self):
        with gzip.open(self.download_full_path, 'rb') as f_in:
            with open(self.extract_fullpath, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f"Successfully extracted {self.extract_filename}")
        return

    def delete_csv(self):
        os.remove(self.extract_fullpath)
        os.remove(self.download_full_path)
