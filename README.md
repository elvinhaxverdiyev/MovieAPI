Movie API 🎬
This API provides access to movies, allowing users to register, log in, create, update, delete, like movies, and interact with movie comments. Users can also filter movies by genre, search by title, and receive movie-related emails upon creation. 📨

Features ✨
User Registration: Create a new user and get an authentication token.
Login/Logout: Users can log in and out using their credentials.
Movies:
List all movies
Create new movies (for authenticated users only)
Retrieve, update, and delete movies (only the creator or admin has permission)
Likes: Users can like movies. Each movie has a like count.
Comments: Add, view, and delete comments on movies.
Search & Filter: Search movies by title and filter by genre.

Endpoints 📡
User Endpoints 👤
POST /register/: Register a new user. Returns a message and authentication token.
POST /login/: Log in a user and return an authentication token.
POST /logout/: Log out the current user.
Movie Endpoints 🎥
GET /movies/: Get a list of movies (paginated).
POST /movies/: Create a new movie (authenticated users only).
GET /movies/{id}/: Retrieve a movie by ID.
PATCH /movies/{id}/: Update a movie (only by the creator or admin).
DELETE /movies/{id}/: Delete a movie (only by the creator or admin).
Like Endpoints ❤️
GET /movies/{id}/like/: Get the number of likes and users who liked a movie.
POST /movies/{id}/like/: Like a movie.
Comment Endpoints 💬
GET /movies/{id}/comments/: Get all comments on a movie.
POST /movies/{id}/comments/: Add a comment to a movie (authenticated users only).
DELETE /comments/{id}/: Delete your own comment.
Search Endpoints 🔍
GET /movies/search/: Search for movies by title.
Genre Filter 🏷️
GET /movies/genre/: Get movies filtered by genre.

Permissions 🔐
IsAuthenticated: Only authenticated users can access specific endpoints.
AllowAny: Accessible by any user.
IsAuthenticatedOrReadOnly: Authenticated users can perform all actions, others can only read.
HeHasPermission: Ensures the user is either the creator or admin to perform some actions (like editing and deleting).

Email Notifications 📧
Whenever a new movie is created, an email is sent to the user confirming the creation.

Troubleshooting 🛠️
If you encounter any errors with authentication, ensure your token is correct.
For issues with pagination, check the page_size or use query parameters to navigate between pages.

Documentation Link:
http://127.0.0.1:8000/swagger/

Enjoy using the Movie API! 🎉
