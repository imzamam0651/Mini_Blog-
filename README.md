# Mini Blog Platform – API Documentation

This Django/Django REST Framework project provides a simple “mini blog” API with user registration, login, CRUD for posts, likes, and comments. All endpoints requiring authentication expect a Token in the `Authorization` header:

http://127.0.0.1:8000/api/

📂 Complete Endpoints Summary
Action	                Method	        URL	                 Auth Required
Register User	          POST	      /api/register/	            No
Login User	            POST	      /api/login/	                No
Create Post	            POST	      /api/posts/	                Yes
List All Posts	        GET	        /api/posts/	                Yes
Get Specific Post (Own)	GET	        /api/posts/<post_id>/	      Yes
Edit Post (Own)	        PUT	        /api/posts/<post_id>/	      Yes
Delete Post (Own)	      DELETE	    /api/posts/<post_id>/	      Yes
Like Post	              POST	      /api/like/<post_id>/	      Yes
Comment on Post	        POST	      /api/comment/<post_id>/	    Yes


#1. REGISTER
POST /api/register/

- **Request Body (JSON)**
  ```json
  {
    "username": "alice",
    "password": "securepassword123"
  }

# cURL Example

curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "securepassword123"
  }'

# Response (JSON)
{
  "token": "0123456789abcdef0123456789abcdef01234567"
}


#2. User Login
POST /api/login/

#cURL Example
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "securepassword123"
  }'

# Response (JSON)
{
  "token": "0123456789abcdef0123456789abcdef01234567"
}


#3. Create Post
Authenticated users can create a new blog post.

POST /api/posts/

#Headers
Authorization: Token <YOUR_TOKEN>
Content-Type: application/json

#Request Body (JSON)
{
  "title": "My First Blog Post",
  "content": "Hello world! This is my first post."
}

# cURL Example
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "Hello world! This is my first post."
  }'

# Response (JSON)
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "Hello world! This is my first post.",
  "author": 1,
  "created_at": "2025-05-31T14:20:00Z"
}


#4. List All Posts
Retrieve a list of all blog posts. (Any authenticated user.)

GET /api/posts/
Headers


Authorization: Token <YOUR_TOKEN>

# cURL Example

curl -X GET http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token <YOUR_TOKEN>"


# Response (JSON)
[
  {
    "id": 1,
    "title": "My First Blog Post",
    "content": "Hello world! This is my first post.",
    "author": 1,
    "created_at": "2025-05-31T14:20:00Z"
  },
  {
    "id": 2,
    "title": "Another Day",
    "content": "Just sharing some thoughts…",
    "author": 2,
    "created_at": "2025-06-01T09:45:00Z"
  }
  // … more posts
]


#5. Get Specific Post (Own-Only)
Retrieve a single post by ID. Users can only fetch their own post via this endpoint.


GET /api/posts/<post_id>/

# Headers

Authorization: Token <YOUR_TOKEN>

# cURL Example

curl -X GET http://127.0.0.1:8000/api/posts/1/ \
  -H "Authorization: Token <YOUR_TOKEN>"

# Response (JSON)
If you are the author of post 1:

{
  "id": 1,
  "title": "My First Blog Post",
  "content": "Hello world! This is my first post.",
  "author": 1,
  "created_at": "2025-05-31T14:20:00Z"
}

* Errors

404 Not Found if the post does not exist or does not belong to you.

401 Unauthorized if no valid token is provided.


#6. Edit Post
Authenticated users can update only their own post.

PUT /api/posts/<post_id>/

# Headers

Authorization: Token <YOUR_TOKEN>
Content-Type: application/json

# Request Body (JSON)
Include only the fields you want to update (both fields required in this setup).

{
  "title": "My First Blog Post – Edited",
  "content": "Updated content goes here."
}

# cURL Example

curl -X PUT http://127.0.0.1:8000/api/posts/1/ \
  -H "Authorization: Token <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post – Edited",
    "content": "Updated content goes here."
  }'

# Response (JSON)

{
  "id": 1,
  "title": "My First Blog Post – Edited",
  "content": "Updated content goes here.",
  "author": 1,
  "created_at": "2025-05-31T14:20:00Z"
}

* Errors

403 Forbidden if you’re not the author.

404 Not Found if the post doesn’t exist.

401 Unauthorized if no valid token is provided.


#7. Delete Post
Authenticated users can delete only their own post.


DELETE /api/posts/<post_id>/
Headers

Authorization: Token <YOUR_TOKEN>

# cURL Example

curl -X DELETE http://127.0.0.1:8000/api/posts/1/ \
  -H "Authorization: Token <YOUR_TOKEN>"

# Response

Status Code: 204 No Content on success

*Errors:

403 Forbidden if you’re not the author

404 Not Found if the post doesn’t exist

401 Unauthorized if no valid token is provided


#8. Like Post
Authenticated users can like any post. Each user can like a given post only once.

POST /api/like/<post_id>/

# Headers

Authorization: Token <YOUR_TOKEN>

# cURL Example

curl -X POST http://127.0.0.1:8000/api/like/2/ \
  -H "Authorization: Token <YOUR_TOKEN>"

#Response (JSON)

{
  "message": "Liked"
}
If already liked:


{
  "message": "Already liked"
}

* Errors

404 Not Found if <post_id> does not exist.

401 Unauthorized if no valid token is provided.


#9. Comment on Post
Authenticated users can add a comment to any post.

POST /api/comment/<post_id>/

#Headers

Authorization: Token <YOUR_TOKEN>
Content-Type: application/json

# Request Body (JSON)

{
  "content": "Great post! Thanks for sharing."
}

# cURL Example

curl -X POST http://127.0.0.1:8000/api/comment/2/ \
  -H "Authorization: Token <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Great post! Thanks for sharing."
  }'

# Response (JSON)

{
  "id": 5,
  "user": 3,
  "blog": 2,
  "content": "Great post! Thanks for sharing.",
  "created_at": "2025-06-02T06:15:00Z"
}

*Errors

404 Not Found if <post_id> does not exist.

400 Bad Request if the payload is invalid.

401 Unauthorized if no valid token is provided.


🔒 Authentication Header Example
For any request that requires a token, include this header exactly as shown:
Authorization: Token <YOUR_TOKEN>

** Dependencies **
🔧 Project Setup
1. Environment Setup

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install Django and DRF
pip install django djangorestframework djoser

