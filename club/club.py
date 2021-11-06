import os
import requests
import random
import json
# from flask import Flask, render_template, request, redirect, url_for, session
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.exceptions import HTTPException
from base64 import b64encode
from functions import get_data, base_url, img_url
from main import app, oauth
from auth.auth import login_required

bp = Blueprint('club', __name__, url_prefix='/club')

@bp.route("/search")
@login_required
def search():
    search = request.args.get('q')
    results = get_data(
        f"search/multi?language=en-US&page=1&include_adult=false&query={search}&")
    results = results["results"]
    set_movie = results[0]

    return render_template("search_result.html",  set_movie=set_movie, img_url=img_url, results=results)


@bp.route('/')
@bp.route('/index')
@bp.route('/home')
@login_required
def index():
    with open('static/tmp/json/popular.json', 'r') as f:
        popular = json.load(f)

    with open('static/tmp/json/trend.json', 'r') as f:
        trend = json.load(f)

    with open('static/tmp/json/netflix.json', 'r') as f:
        netflix = json.load(f)

    secure_random = random.SystemRandom()
    set_movie = secure_random.choice(popular)

    return render_template('index.html', set_movie=set_movie, img_url=img_url, popular=popular, trend=trend, netflix=netflix)


@bp.route('/filmes')
@bp.route('/movie')
@login_required
def movie():
    with open(f'static/tmp/json/movie/genres.json', 'r') as f:
        genres = json.load(f)
    genres = genres["genres"]

    for genre in genres:
        with open(f'static/tmp/json/movie/{genre["name"]}.json', 'r') as f:
            genre["results"] = json.load(f)

    with open('static/tmp/json/movie/popular.json', 'r') as f:
        popular = json.load(f)

    with open('static/tmp/json/movie/trend.json', 'r') as f:
        trend = json.load(f)

    with open('static/tmp/json/movie/netflix.json', 'r') as f:
        netflix = json.load(f)

    secure_random = random.SystemRandom()
    set_movie = secure_random.choice(popular)

    return render_template('filmes.html', set_movie=set_movie, img_url=img_url, genres=genres, popular=popular, trend=trend, netflix=netflix)


@bp.route('/series')
@bp.route('/tv')
@login_required
def series():
    with open(f'static/tmp/json/tv/genres.json', 'r') as f:
        genres = json.load(f)
    genres = genres["genres"]

    for genre in genres:
        with open(f'static/tmp/json/tv/{genre["name"]}.json', 'r') as f:
            genre["results"] = json.load(f)

    with open('static/tmp/json/tv/popular.json', 'r') as f:
        popular = json.load(f)

    with open('static/tmp/json/tv/trend.json', 'r') as f:
        trend = json.load(f)

    with open('static/tmp/json/tv/netflix.json', 'r') as f:
        netflix = json.load(f)

    secure_random = random.SystemRandom()
    set_show = secure_random.choice(popular)

    return render_template('series.html', set_show=set_show, img_url=img_url, genres=genres, popular=popular, trend=trend, netflix=netflix)


@bp.route("/<type>/about/<id>")
@login_required
def about(type, id):
    movie = get_data(f'{type}/{id}?')
    return render_template('sobre.html', movie=movie, img_url=img_url)


@bp.errorhandler(HTTPException)
def handle_exception(e):
    code = e.code
    resp = requests.get(f"http://http.cat/{code}")
    obj = resp.content
    image = b64encode(obj).decode("utf-8")
    return render_template("error_generic.html", title=e.name, description=e.description, image=image, code=code), code
