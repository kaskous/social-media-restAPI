# HackSoft Django API

This project is a Django-based JSON API backend for a social media platform, designed to work with a React frontend. It implements user authentication, post creation and management, and a feed system.

## Features

- User registration and authentication using JWT
- User profile management
- Post creation, soft deletion, and restoration
- Like/unlike functionality for posts
- Feed API with pagination
- Automatic hard deletion of soft-deleted posts after 10 days
- Django admin interface for user and post management

## Technology Stack

- Python 3.9+
- Django 4.2
- Django Rest Framework
- Simple JWT for authentication
- Poetry for dependency management
- SQLite (default database)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hacksoft-django-api.git
   cd hacksoft-django-api
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

3. Activate the virtual environment:
   ```
   poetry shell
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- `POST /api/register/`: Register a new user
- `POST /api/login/`: Obtain JWT token
- `POST /api/logout/`: Logout (blacklist token)
- `GET /api/profile/`: Get current user profile
- `PATCH /api/profile/`: Update current user profile
- `POST /api/posts/`: Create a new post
- `GET /api/posts/`: List all posts
- `GET /api/posts/{id}/`: Retrieve a specific post
- `DELETE /api/posts/{id}/`: Soft delete a post
- `POST /api/posts/{id}/like_post/`: Like a post
- `POST /api/posts/{id}/unlike_post/`: Unlike a post
- `GET /api/feed/`: Get paginated feed of posts

For a complete list of endpoints and their usage, refer to the Swagger documentation at `/api/schema/swagger-ui/`.


## Request Flow

Here's a step-by-step guide to interacting with the main features of the API:

### 1. Register a new user
```bash
curl --location --request POST 'http://localhost:8000/api/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123",
    "short_description": "This is a new user!"
}'
```

### 2. Login and obtain JWT token
```bash
curl --location --request POST 'http://localhost:8000/api/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "newuser",
    "password": "securepassword123"
}'
```

### 3. Create a new post
```bash
curl --location --request POST 'http://localhost:8000/api/posts/' \
--header 'Authorization: Bearer <your_access_token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "content": "This is my first post!"
}'
```

### 4. Like a post
```bash
curl --location --request POST 'http://localhost:8000/api/posts/{post_id}/like_post/' \
--header 'Authorization: Bearer <your_access_token>'
```

### 5. Unlike a post
```bash
curl --location --request POST 'http://localhost:8000/api/posts/{post_id}/unlike_post/' \
--header 'Authorization: Bearer <your_access_token>'
```

### 6. Get user profile
```bash
curl --location --request GET 'http://localhost:8000/api/profile/' \
--header 'Authorization: Bearer <your_access_token>'
```

### 7. Update user profile
```bash
curl --location --request PATCH 'http://localhost:8000/api/profile/' \
--header 'Authorization: Bearer <your_access_token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "short_description": "I'm updating my profile!"
}'
```

### 8. Get feed
```bash
curl --location --request GET 'http://localhost:8000/api/feed/' \
--header 'Authorization: Bearer <your_access_token>'
```

### 9. Logout (Blacklist token)
```bash
curl --location --request POST 'http://localhost:8000/api/logout/' \
--header 'Authorization: Bearer <your_access_token>'
```

### 10. Soft Delete a post
```bash
curl --location --request DELETE 'http://localhost:8000/api/posts/{post_id}/' \
--header 'Authorization: Bearer <your_access_token>'
```

Note: Replace `<your_access_token>` with the actual JWT token received from the login endpoint. Also, replace `{post_id}` with the actual ID of the post you want to interact with.

These examples assume you're running the server locally on port 8000. Adjust the URL if your setup is different.

## Authentication

This API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header of your requests:

```
Authorization: Bearer <your_token_here>
```

## User Registration Process

1. Users can register through the `/api/register/` endpoint.
2. New users are initially marked as inactive and need to be validated by a superuser.
3. Superusers can validate users through the Django admin interface.

## Post Management

- Posts can be soft-deleted, which marks them as deleted but keeps them in the database.
- Soft-deleted posts can be restored by superusers through the admin interface.
- A management command automatically hard-deletes posts that were soft-deleted more than 10 days ago.

## Running Tests

To run the test suite:

```
python manage.py test
```

## Management Commands

To manually trigger the deletion of old soft-deleted posts:

```
python manage.py delete_old_soft_deleted_posts
```

## Development Notes

- The project uses `drf-spectacular` for API documentation. You can view the Swagger UI at `/api/schema/swagger-ui/`.
- Profile pictures are stored in the `media/profile_pictures/` directory.
- The `DEFAULT_AUTO_FIELD` is set to `'django.db.models.BigAutoField'`.

## Security Considerations

- Ensure to change the `SECRET_KEY` in `settings.py` before deploying to production.
- The `DEBUG` setting is currently set to `True`. Set it to `False` in production.
- Consider using a more robust database like PostgreSQL for production use.

## Deployment

This project is designed to be deployed as an API backend. The frontend is expected to be a separate React application. When deploying:

1. Update `ALLOWED_HOSTS` in `settings.py`.
2. Configure your web server to serve static and media files.
3. Set up a production-ready database.
4. Use environment variables for sensitive settings.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.