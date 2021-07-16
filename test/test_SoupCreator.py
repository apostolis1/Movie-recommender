import unittest
from movierecommender.datahandler.DataExtractors import SoupCreator


class TestSoupCreator(unittest.TestCase):
    def test_SoupCreator_init(self):
        SC = SoupCreator()
        return

    def test_soup_creation(self):
        SC = SoupCreator()
        SC.keywords_df = SC.keywords_df[:10]  # Keep only a small portion for test performance
        SC.group_actors()
        soup_df = SC.get_soup_df()
        keywords_df = SC.get_keywords_df()
        tconst = soup_df.iloc[0]["tconst"] # Grab first record from soup_df and compare with keywords_df for same tconst
        print(f"Using sample tconst: {tconst}")
        rec_keywords = keywords_df.loc[keywords_df['tconst'] == tconst, "keywords"][0]
        rec_soup = soup_df.loc[soup_df["tconst"] == tconst, "soup"][0]
        print(rec_keywords)
        print(rec_soup)
        assert rec_keywords in rec_soup


if __name__ == '__main__':
    unittest.main()
