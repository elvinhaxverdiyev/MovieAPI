Movie App API - README 🎬
Overview 🌟
This API allows users to interact with movies, including viewing a list of movies, adding new ones, searching by title, liking movies, commenting, and filtering movies by genre. The API is built with Django and the Django REST framework, offering both functionality for authenticated users and read-only access to public data. The API also includes pagination for movie listings and allows users to interact with specific movies, comments, and likes. 🎥🍿

Features ✨
Movie List (GET & POST): Retrieve a paginated list of movies and add new movies 📜
Movie Detail (GET, PATCH, DELETE): Retrieve detailed information, update, or delete a movie (only by the creator) 🛠️
Like a Movie (GET & POST): View the like count and like movies 🍿
Add/View Comments (GET & POST): View existing comments and add new ones 💬
Delete Comments (DELETE): Users can delete their own comments ❌
Search Movies by Title (GET): Search for movies using a query string 🔍
Filter Movies by Genre (GET): Filter movies based on their genre 🎬

Authentication 🔑
Some endpoints require authentication (IsAuthenticatedOrReadOnly), such as liking movies, adding comments, or modifying movies.
Authentication can be done using Django's built-in token authentication or any other method supported by Django REST Framework.

Endpoints 📍
1. Movie List (GET, POST)
GET: /api/movies/
Retrieve a list of movies (paginated).
Response: Paginated list of movies.

POST: /api/movies/
Create a new movie.
Body: JSON data (e.g., title, description, genre)
Response: New movie data with 201 CREATED status.

2. Movie Detail (GET, PATCH, DELETE)
GET: /api/movies/{id}/
Retrieve details of a specific movie by id (view count increases).
Response: Movie details, like count, views count.

PATCH: /api/movies/{id}/
Update a movie's information (only the creator can update).
Body: Partial data (e.g., new description, title, etc.)
Response: Updated movie data.

DELETE: /api/movies/{id}/
Delete a movie (only the creator can delete).
Response: { "message": "Movie deleted" } with 204 NO CONTENT.

3. Movie Like (GET, POST)
GET: /api/movies/{id}/likes/
View the like count and a list of users who liked the movie.
Response: Likes count and a list of users who liked the movie.

POST: /api/movies/{id}/likes/
Like a movie (one like per user).
Response: { "message": "Movie liked" } with 201 CREATED.

4. Add/View Comments (GET, POST)
GET: /api/movies/{id}/comments/
Retrieve all comments for a specific movie.
Response: List of comments for the movie.

POST: /api/movies/{id}/comments/
Add a comment to a movie (authentication required).
Body: JSON with text field.
Response: Created comment data.

5. Delete Comment (DELETE)
DELETE: /api/comments/{id}/
Delete a user's own comment.
Response: { "message": "Comment deleted" } with 204 NO CONTENT.
6. Search Movies by Title (GET)
GET: /api/movies/search/
Search for movies by title (query parameter: q).
Response: List of movies matching the search query.
7. Filter Movies by Genre (GET)
GET: /api/movies/genre/
Filter movies by genre (query parameter: genre).
Response: List of movies belonging to the specified genre.

Pagination 📑
The Movie List view supports pagination, returning 2 movies per page by default.
The response includes links to navigate between pages.

Installation & Setup 🖥️
Install required dependencies:
pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Run the development server:
python manage.py runserver

Then navigate to http://127.0.0.1:8000/api/ to interact with the API.

Usage 💻
Create a movie: Send a POST request to /api/movies/ with the movie data.
Like a movie: Send a POST request to /api/movies/{id}/likes/ to like a movie.
Add a comment: Send a POST request to /api/movies/{id}/comments/ with the comment text.
Search for a movie: Send a GET request to /api/movies/search/ with the q query parameter.
Filter by genre: Send a GET request to /api/movies/genre/ with the genre query parameter.

Notes ⚠️
Users can only like a movie once.
Users can only delete their own comments.
Movie creators can edit or delete their own movies.
All endpoints are designed to return responses in JSON format.
Recommendations 📋
For authentication, use Django REST Framework's token authentication.
For more information on pagination, check Django REST Framework Pagination Docs.
Enjoy using the Movie App API! 🎉🎬
