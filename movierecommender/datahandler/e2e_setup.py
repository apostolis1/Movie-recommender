from TsvHandler import TsvHandler
from DataExtractors import TitleBasicsExtractor, TitleNameExtractor, NameBasicsExtractor, TitleRatingsExtractor, SoupCreator
from WebScraper import ParallelScraper


def download_insert_title_basics(download=True, delete=True):
    """
    Download data from https://datasets.imdbws.com/title.basics.tsv.gz and insert them on the title_basics table
    :param download: bool, specifies if we want to download the file again or we already have it downloaded
    :param delete: bool, specifies if we want to delete the files after extraction
    :return: None
    """
    if download:
        my_tsv = TsvHandler("https://datasets.imdbws.com/title.basics.tsv.gz")
        my_tsv.download()
        my_tsv.extract()
    extractor = TitleBasicsExtractor("../../data/temp/title.basics.tsv")
    extractor.filter_and_insert()
    if delete:
        my_tsv = TsvHandler("https://datasets.imdbws.com/title.basics.tsv.gz")
        my_tsv.delete_csv()
    return


def download_insert_title_principals(download=True, delete=True):
    """
    Download data from https://datasets.imdbws.com/title.principals.tsv.gz and insert them on the title_basics table
    :param download: bool, specifies if we want to download the file again or we already have it downloaded
    :param delete: bool, specifies if we want to delete the files after extraction
    :return: None
    """
    if download:
        my_tsv = TsvHandler("https://datasets.imdbws.com/title.principals.tsv.gz")
        my_tsv.download()
        my_tsv.extract()
    extractor = TitleNameExtractor("../../data/temp/title.principals.tsv")
    extractor.get_reader()
    for chunk in extractor.reader:
        extractor.df = chunk
        extractor.filter_and_insert()
    if delete:
        my_tsv = TsvHandler("https://datasets.imdbws.com/title.principals.tsv.gz")
        my_tsv.delete_csv()
    return


def download_insert_name_basics(download=True, delete=True):
    """
    Download data from https://datasets.imdbws.com/name.basics.tsv.gz and insert them on the title_basics table
    :param download: bool, specifies if we want to download the file again or we already have it downloaded
    :param delete: bool, specifies if we want to delete the files after extraction
    :return: None
    """
    if download:
        my_tsv = TsvHandler("https://datasets.imdbws.com/name.basics.tsv.gz")
        my_tsv.download()
        my_tsv.extract()
    extractor = NameBasicsExtractor("../../data/temp/name.basics.tsv")
    extractor.get_reader()
    for chunk in extractor.reader:
        extractor.df = chunk
        extractor.filter_and_insert()
    if delete:
        my_tsv = TsvHandler("https://datasets.imdbws.com/name.basics.tsv.gz")
        my_tsv.delete_csv()
    return


def download_insert_title_ratings(download=True, delete=True):
    """
    Download data from https://datasets.imdbws.com/title.ratings.tsv.gz and insert them on the title_basics table
    :param download: bool, specifies if we want to download the file again or we already have it downloaded
    :param delete: bool, specifies if we want to delete the files after extraction
    :return: None
    """
    if download:
        my_tsv = TsvHandler("https://datasets.imdbws.com/title.ratings.tsv.gz")
        my_tsv.download()
        my_tsv.extract()
    extractor = TitleRatingsExtractor("../../data/temp/title.ratings.tsv")
    extractor.get_reader()
    for chunk in extractor.reader:
        extractor.df = chunk
        extractor.filter_and_insert()
    if delete:
        my_tsv = TsvHandler("https://datasets.imdbws.com/title.ratings.tsv.gz")
        my_tsv.delete_csv()
    return


def scrap_keywords():
    """
    Function used to scrap the keywords from IMDB, just a call to the create_and_run_threads of the ParallelScraper
    :return: None
    """
    ParScr = ParallelScraper()
    ParScr.create_and_run_threads()
    return


def create_and_insert_soup():
    """
    Function used to create the soup from the different tables on the db
    :return: None
    """
    SC = SoupCreator()
    SC.group_actors()
    SC.insert_to_db()
    return


def main():
    """
    E2E function that handles the whole process of extracting the relevant data and inserting them in the db
    The order of the functions must not change to avoid accessing a table because it is populated
    Functions can be ignored if we only want specific updates to be done without messing with other tables
    :return: None
    """
    download_insert_title_basics()
    download_insert_title_principals()
    download_insert_name_basics()
    download_insert_title_ratings()
    scrap_keywords()
    create_and_insert_soup()
    return


if __name__ == '__main__':
    main()
