import requests
import re
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.urls import reverse
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# The homepage
def index(request):
    return render(request, "account/index.html")


# Registration page
def register(request):

    registered = False
    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for {username}! Now you can use the search function!")
            return redirect("index")

    else:

        form = CreateUserForm()

    return render(request, "account/registration.html",
                  {"form": form, "registered": registered})


# Logout with the added decorator so that only logged users can access the logout option
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Login page
def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Username or password is incorrect!")
            return render(request, "account/login.html", {})
    else:
        return render(request, "account/login.html", {})


# The search algorithm made out of BeautifulSoup and Youtube API
@login_required
def search_result(request):
    api_key = "AIzaSyCfhbTthwHuEkZAR-Z4kl1zsqmPHFu31Xg"

    # Adding the Youtube Api to a variable
    youtube = build("youtube", "v3", developerKey=api_key)

    # Creating a variable that inherits the re function's filtering system
    clean = re.compile('<.*?>')

    # Creating a variable that inherits the user's input regarding the search limit
    search_number = request.GET["search_numbers"]

    # User's input regarding the movie_search genre search
    user_input = request.GET["user_input"]

    # Request for the IMDB's address in which the user adds the genre though user_input
    source = requests.get("https://www.imdb.com/search/title/?genres=" + user_input)

    # Using BeautifulSoup to scrape, converting the page's resource to text and using the
    # html parser to parse the html code
    soup = BeautifulSoup(source.text, 'html.parser')

    # Creating a container for all the results created by BeautifulSoup
    articles = soup.find_all("div", class_="lister-item mode-advanced")

    # Lists that will contain parsed items
    headline_list = []
    summary_list = []
    launch_date_list = []
    movie_duration_list = []
    movie_rating_list = []
    director_list = []
    star1_list = []
    star2_list = []
    star3_list = []
    image_list = []
    image_list_modified = []
    rating_list_modified = []
    movie_duration_modified_list = []
    movtrailer_list = []
    movtrailer_searched_list = []
    movtrailer_ready_list = []

    # Looping though the main div using the user's input search number to limit the amount of examples yield by the loop
    for item in articles[:int(search_number)]:
        # Titles:
        headline = item.find("h3", class_="lister-item-header").a.text
        headline_list.append(headline)

        # Description:
        summary = item.find_all("p", class_="text-muted")[1].text
        summary_list.append(summary)

        # Launch date:
        launch_date = item.h3.find("span", class_="lister-item-year text-muted unbold").text
        launch_date_list.append(launch_date)

        # Movie duration:
        movie_duration = str(item.find("span", class_="runtime"))
        movie_duration_list.append(movie_duration)

        # Movie rating:
        movie_rating = str(item.find("strong"))
        movie_rating_list.append(movie_rating)

        # Director:
        director = item.find_all("p")[2]("a")[0].text
        director_list.append(director)

        # First actor:
        star1 = item.find_all("p")[2]("a")[1].text
        star1_list.append(star1)

        # Second actor:
        star2 = item.find_all("p")[2]("a")[2].text
        star2_list.append(star2)

        # Third actor:
        star3 = item.find_all("p")[2]("a")[3].text
        star3_list.append(star3)

        # Poster image:
        image = item.find("img", class_="loadlate")
        image_list.append(image)

    # Filtering data before adding it to a new list for the HTML loop

    # Filtering image:
    for item in image_list:
        image_list_modified.append(item.get("loadlate"))

    # Cleaning the rating list
    for item in movie_rating_list:
        rating_list_modified.append((re.sub(clean, "", item)))

    # Cleaning the duration list
    for item in movie_duration_list:
        movie_duration_modified_list.append((re.sub(clean, "", item)))

    # Adding "movie_search trailer" to the search string in order to minimize incorrect search results
    for item in headline_list:
        movtrailer_list.append(item + " movie%trailer")

    # Looping through the list to search for the videos using the Youtube API
    for item in movtrailer_list:
        ytsearch = youtube.search().list(
            q="".join(item),
            part="snippet",
            type="video")

        movtrailer_searched_list.append(ytsearch.execute())

    # Filtering through the list and dictionaries created by the API in order to add the Youtube video IDs to a list
    for item in movtrailer_searched_list:
        movtrailer_ready_list.append(item["items"][0]["id"]["videoId"])

    # Creating a zip with all the lists so we can loop through them using the loops in the movie_search.html file
    container = zip(headline_list, summary_list, launch_date_list, movie_duration_modified_list, rating_list_modified,
                    director_list, star1_list, star2_list, star3_list, image_list_modified, movtrailer_ready_list)

    return render(request, "movie_search/movie.html", {"container": container})


@login_required
def input_genre(request):
    return render(request, "movie_search/search.html")
