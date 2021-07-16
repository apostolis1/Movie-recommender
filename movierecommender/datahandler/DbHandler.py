import json
import mysql.connector
import sqlalchemy as db
import pathlib
import os.path
from sqlalchemy import text


class DbHandler:
    """
    Using sqlalchemy to make the connection to the db compared to some other connector because
    of its compatibility with pandas pd.Dataframe.to_sql
    """
    def __init__(self):
        creds = self.load_creds()
        self.username = creds["username"]
        self.password = creds["password"]
        self.db = creds["db"]
        self.host = creds["host"]
        self.conn = None
        self.cur = None

    def load_creds(self):
        # make sure it works from every path, can be improved to not use so many parents probably
        file_dir = pathlib.Path(__file__).parent.parent.parent.resolve()
        with open(os.path.join(file_dir, "data/creds.json"), "r") as f:
            creds = json.load(f)
        return creds

    def connect(self):
        try:
            engine = db.create_engine(f'mysql+mysqlconnector://{self.username}:{self.password}@{self.host}/{self.db}')
        except mysql.connector.Error as e:
            print("Error while connecting to MySql", e)
            self.conn = None
            return
        self.conn = engine.connect()
        return

    def exec_select_sql_from_file(self, sql_file) -> list:
        self.connect()
        with open(sql_file, "r") as f:
            sql_string = f.read()
        # return self.conn.execute(text(sql_string))
        return [r for r in self.conn.execute(text(sql_string))]

    def exec_sql_cmd(self, sql_cmd) -> list:
        """
        Executes the command and returns the result, intended for select statements to query the db from flask
        :param sql_cmd: the cmd to execute
        :return: list, the results of the cmd
        """
        self.connect()
        return [r for r in self.conn.execute(text(sql_cmd))]
