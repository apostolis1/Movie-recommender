import unittest
from movierecommender.datahandler.DbHandler import DbHandler
from sqlalchemy import text
import pathlib
import os


file_dir = pathlib.Path(__file__).parent.parent.resolve()
DATA_PATH = os.path.join(file_dir, "data/")


class TestDBHandler(unittest.TestCase):
    def test_handler_init(self):
        handler = DbHandler()
        assert handler.host is not None and handler.password is not None and handler.username is not None \
            and handler.db is not None

    def test_handler_connection(self):
        handler = DbHandler()
        handler.connect()
        assert handler.conn is not None

    def test_execute_query(self):
        """
        Run a sample query to make sure the connection is indeed correct and the schema is created
        :return:
        """
        handler = DbHandler()
        handler.connect()
        try:
            handler.conn.execute(text("SELECT table_name FROM information_schema.tables \
            WHERE table_schema = 'movie_recommender';"))
        except Exception as e:
            assert False, e

    def test_execute_select_from_sql(self):
        handler = DbHandler()
        handler.connect()
        try:
            results = handler.exec_select_sql_from_file(os.path.join(DATA_PATH, "sql/select_actors.sql"))
            print([r['tconst'] for r in results][:2])
        except Exception as e:
            assert False, e
        return


if __name__ == '__main__':
    unittest.main()
