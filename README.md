Movie App API - README
This API provides basic operations for managing movies and comments. Users can retrieve, add, like, unlike, and comment on movies.

API Endpoints:
GET /movies/
Lists all movies.

POST /movies/
Adds a new movie.

GET /movies/int:id/
Retrieves the details of a specific movie.

PUT /movies/int:id/
Updates a specific movie.

DELETE /movies/int:id/
Deletes a specific movie.

POST /movies/int:id/like/
Likes a specific movie.

POST /movies/int:id/unlike/
Unlikes a specific movie.

GET /movies/int:id/comments/
Retrieves all comments for a specific movie.

POST /movies/int:id/comments/
Adds a new comment to a specific movie.

DELETE /comments/int:id/delete/
Deletes a specific comment.

Permissions:
IsAuthenticatedOrReadOnly: Only authenticated users can add or delete comments. Other actions are accessible to all users.
Responses:
200 OK: The request was successful.
201 CREATED: A new resource was created successfully.
204 NO CONTENT: The resource was deleted successfully.
400 BAD REQUEST: Invalid data.
403 FORBIDDEN: User does not have permission.
404 NOT FOUND: The resource was not found.
Usage:
The API allows you to perform CRUD (Create, Read, Update, Delete) operations on movies and comments.
