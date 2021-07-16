import pandas as pd
import numpy as np
from movierecommender.datahandler.DbHandler import DbHandler
from sqlalchemy import text
import pathlib
import os


root_dir = pathlib.Path(__file__).parent.parent.parent.resolve()
DATA_PATH = os.path.join(root_dir, "data/")


class BaseExtractor:
    def __init__(self, tsv_file=None):
        self.tsv_file = tsv_file
        self.df = None
        self.reader = None

    def read_tsv(self):
        self.df = pd.read_csv(self.tsv_file, sep='\t', header=0)
        return

    def get_reader(self):
        chunksize = 10 ** 6
        self.reader = pd.read_csv(self.tsv_file, sep='\t', header=0, chunksize=chunksize)
        return

    def filter_nan_from_tsv(self):
        self.df.replace(r'\N', np.nan, inplace=True)
        return


class TitleBasicsExtractor(BaseExtractor):
    def __init__(self, tsv_file=None):
        super(TitleBasicsExtractor, self).__init__(tsv_file=tsv_file)
        self.filtered_df = None
        return

    def filter_movies_from_df(self):
        is_movie = self.df["titleType"] == "movie"
        self.filtered_df = self.df[is_movie]
        return

    def filter_columns(self):
        """tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres"""
        columns_to_keep = ['tconst', 'primaryTitle', 'startYear', 'genres']
        self.filtered_df = self.filtered_df[columns_to_keep]
        return

    def insert_to_db(self):
        myDbHandler = DbHandler()
        myDbHandler.connect()
        self.filtered_df.to_sql("title_basics", myDbHandler.conn, if_exists='append', index=False)
        return

    def filter_and_insert(self):
        """
        E2E function that handles everything from reading the tsv to inserting in the db after filtering
        :return:
        """
        self.read_tsv()
        self.filter_nan_from_tsv()
        print("Successfully replaced Nan")
        self.filter_movies_from_df()
        print("Successfully filtered movies")
        self.filter_columns()
        print("Successfully filtered columns")
        self.insert_to_db()
        print("Successfully inserted to db")
        return


class TitleNameExtractor(BaseExtractor):
    def __init__(self, tsv_file=None):
        super(TitleNameExtractor, self).__init__(tsv_file=tsv_file)
        self.filtered_df = None
        return

    def filter_columns(self):
        """tconst	ordering	nconst	category	job	characters"""
        columns_to_keep = ['tconst', 'nconst']
        self.filtered_df = self.df[columns_to_keep]
        del self.df
        return

    def filter_foreign_keys(self):
        myDbHandler = DbHandler()
        myDbHandler.connect()
        tconst_ids = [row["tconst"] for row in myDbHandler.conn.execute(text("SELECT tconst FROM title_basics"))]
        self.filtered_df = self.filtered_df[self.filtered_df.tconst.isin(tconst_ids)]
        self.filtered_df = self.filtered_df.groupby(['tconst', 'nconst']).size().reset_index()
        columns_to_keep = ['tconst', 'nconst']
        self.filtered_df = self.filtered_df[columns_to_keep]
        return

    def insert_to_db(self):
        myDbHandler = DbHandler()
        myDbHandler.connect()
        self.filtered_df.to_sql("title_principals", myDbHandler.conn, if_exists='append', index=False)
        return

    def filter_and_insert(self):
        """
        E2E function that handles everything from reading the tsv to inserting in the db after filtering
        We don't use self.read_tsv() here, we use the reader to break the file in chunks
        :return:
        """
        self.filter_nan_from_tsv()
        print("Successfully replaced Nan")
        self.filter_columns()
        print("Successfully filtered columns")
        self.filter_foreign_keys()
        print("Successfully filtered foreign key constraints")
        self.insert_to_db()
        print("Successfully inserted to db")
        return


