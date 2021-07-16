from movierecommender.recommender.Recommender import Recommender
import sys
from art import tprint
from prettytable import PrettyTable


def main():
    rec = Recommender()
    rec.import_cosine_sim_from_pkl()
    tprint("Movie Recommender")

    while True:
        ptable = PrettyTable()
        tconst = input("Enter a tconst id to get recommendations or type exit to exit: ")
        if tconst == 'exit':
            sys.exit(0)
        recommendation_titles = rec.get_recommendation_titles_from_tconst(tconst)[1:]
        ptable.field_names = ['Tconst', 'Title']
        ptable.add_rows(recommendation_titles)
        print(ptable)


if __name__ == '__main__':
    main()
