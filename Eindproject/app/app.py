import random
from random import randint
import requests
import json

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


tags_metadata = [
    {
        "name": "movie",
        "description": "Je kan alle films oplijsten of eentje toevoegen"
    },
    {
        "name": "random movie",
        "description": "De api geeft een willekeurige film terug die je kan kijken"
    },
    {
        "name": "extra info",
        "description": "Hier kan je wat meer info terug vinden over de film, door het gebruik van een andere API"
    }
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="Movie API",
    description="An API to keep track of your movies.",
    contact={
        "name": "Pauline Valgaeren",
        "email": "r0781850@student.thomasmore.be"
    }
)


class Movie(BaseModel):
    titel: str
    regisseur: str
    duur_min: str
    genre: str
    bron: str
    release_datum: str


movies = {
    0: {
        "titel": "Ava",
        "regisseur": "Tate Taylor",
        "duur_min": "1u 37min" ,
        "genre": "Actie/Triller",
        "bron": "Netflix of Apple TV",
        "release_datum": "juli 2020"
    },
   1: {
        "titel": "Avatar",
        "regisseur": "James Cameron",
        "duur_min": "2u 41min",
        "genre": "Sci-fi/Actie",
        "bron": "Google Play Films, Apple TV, Disney+",
        "release_datum": "16 december 2009"
    },
}

# geef een lijst met alle films
@app.get("/movies", tags=["movie"])
async def get_movies():
    return movies


# Geef een specifieke film uit de lijst terug
@app.get("/movie/{movie_id}", tags=["movie"])
async def get_movie(movie_id: int | None = Query(
    default=None,
    description="Het id van de film die je graag zou willen zien.",
)):
    if movie_id in movies:
        return movies[movie_id]
    else:
        return {"error": "De film die u probeerd te zoeken werd niet gevonden in onze bibliotheek."}

# Kies een willekeurige film uit de lijst
@app.get("/randommovie", tags=["random movie"])
async def get_random_movie():
    choice = random.choice(list(movies.keys()))
    return movies[choice]


# Verbinden met een andere aPI
@app.get("/{}", tags=["display"])
async def get_cover(ISBN: str | None = Query(
    default=None,
    description="The ISBN of the book a cover needs to be retreived for.",
)):
    URL = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup{0}".format(ISBN)
    response = requests.get(URL)
    obj = json.loads(response.text)
    cover_link = obj['items'][0]['volumeInfo']['imageLinks']['thumbnail']
    return cover_link


# Voeg een nieuwe film toe
@app.post("/movie", response_model=Movie, tags=["movie"])
async def create_book(movies: Movie):
    key = len(movies)
    movies[key] = movies
    return movies[key]