class NameBasicsExtractor(BaseExtractor):
    def __init__(self, tsv_file=None):
        super(NameBasicsExtractor, self).__init__(tsv_file=tsv_file)
        self.filtered_df = None
        return

    def filter_columns(self):
        """tconst	ordering	nconst	category	job	characters"""
        columns_to_keep = ['nconst', 'primaryName']
        self.filtered_df = self.df[columns_to_keep]
        del self.df
        return

    def filter_foreign_keys(self):
        myDbHandler = DbHandler()
        myDbHandler.connect()
        nconst_ids = [row["nconst"] for row in myDbHandler.conn.execute(text("SELECT DISTINCT nconst \ "
                                                                             "FROM title_principals"))]
        self.filtered_df = self.filtered_df[self.filtered_df.nconst.isin(nconst_ids)]
        return

    def insert_to_db(self):
        myDbHandler = DbHandler()
        myDbHandler.connect()
        self.filtered_df.to_sql("name_basics", myDbHandler.conn, if_exists='append', index=False)
        return

    def filter_and_insert(self):
        """
        E2E function that handles everything from reading the tsv to inserting in the db after filtering
        We don't use self.read_tsv() here, we use the reader to break the file in chunks
        :return:
        """

        self.filter_nan_from_tsv()
        print("Successfully replaced Nan")
        self.filter_columns()
        print("Successfully filtered columns")
        self.filter_foreign_keys()
        print("Successfully filtered foreign key constraints")
        self.insert_to_db()
        print("Successfully inserted to db")
        return


class TitleRatingsExtractor(BaseExtractor):
    def __init__(self, tsv_file=None):
        super(TitleRatingsExtractor, self).__init__(tsv_file=tsv_file)
        self.filtered_df = None
        return

    def filter_columns(self):
        """
        tconst	averageRating	numVotes
        we need everything for ratings
        :return:
        """
        self.filtered_df = self.df
        del self.df
        return

    def filter_foreign_keys(self):
        """
        Keep only the tconst ids that are in the title_basics table
        :return:
        """
        myDbHandler = DbHandler()
        myDbHandler.connect()
        tconst_ids = [row["tconst"] for row in myDbHandler.conn.execute(text("SELECT tconst FROM title_basics"))]
        self.filtered_df = self.filtered_df[self.filtered_df.tconst.isin(tconst_ids)]
        return

    def insert_to_db(self):
        """
        Insert the filtered_df in the db, tablename: title_ratings
        :return:
        """
        myDbHandler = DbHandler()
        myDbHandler.connect()
        self.filtered_df.to_sql("title_ratings", myDbHandler.conn, if_exists='append', index=False)
        return

    def filter_and_insert(self):
        """
        E2E function that handles everything from reading the tsv to inserting in the db after filtering
        We don't use self.read_tsv() here, we use the reader to break the file in chunks
        :return:
        """
        self.filter_nan_from_tsv()
        print("Successfully replaced Nan")
        self.filter_columns()
        print("Successfully filtered columns")
        self.filter_foreign_keys()
        print("Successfully filtered foreign key constraints")
        self.insert_to_db()
        print("Successfully inserted to db")
        return


class SoupCreator:
    def __init__(self):
        myDbHandler = DbHandler()
        keywords_list = myDbHandler.exec_select_sql_from_file(os.path.join(DATA_PATH, 'sql/select_genres_keywords.sql'))
        self.keywords_df = pd.DataFrame(keywords_list, columns=['tconst', 'genres', 'keywords'])
        print(self.keywords_df.head())
        actors_list = myDbHandler.exec_select_sql_from_file(os.path.join(DATA_PATH, 'sql/select_actors.sql'))
        self.actors_df = pd.DataFrame(actors_list, columns=['tconst', 'PrimaryName'])
        print(self.actors_df.head())
        self.soup_df = pd.DataFrame(columns=['tconst', 'soup'])

    def group_actors(self):
        soup_list = []
        for index, row in self.keywords_df.iterrows():
            tconst = row["tconst"]
            actors_tconst_df = self.actors_df.loc[self.actors_df['tconst'] == tconst]
            actors_soup = ','.join(actors_tconst_df.PrimaryName)
            final_soup = ",".join([row["genres"], actors_soup, row["keywords"]])
            # print(final_soup)
            soup_list.append((tconst, final_soup))
        self.soup_df = pd.DataFrame(data=soup_list, columns=['tconst', 'soup'])
        print(self.soup_df.head())
        return

    def get_keywords_df(self) -> pd.DataFrame:
        return self.keywords_df

    def get_soup_df(self) -> pd.DataFrame:
        return self.soup_df

    def insert_to_db(self) -> None:
        """
        Assuming the group_actors function is already called and the self.soup_df df is created, insert it
        in the title_soup table
        :return:
        """
        myDbHandler = DbHandler()
        myDbHandler.connect()
        self.soup_df.to_sql("title_soup", myDbHandler.conn, if_exists='append', index=False)
        print("Successfully inserted values in the db")
        return
