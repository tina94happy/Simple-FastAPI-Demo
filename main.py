from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def display_movies(request: Request):
    """
    Fetch movies from movies.json and render an HTML page displaying titles, posters, and release dates.
    """
    with open("movie_data.json", "r") as file:
        movies_data = json.load(file)

    # Parse the movie data
    movies = [
        {
            "title": movie["title"],
            "poster_url": f"https://image.tmdb.org/t/p/original{movie['poster_path']}",
            "release_date": movie.get("release_date", "N/A"),
        }
        for movie in movies_data.get("results", [])
        if movie.get("poster_path")  # Ensure a poster path exists
    ]

    return templates.TemplateResponse("index.html", {"request": request, "movies": movies})

@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request):
    with open("users.json", "r") as file:
        # Convert the string contents to json
        file_contents = "".join(file.readlines())
        users_data = json.loads(file_contents)
    # Parse the user data
    users = [
        {
            "name": user["name"],
            "phone": user["phone"],
            "fave_color": user["fave_color"],
        }
        for user in users_data.get("users", [])
    ]

    return templates.TemplateResponse("users.html", {"request": request, "users": users})