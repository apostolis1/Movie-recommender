import random
import unittest
import pandas as pd
from movierecommender.recommender.Recommender import Recommender, get_titles_from_tconst_list
import pathlib
import os
from movierecommender.datahandler.DbHandler import DbHandler
from sqlalchemy import text


file_dir = pathlib.Path(__file__).parent.parent.resolve()
DATA_PATH = os.path.join(file_dir, "data/")


class TestRecommender(unittest.TestCase):
    def test_recommender_init(self):
        try:
            rec = Recommender()
        except Exception as e:
            assert False, e

    def test_get_recommendation_with_create_count_vecctorizer(self):
        rec = Recommender()
        rec.create_cosine_sim()
        sample_tconst = random.choice(list(rec.cosine_sim.tconst.values))  # grab a random movie to test
        print(f"Running test_get_recommendation for tconst: {sample_tconst}")
        sample_recommendations = rec.get_recommendation_from_tconst(sample_tconst)
        assert sample_recommendations[0] == sample_tconst  # the best fit should be the movie itself

    def test_get_recommendation_with_import(self):
        rec = Recommender()
        rec.import_cosine_sim_from_pkl()
        sample_tconst = random.choice(list(rec.cosine_sim.tconst.values))  # grab a random movie to test
        print(f"Running test_get_recommendation for tconst: {sample_tconst}")
        sample_recommendations = rec.get_recommendation_from_tconst(sample_tconst)
        assert sample_recommendations[0] == sample_tconst  # the best fit should be the movie itself

    def test_cosine_sim_export(self):
        """
        Test that export functionality after create_count_vectorizer() method is called works
        :return:
        """
        temp_test_path = os.path.join(DATA_PATH, 'cosine_sim/test_file.pkl')
        rec = Recommender()
        rec.create_cosine_sim()  # Initialize self.cosine_sim
        rec.export_cosine_sim_to_pkl(temp_test_path)
        assert os.path.exists(temp_test_path)
        os.remove(temp_test_path)  # Remove test temp file
        return

    def test_cosine_sim_import(self):
        """
        Test that the import correctly initializes the self.cosine_sim dataframe
        :return:
        """
        rec = Recommender()
        rec.import_cosine_sim_from_pkl()
        print(rec.cosine_sim.head())
        assert type(rec.cosine_sim) == pd.DataFrame

    def test_cosine_sim_import_error(self):
        """
        Test that correct Exception is thrown in case of wrong filepath import
        :return:
        """
        rec = Recommender()
        wrong_path = os.path.join(DATA_PATH, 'cosine_sim/wrong_file.pkl')
        try:
            rec.import_cosine_sim_from_pkl(pkl_path=wrong_path)
            assert False
        except FileNotFoundError:
            assert True

    def test_cosine_sim_import_auto_create(self):
        """
        Test that if auto_create is set then the file is successfully created
        :return:
        """
        rec = Recommender()
        wrong_path = os.path.join(DATA_PATH, 'cosine_sim/wrong_file_auto_create.pkl')
        rec.import_cosine_sim_from_pkl(pkl_path=wrong_path, auto_create=True)
        assert os.path.exists(wrong_path)
        os.remove(wrong_path)

    def test_get_titles_from_tconst(self):
        """
        Test the get_titles_from_tconst_list function
        Grab the recommendation titles for a random movie and crosscheck with the titles in the title_basics table
        :return:
        """
        rec = Recommender()
        rec.import_cosine_sim_from_pkl()
        sample_tconst = random.choice(list(rec.cosine_sim.tconst.values))  # grab a random movie to test
        sample_recommendations_tconst = rec.get_recommendation_from_tconst(sample_tconst)
        sample_titles = get_titles_from_tconst_list(sample_recommendations_tconst)
        recommendation_titles = [result[1] for result in sample_titles]
        # Make sure the titles returned are a subset of the titles in title_basics table
        dbhandler = DbHandler()
        dbhandler.connect()
        # Use a join to limit the results only on those that interest us
        all_titles = dbhandler.conn.execute(text(
            "SELECT tconst,primaryTitle from title_basics NATURAL JOIN title_keywords"))
        # Convert the result of the query to a df
        all_titles_df = pd.DataFrame(data=[row for row in all_titles], columns=['tconst','primaryTitle'])
        # Find the titles that exist in both the df from the db and the results from the recommender
        same_titles = all_titles_df.loc[all_titles_df['tconst'].isin(sample_recommendations_tconst)]['primaryTitle']
        # Make sure we found all the movie titles
        assert len(recommendation_titles) == same_titles.size

    def test_recommendation_limit_works(self):
        """
        Test that the limit param in get_recommendation_from_tconst works as intended
        :return:
        """
        limit = random.randint(1, 50)
        print(f"Testing for limit: {limit}")
        rec = Recommender()
        rec.import_cosine_sim_from_pkl()
        sample_tconst = random.choice(list(rec.cosine_sim.tconst.values))  # grab a random movie to test
        sample_recommendations_tconst = rec.get_recommendation_from_tconst(sample_tconst, limit=limit)
        assert len(sample_recommendations_tconst) == limit

    def test_wrong_tconst_str(self):
        """
        Test that if a wrong tconst value is provided in the get_recommendation_from_tconst method
        an Exception is raised
        :return:
        """
        rec = Recommender()
        rec.import_cosine_sim_from_pkl()
        try:
            rec.get_recommendation_from_tconst('wrong_tconst')
        # If Exception is raised then True
        except Exception as e:
            print(e)
            assert True
            return
        assert False, "Exception not thrown for wrong tconst"
