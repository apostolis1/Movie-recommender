import requests
from bs4 import BeautifulSoup as Bs
import threading
from queue import Queue
from movierecommender.datahandler.DbHandler import DbHandler
from sqlalchemy import text
import time
import pandas as pd


def get_tconst_ids():
    """
    A way of limiting the tconst ids we will scrap from imdb
    This is useful as we don't want to make too many queries, as it will overload the site and we will
    have to wait quite a bit of time to get results due to imdb 's rate limiting
    By modifying this function we can use different ways to filter the movies we are interested in
    Note that this function can simply return all the tconst ids we have in our DB with
        tconst_ids = [row["tconst"] for row in myDbHandler.conn.execute(text("SELECT tconst FROM title_basics"))]
    but this will not be optimal for the reasons stated above
    """
    myDbHandler = DbHandler()
    myDbHandler.connect()
    tconst_ids = [row["tconst"] for row in myDbHandler.conn.execute(text("SELECT * FROM movie_recommender.title_ratings\
     order by numVotes DESC, averageRating ;"))]
    # We keep only top 5% of the most popular movies (ordering by their amount of ratings)
    movies_to_keep = int(len(tconst_ids)*0.05)
    print(f"We will keep only {movies_to_keep} movies")
    return tconst_ids[:movies_to_keep]


class KeywordScrapper(threading.Thread):
    def __init__(self, q: Queue, results: Queue):
        threading.Thread.__init__(self)
        self.q = q
        self.results = results

    def run(self) -> None:
        while not self.q.empty():
            tconst = self.q.get()
            keywords_str = self.get_keywords_from_tconst(tconst)
            # print(tconst, keywords_str)
            if keywords_str:  # Don't put empty strings
                self.results.put((tconst, keywords_str))
            self.q.task_done()
        return

    def get_keywords_from_tconst(self, tconst: str) -> str:
        imdb_url = f"https://www.imdb.com/title/{tconst}/keywords/"
        max_tries = 5
        tries = 0
        while tries < max_tries:
            res = requests.get(imdb_url)
            if res.status_code != 200:
                print(f"Waiting try {tries}...")
                time.sleep(60*2)
                tries += 1
            else:
                print(f"Unblocking after try {tries}")
                break
        if tries == max_tries:  # Reached max tries
            return ''
        soup = Bs(res.text, 'html.parser')
        table_tags = soup.find_all('td', {"class": "soda sodavote"})
        keywords_str = ','.join([i["data-item-keyword"].strip() for i in table_tags])
        return keywords_str

    def insert_keywords_to_db(self):
        pass


class ParallelScraper:
    def __init__(self):
        self.queue_of_ids = Queue()
        for tconst_id in get_tconst_ids():
            self.queue_of_ids.put(tconst_id)
        self.results_queue = Queue()
        self.concurrent = 100

    def insert_results_to_db(self):
        results_list = list()
        while not self.results_queue.empty():
            results_list.append(self.results_queue.get())
        df = pd.DataFrame(data=results_list, columns=['tconst', 'keywords'])
        myDbHandler = DbHandler()
        myDbHandler.connect()
        df.to_sql("title_keywords", myDbHandler.conn, if_exists='append', index=False)
        return

    def create_and_run_threads(self):
        start_time = time.time()
        for i in range(self.concurrent):
            t = KeywordScrapper(self.queue_of_ids, self.results_queue)
            t.daemon = True
            t.start()
        self.queue_of_ids.join()
        end_time = time.time()
        print("Exiting!")
        print(f"Concurrent: {self.concurrent} Time: {end_time - start_time}")
        print(f"Collected {self.results_queue.qsize()} results")
        self.insert_results_to_db()
        return


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def main():
    myDbHandler = DbHandler()
    myDbHandler.connect()
    tconst_ids = [row["tconst"] for row in myDbHandler.conn.execute(text("SELECT tconst FROM title_basics"))]
    tconst_ids_queue = Queue()
    for chunk in chunks(tconst_ids[:5010], 1000):
        for tconst_id in chunk:
            tconst_ids_queue.put(tconst_id)
        ParScr = ParallelScraper()
        ParScr.queue_of_ids = tconst_ids_queue
        ParScr.create_and_run_threads()
        counter = 0
        while not ParScr.results_queue.empty() and counter < 15:
            print(ParScr.results_queue.get())
            counter += 1
        del ParScr


if __name__ == '__main__':
    ParScr = ParallelScraper()
    ParScr.create_and_run_threads()
