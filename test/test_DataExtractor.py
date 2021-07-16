import unittest
import os.path
from movierecommender.datahandler import DataExtractors as DE
from movierecommender.datahandler.TsvHandler import TsvHandler
import pathlib

unittest.TestLoader.sortTestMethodsUsing = None
file_dir = pathlib.Path(__file__).parent.parent.resolve()
TEMP_PATH = os.path.join(file_dir, "data/temp/")


class TestDataExtractor(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        This can either be done in integration testing, or make sure we already have the file
        by making sure the tests run in order, meaning test_tsv_download runs first
        If we want to keep them as unit tests they should be able to run autonomously, meaning
        they check if the file exists and if not they download it
        """
        if not os.path.exists(os.path.join(TEMP_PATH, "title.basics.tsv")):
            my_tsv = TsvHandler("https://datasets.imdbws.com/title.basics.tsv.gz")
            my_tsv.download()
            my_tsv.extract()
        unittest.TestCase.setUpClass()
        return

    def test_tsv_download(self):
        my_tsv = TsvHandler("https://datasets.imdbws.com/title.basics.tsv.gz")
        my_tsv.download()
        my_tsv.extract()
        assert os.path.exists(os.path.join(TEMP_PATH, "title.basics.tsv"))

    def test_handler_read(self):
        read_file = "title.basics.tsv"
        read_location = os.path.join(TEMP_PATH, read_file)
        handler = DE.BaseExtractor(read_location)
        try:
            handler.read_tsv()
        except OSError as e:
            assert False, f"Can't read file, {e}"
        return

    def test_handler_filter(self):
        read_file = "title.basics.tsv"
        read_location = os.path.join(TEMP_PATH, read_file)
        handler = DE.BaseExtractor(read_location)
        handler.read_tsv()
        handler.filter_nan_from_tsv()
        assert not (r'\N' in handler.df.values), f"Replacement with \\N didn't work"

    def test_title_basics_filter_movies(self):
        read_file = "title.basics.tsv"
        read_location = os.path.join(TEMP_PATH, read_file)
        handler = DE.TitleBasicsExtractor(read_location)
        handler.read_tsv()
        handler.filter_movies_from_df()
        titleTypes = set(handler.filtered_df['titleType'])
        print(titleTypes)
        assert len(titleTypes) == 1 and 'movie' in titleTypes, f"Filtering movies from titleType didn't work"

    def test_tsv_deletion(self):
        my_tsv = TsvHandler("https://datasets.imdbws.com/title.basics.tsv.gz")
        my_tsv.delete_csv()
        assert not os.path.exists(os.path.join(TEMP_PATH, "title.basics.tsv"))

    @classmethod
    def tearDownClass(cls) -> None:
        if os.path.exists(os.path.join(TEMP_PATH, "title.basics.tsv")):
            my_tsv = TsvHandler("https://datasets.imdbws.com/title.basics.tsv.gz")
            my_tsv.delete_csv()
        unittest.TestCase.tearDownClass()


if __name__ == '__main__':
    unittest.main()
