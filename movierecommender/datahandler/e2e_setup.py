from TsvHandler import TsvHandler
from DataExtractors import TitleBasicsExtractor, TitleNameExtractor, NameBasicsExtractor, TitleRatingsExtractor, SoupCreator
from WebScraper import ParallelScraper


def download_insert_title_basics(download=True, delete=True):
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
    ParScr = ParallelScraper()
    ParScr.create_and_run_threads()


def create_and_insert_soup():
    SC = SoupCreator()
    SC.group_actors()
    SC.insert_to_db()


def main():
    download_insert_title_basics()
    download_insert_title_principals()
    download_insert_name_basics()
    download_insert_title_ratings()
    scrap_keywords()
    create_and_insert_soup()


if __name__ == '__main__':
    main()
