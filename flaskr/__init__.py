import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#TODO: change model names
# from models import setup_db, Plant
from models import setup_db, Actor, Movie

# https://flask.palletsprojects.com/en/2.3.x/tutorial/factory/
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    #TODO
    #setup_migration(app)
    #TODO
    #CORS(app)

    # #TODO: swap to using config file and Migrate? Fyyur - or use settings like in Trivia App?
    # # moment = Moment(app)

    # # # https://knowledge.udacity.com/questions/720875
    # # db.init_app(app)

    # # # TODO: connect to a local postgresql database
    # # migrate = Migrate(app, db)

    # db.create_all()
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route
    after completing the TODOs
    """
    #TODO
    # CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    #TODO

        
    @app.route("/")
    def index():
        return jsonify({'message': "Welcome to the Casting Agency App!"})
        
    # ----------------------------------------------------------------------------#
    # Actor Endpoints
    # ----------------------------------------------------------------------------#

    @app.route("/actors")
    #TODO: requires auth to view actors - pass in jwt
    def get_actors():
        """ The get_actors function uses the GET method to
        list all the avaliable actors in the agency.

        The endpoint returns an list of actors if the user has the required 
        view permissions.

        Raises:
        HTTPException: 404, "resource not found", if there are no
        actors in the database.
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """
        allActors = Actor.query.all()

        #     if len(categories) == 0:
        #         abort(404)
        actors = list(map(lambda actor: actor.format(), allActors))

        return jsonify(
            {
                "success": True,
                "Actors":actors,
            }
            )
    
        
        # try:

        #     # Ref: https://knowledge.udacity.com/questions/613259
        #     categories = Category.query.all()

        #     if len(categories) == 0:
        #         abort(404)

        #     return jsonify(
        #         {
        #             "success": True,
        #             "categories": {
        #                 category.id: category.type for category in categories
        #             },
        #         }
        #     )
        # # The below exception statement allows the abort(404) inside
        # # the try block to work.
        # # https://stackoverflow.com/questions/17746897/flask-abort-inside-try-block-behaviour
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    @app.route("/actor/<int:actor_id>/movies")
    #TODO: requires auth to view actors - pass in jwt
    def get_actor_movies(actor_id):
        """ The get_actor_movies function uses the GET method to
        list the movies an actor is cast in based on the actor_id.

        The endpoint returns a list of movies an actor is cast in
        if the user has the required view permissions.

        Raises:
        #TODO - will this work if actor has no movies? or just send message
        "actor has not been cast in any movies yet"
        HTTPException: 404, "resource not found", if there are no
        questions in the category.
        VS
        HTTPException: 404, "resource not found", if the actor_id is not
        in the database.
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """
        #try:
        actor = Actor.query.filter(
            Actor.id == actor_id
            ).one_or_none()
        #if actor is None:
        # abort(404, message = "No actor with that id exists")
        
        movies = [movie.format() for movie in actor.movies]
        
        #if len(movies) == 0:
        #    return jsonify({"message": "This actor has not been cast in any movies yet"})

        return jsonify(
            {
                "success": True,
                "Actor":actor.format(),
                "Movies cast in": movies
            }
            )
    # # The below exception statement allows the abort(404) inside
        # # the try block to work.
        # # https://stackoverflow.com/questions/17746897/flask-abort-inside-try-block-behaviour
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    @app.route("/actors/add", methods=["POST"])
    #TODO: requires auth to add actors - pass in jwt
    def add_actor():
        """ The add_actor endpoint uses the POST method to
        add a new actor to the database.

        The endpoint takes the submitted name, age and gender
        and adds the new actor object to the database.

        Raises:
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """
        body = request.get_json()
        new_name = body.get("name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)

        actor = Actor(
            name=new_name,
            age=new_age,
            gender=new_gender,
        )

        actor.insert()

        return jsonify(
            {
                "success": True,
                "created": actor.id,
            }
        )

        # try:
        #     movie = Movie(
        #         title=new_title,
        #         release_date=new_release_date,
        #     )

        #     movie.insert()

        #     return jsonify(
        #         {
        #             "success": True,
        #             "created": movie.id,
        #         }
        #     )
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    @app.route("/actors/<int:actor_id>/edit", methods=["PATCH"])
    #TODO: requires auth to edit actors - pass in jwt
    def edit_actor(actor_id):
        """ The edit_actor function uses the PATCH method to
        edit a chosen actor from the database.

        The endpoint takes the actor id and, if the actor exists,
        edits it and commits it back to the database.

        Raises:
        HTTPException: 404, "resource not found", if the actor does
        not exist.
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """
        body = request.get_json()
        #try:
        actor = Actor.query.filter(
            Actor.id == actor_id
            ).one_or_none()
        #if actor is None
        if "name" in body:
            actor.name = body.get("name", None)
        if "age" in body:
            actor.age = body.get("age", None)
        if "gender" in body:
            actor.gender = body.get("gender", None)
        actor.update()

        return jsonify(
            {
                "success": True,
                "actor": actor.format(),
            }
        )

        # try:
            # actor = Actor.query.filter(
            #     Actor.id == actor_id
            #     ).one_or_none()
            # if actor is None:
            #     abort(404)
            # if "name" in body:
            #     actor.name = body.get("name")
            # if "age" in body:
            #     actor.age = body.get("age")
            # if "gender" in body:
            #     actor.gender = body.get("gender")
            # actor.update()

            # return jsonify(
        #         {
        #             "success": True,
        #             "actor": actor.format(),
        #         }
        #     )
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    @app.route("/actors/<int:actor_id>/delete", methods=["DELETE"])
    #TODO: requires auth to delete actors - pass in jwt
    def delete_actor(actor_id):
        """ The delete_actor function uses the DELETE method to
        delete a chosen actor from the database.

        The endpoint takes the actor id and, if the actor exists,
        deletes it from the database.

        Raises:
        HTTPException: 404, "resource not found", if the actor does
        not exist.
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """

        actor = Actor.query.filter(
                Actor.id == actor_id
                ).one_or_none()
        
        actor.delete()

        return jsonify(
            {
                "success": True,
                "deleted": actor_id,
            }
        )
        # try:
        #     actor = Actor.query.filter(
        #         Actor.id == actor_id
        #         ).one_or_none()
        #     if actor is None:
        #         abort(404)
        #     actor.delete()

        #     return jsonify(
        #         {
        #             "success": True,
        #             "deleted": actor_id,
        #         }
        #     )
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    # ----------------------------------------------------------------------------#
    # Movie Endpoints
    # ----------------------------------------------------------------------------#

    @app.route("/movies")
    #TODO: requires auth to view movies - pass in jwt
    def get_movies():
        """ The get_movies function uses the GET method to
        list all the avaliable movies in the agency.

        The endpoint returns an list of movies if the user has the required 
        view permissions.

        Raises:
        HTTPException: 404, "resource not found", if there are no
        movies in the database.
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """
        allMovies = Movie.query.all()

        #     if len(categories) == 0:
        #         abort(404)

        movies = list(map(lambda movie: movie.format(), allMovies))

        return jsonify(
            {
                "success": True,
                "Movies":movies,
            }
            )
    
        
        # try:

        #     # Ref: https://knowledge.udacity.com/questions/613259
        #     categories = Category.query.all()

        #     if len(categories) == 0:
        #         abort(404)

        #     return jsonify(
        #         {
        #             "success": True,
        #             "categories": {
        #                 category.id: category.type for category in categories
        #             },
        #         }
        #     )
        # # The below exception statement allows the abort(404) inside
        # # the try block to work.
        # # https://stackoverflow.com/questions/17746897/flask-abort-inside-try-block-behaviour
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    @app.route("/movie/<int:movie_id>/actors")
    #TODO: requires auth to view actors - pass in jwt
    def get_movie_actors(movie_id):
        """ The get_movie_actors function uses the GET method to
        list the actors cast in a movie based on the movie_id.

        The endpoint returns a list of actors cast in a movie
        if the user has the required view permissions.

        Raises:
        #TODO - will this work if movie has no actors? or just send message
        "movie does not have any cast members yet"
        HTTPException: 404, "resource not found", if there are no
        actors cast in the movie.
        VS
        HTTPException: 404, "resource not found", if the movie_id is not
        in the database.
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """
        #try:
        movie = Movie.query.filter(
            Movie.id == movie_id
            ).one_or_none()
        
        actors = [actor.format() for actor in movie.actors]
        
        # actors = (
        #     Actor.query.filter(movie in Actor.movies)
        #     .order_by(Actor.id)
        #     .all()
        #     )
        
        #if movie is None:
        # abort(404)

        #if len(actors) == 0:
        #    return jsonify({"message": "This movie does not have any cast members yet"})

        return jsonify(
            {
                "success": True,
                "Movie":movie.format(),
                "Actors cast": actors
            }
            )
    # # The below exception statement allows the abort(404) inside
        # # the try block to work.
        # # https://stackoverflow.com/questions/17746897/flask-abort-inside-try-block-behaviour
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)


    @app.route("/movies/add", methods=["POST"])
    #TODO: requires auth to add movies - pass in jwt
    def add_movie():
        """ The add_movie endpoint uses the POST method to
        add a new movie to the database.

        The endpoint takes the submitted movie title and
        release date and adds the new movie object to the
        database.

        Raises:
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """
        body = request.get_json()
        new_title = body.get("title", None)
        new_release_date = body.get("release_date", None)

        movie = Movie(
            title=new_title,
            release_date=new_release_date,
        )

        movie.insert()

        return jsonify(
            {
                "success": True,
                "created": movie.id,
            }
        )

        # try:
        #     movie = Movie(
        #         title=new_title,
        #         release_date=new_release_date,
        #     )

        #     movie.insert()

        #     return jsonify(
        #         {
        #             "success": True,
        #             "created": movie.id,
        #         }
        #     )
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    @app.route("/movies/<int:movie_id>/edit", methods=["PATCH"])
    #TODO: requires auth to edit movies - pass in jwt
    def edit_movie(movie_id):
        """ The edit_movie function uses the PATCH method to
        edit a chosen movie from the database.

        The endpoint takes the movie id and, if the movie exists,
        edits it and commits it back to the database.

        Raises:
        HTTPException: 404, "resource not found", if the movie does
        not exist.
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """
        body = request.get_json()
        #try:
        movie = Movie.query.filter(
            Movie.id == movie_id
            ).one_or_none()
        #if actor is None
        if "title" in body:
            movie.title = body.get("title")
        if "release_date" in body:
            movie.release_date = body.get("release_date")
        movie.update()

        return jsonify(
            {
                "success": True,
                "movie": movie.format(),
            }
        )

        # try:
            # actor = Actor.query.filter(
            #     Actor.id == actor_id
            #     ).one_or_none()
            # if actor is None:
            #     abort(404)
            # if "name" in body:
            #     actor.name = body.get("name")
            # if "age" in body:
            #     actor.age = body.get("age")
            # if "gender" in body:
            #     actor.gender = body.get("gender")
            # actor.update()

            # return jsonify(
        #         {
        #             "success": True,
        #             "actor": actor.format(),
        #         }
        #     )
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    @app.route("/movies/<int:movie_id>/delete", methods=["DELETE"])
    #TODO: requires auth to delete movies - pass in jwt
    def delete_movie(movie_id):
        """ The delete_actor function uses the DELETE method to
        delete a chosen actor from the database.

        The endpoint takes the actor id and, if the actor exists,
        deletes it from the database.

        Raises:
        HTTPException: 404, "resource not found", if the actor does
        not exist.
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """

        movie = Movie.query.filter(
                Movie.id == movie_id
                ).one_or_none()
        
        movie.delete()

        return jsonify(
            {
                "success": True,
                "deleted": movie_id,
            }
        )
        # try:
        #     movie = Movie.query.filter(
        #         Movie.id == movie_id
        #         ).one_or_none()
        #     if actor is None:
        #         abort(404)
        #     movie.delete()

        #     return jsonify(
        #         {
        #             "success": True,
        #             "deleted": movie_id,
        #         }
        #     )
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    @app.route("/movie/<int:movie_id>/actor/<int:actor_id>", methods=["POST"])
    #TODO: requires auth to add movies - pass in jwt
    def link_movie_to_actor(movie_id, actor_id):
        """ The add_movie endpoint uses the POST method to
        add a new movie to the database.

        The endpoint takes the submitted movie title and
        release date and adds the new movie object to the
        database.

        Raises:
        HTTPException: 422, "unprocessable", if the request cannot be
        completed.
        """
        #TODO what about get_or_404? will this remove lines of code?
        movie = Movie.query.filter(
                Movie.id == movie_id
                ).one_or_none()
        
        # if movie is None:
        #     abort(404)

        actor = Actor.query.filter(
                Actor.id == actor_id
                ).one_or_none()
        
        # if actor is None:
        #     abort(404)

        movie.actors.append(actor)
        movie.insert()

        #TODO - are both needed?
        # actor.movies.append(movie)
        # actor.insert()


        return jsonify(
            {
                "success": True,
                #TODO return names instead of IDs?
                "Movie linked": movie.id,
                "Actor linked": actor.id
            }
        )

        # try:
        #     movie = Movie(
        #         title=new_title,
        #         release_date=new_release_date,
        #     )

        #     movie.insert()

        #     return jsonify(
        #         {
        #             "success": True,
        #             "created": movie.id,
        #         }
        #     )
        # except Exception as e:
        #     if isinstance(e, HTTPException):
        #         abort(e.code)
        #     else:
        #         abort(422)

    # ----------------------------------------------------------------------------#
    # Error Handling.
    # ----------------------------------------------------------------------------#

    #TODO: add error handling for at least four status codes

    return app