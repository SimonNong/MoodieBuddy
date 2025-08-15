#PROJECT DESCRIPTION
"This program called Moodiebuddy is a mood fixer, purposely for entertainment. It allows the user to tell his/her mood. Then the programe go through a list of movie genres and recommends a movie to watch that matches your current mood"
#Getting libraries for the program
import random
import requests
import os

#Setting up the API environment
#Getting the API key
API_key = os.getenv("TMDB_API_KEY") or input("Enter your TMDB API key: ")
#API_key: 556c7f16cc28474fa9ef7a0dd72cf7cb
API_URL = "https://api.themoviedb.org/3/discover/movie"

#Mapping moods to movie genres in a dictionary
#stressed=animation-fantasy, excited=action-adventure, happy=comedy-family, sad=drama-romance, bored=mystery-thriller
moods = {
  "stressed" : [16, 14],
  "excited" : [28, 12],
  "happy" : [35, 10751],
  "sad" : [18, 10749],
  "bored" : [9648, 53]
}

#What the following function does:
#Fetching the movie from TMDB API by genre list, then sort by popularity, picking random pages and return empty list if there's an error
def get_movie_by_genres(genres):
  params = {
    "api_key" : API_key,
    "with_genres" : ",". join(map(str, genres)),
    "language" : "en-us",
    "sort_by" : "popularity.desc",
    "page" : random.randint(1, 5 )

  }
  try:
    response = requests.get(API_URL, params = params)
    data = response.json()
    return data.get("results", [])
  except :
    return []

#Picking a random movie for a given mood
#the function looks up for mood in the dictionary of moods created and if found, it fetches the list of movies for the genre
#Then it forms a list of random movies
def recommend_movie (mood):
  genres = moods.get(mood)
  if not genres:
    return None
  movies = get_movie_by_genres (genres)
  if not movies:
    return None
  return random.choice(movies)

#MAIN PROGRAM
#Printing a welcome message and available moods
#Then runs a loop asking the user for their mood and if user type 'quit' the program ends
print("Welcome to MOODIEBUDDY!!")
print("Available moods: ", ",".join(moods.keys())) #Corrected line

while True:
  mood = input("\nHow are you feeling today? (or 'quit' to exit):").lower().strip()
  if mood == "quit":
    print("GOODBYE!")
    break # Break statement moved inside the if statement

  #Getting the title, year, and description of the movie
  #Error message is printed if no movie was found
  movie = recommend_movie(mood)
  if movie :
    title = movie.get("title", "unknown title")
    year = movie.get("release_date", "???") [:4]
    overview = movie.get("overview", "No description available")
    print(f"\nRecommendation : {title} ({year})")
    print(f"{overview}")
  else :
    print("Sorry, I could not find a movie recommendation for that mood.")