from flask import Flask, redirect, url_for, request, render_template
from movierecommender.recommender.Recommender import Recommender
from movierecommender.datahandler.DbHandler import DbHandler
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    enhanced_movies = []
    if request.method == "GET":
        msg = "Provide a title to search for a movie"
    if request.method == "POST":
        movie_param = request.form["title"]
        msg = f"Results for '{movie_param}'"
        if movie_param.strip():  # if movie_param is not whitespace
            dbhandler = DbHandler()
            sql_cmd = f"select tconst, startYear,primaryTitle, genres FROM title_basics " \
                      f"natural join title_keywords WHERE primaryTitle LIKE '%{movie_param}%' LIMIT 20"
            movies = dbhandler.exec_sql_cmd(sql_cmd=sql_cmd)
            for movie in movies:
                movie_dict = {field: movie[field] for field in movie._fields}
                movie_dict['imdburl'] = f"https://www.imdb.com/title/{movie['tconst']}/"
                enhanced_movies.append(movie_dict)
        if not enhanced_movies:
            msg = "No results where found, please try again"
    return render_template("index.html", movies=enhanced_movies,  result_message=msg)


@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    rec = Recommender()
    rec.import_cosine_sim_from_pkl()
    movies_enhanched = []
    msg = ''
    if request.method == "POST":
        tconst_id = request.form['tconst']
        dbhandler = DbHandler()
        movie_title = dbhandler.exec_sql_cmd(f"SELECT primaryTitle FROM title_basics WHERE tconst = '{tconst_id}'")
        msg = f"Recommendations for '{movie_title[0][0]}'"
        print(msg)
        movies = rec.get_recommendation_titles_from_tconst(tconst=tconst_id, limit=20)
        for movie in movies[1:]:
            movies_enhanched.append({
                "tconst": movie[0],
                "title": movie[1],
                "imdburl": f"https://www.imdb.com/title/{movie[0]}/"
            })
    return render_template("recommendations.html", name="Apostolis", movies=movies_enhanched, result_message=msg)


if __name__ == '__main__':
    app.run(debug=True)
