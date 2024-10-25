# Project Name: Posts and Comments API

## Description
This project provides an API for managing posts and comments, including user registration, authentication, post creation, and comment management. It also includes functionality for automatic replies and analytics for posts and comments. The API is built using Django and Django Ninja for fast and efficient API development. The application uses Docker for containerization, allowing easy deployment and scaling.

## Key Features
- User registration and authentication
- Create, update, and delete posts
- Comment management
- Automatic replies to comments
- Analytics on posts and comments
- Celery integration for asynchronous tasks
- Redis for caching and message brokering
- PostgreSQL as the database
- Dockerized application for easy deployment

## Technologies Used
- **Django**: A high-level Python web framework
- **Django Ninja**: A framework for building fast APIs
- **Celery**: Distributed task queue for handling asynchronous tasks
- **Redis**: In-memory data store used for caching and message brokering
- **PostgreSQL**: Relational database for storing persistent data
- **Docker**: Containerization platform for application deployment

## Installation Instructions
1. Clone the repository to your local machine:
   ```bash
   git clone git@github.com:krasheg/StarNavi_test_task.git

2. Ensure that you have Docker and Docker Compose installed.
3. Open the terminal and navigate to the project directory.
4. Create .env with all necessary variables
    ```bash
   cp .env_example .env
5. Grant execute permissions to the bash script.
    ```bash
   sudo chmod +x wait-for-it.sh
6. Run the following command to build and start the application in the background:
    ```bash
    docker-compose up -d --build
7. After the containers are built and running, the API will be available at: 
    ```bash
    http://localhost:8000/api/
8. The following services will be available:

- API: 

    ```bash
    http://localhost:8000/api/

- PostgreSQL database
- Redis for caching and Celery broker
- Celery for handling background tasks
### Running Tests: 
You can run the project's tests by executing the following command inside the Django container:

    docker exec -it <container_name> python manage.py test

**Note**: Replace `<container_name>` with the name of your Django container, typically something like `posts_comments-django-1`.

**Usage**: You can interact with the API via tools like *Postman*, *curl*, or any HTTP client. The project includes routes for user registration, ***login, creating posts, adding comments***, etc.

- If you need to view the available API endpoints, you can find the documentation at:       
```bash 
http://localhost:8000/api/docs