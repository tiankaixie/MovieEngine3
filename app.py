from flask import Blueprint
main = Blueprint('main', __name__)
 
import json
from engine import RecommendationEngine
 
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
from flask import Flask, render_template, request, session, redirect, url_for, Response, send_file


@main.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movieName =  request.form.get('movieName')
        res = recommendation_engine.queryMovie(movieName)
        return render_template('result.html', moviename = movieName, search_res = res)
    return render_template('search.html') 

@main.route('/info/<int:movie_id>')
def movieInfo(movie_id):
    rating = recommendation_engine.get_average_rating_for_movie_id(movie_id)
    #return json.dumps(rating)
    return render_template('details.html',score = round(rating[0][1][1],2),num = rating[0][1][0], movie_id = movie_id)

@main.route("/<int:user_id>/ratings/top/<int:count>", methods=["GET"])
def top_ratings(user_id, count):
    logger.debug("User %s TOP ratings requested", user_id)
    top_ratings = recommendation_engine.get_top_ratings(user_id,count)
    return render_template('recommendation.html', movies = top_ratings)
    #return json.dumps(top_ratings)
 
@main.route("/<int:user_id>/ratings/<int:movie_id>", methods=["GET"])
def movie_ratings(user_id, movie_id):
    logger.debug("User %s rating requested for movie %s", user_id, movie_id)
    ratings = recommendation_engine.get_ratings_for_movie_ids(user_id, [movie_id])
    return json.dumps(ratings)
    #return render_template('details.html',score = rating, movie_id = movie_id)

@main.route("/<int:user_id>/rating/<int:movie_id>", methods = ["POST"])
def add_rating(user_id,movie_id):
    rating = [(user_id, (int)(movie_id), (int)(request.form.get('score')))]
    recommendation_engine.add_ratings(rating)
    return redirect("/0/rated")

@main.route("/<int:user_id>/rated")
def rated(user_id):
    rated_movies = recommendation_engine.get_rated_movies(user_id)
    return render_template('rated.html', rated = rated_movies)
    #return json.dumps(rated_movies)
 
@main.route("/<int:user_id>/ratings", methods = ["POST"])
def add_ratings(user_id):
    # get the ratings from the Flask POST request object
    ratings_list = request.form.keys()[0].strip().split("\n")
    ratings_list = map(lambda x: x.split(","), ratings_list)
    # create a list with the format required by the negine (user_id, movie_id, rating)
    ratings = map(lambda x: (user_id, int(x[0]), float(x[1])), ratings_list)
    # add them to the model using then engine API
    recommendation_engine.add_ratings(ratings)
    
    return json.dumps(ratings)
 

def create_app(spark_context, dataset_path):
    global recommendation_engine 

    recommendation_engine = RecommendationEngine(spark_context, dataset_path)    
    
    app = Flask(__name__, static_url_path='/static')
    app.register_blueprint(main)
    return app 
