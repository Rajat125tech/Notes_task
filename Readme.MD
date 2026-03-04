# 🧩 Task & Notes Management API (Dockerized Django Application)

A fully containerized **Django REST API** for managing **Tasks** and **Notes**, featuring **user authentication**, **file uploads**, and **relational linking** between tasks and notes.  
Built as part of a backend engineering assignment — designed for clarity, scalability, and ease of deployment.

---

## 🚀 Features

### 👥 Authentication
- User **signup**, **login**, and **logout** with JWT-based authentication.
- Secure password storage using Django’s built-in hashing.
- Token refresh mechanism for session continuity.

### ✅ Task Management
- Create, update, delete, and mark tasks as completed.
- Retrieve all tasks or a specific task.
- Each task is linked to a specific authenticated user.

### 🗒️ Notes Management
- Create, update, and delete notes.
- Each note can be **linked to a task** (optional association).
- Supports **file uploads** (`.pdf`, `.txt`, `.docx`).
- Notes are private per user.

### 🐳 Dockerized Deployment
- Fully containerized environment with:
  - **Django App**
  - **PostgreSQL Database**
- Runs using a single command:  
  ```bash
  docker compose up --build

🗂️ Folder Structure
APP/
├── app/                  # Main Django application (tasks, notes, auth APIs)
├── core/                 # Core project settings and configurations
├── static/               # Static files (CSS, JS, images)
├── staticfiles/          # Collected static files for production
├── .env.example          # Example environment configuration
├── .gitignore            # Ignored files list for Git
├── docker-compose.yml    # Docker Compose setup for Django + PostgreSQL
├── Dockerfile            # Django app container definition
├── entrypoint.sh         # Entry script for Docker container
├── manage.py             # Django management script
├── Readme.MD             # Project documentation
└── requirements.txt      # Python dependencies



🧾 API Documentation

Integrated Swagger UI for interactive API testing.

All endpoints are self-documented and accessible from /swagger/.

🧱 Tech Stack
Layer	                   Technology
Framework	             Django REST Framework
Database	             PostgreSQL
Authentication	       JWT (SimpleJWT)
Containerization	     Docker, Docker Compose
API Docs	             Swagger (drf-yasg)
File Storage	         Django File System Storage


🐳 Running the Application with Docker

Ensure you have Docker and Docker Compose installed.
1. Clone the repository
git clone https://github.com/Rajat125tech/Notes_task.git
cd Notes_task

2️. Build and start the containers
docker compose up --build

This will:

Build Django and PostgreSQL containers
Apply database migrations automatically


🧪 Example API Endpoints
🔐 Authentication
Method	Endpoint	                         Description
POST	/api/auth/register/	             Register a new user
POST	/api/auth/token/	               Login and get JWT tokens
POST	/api/auth/logout/	            Logout user and blacklist token
POST	/api/auth/token/refresh/	       Refresh access token

👨‍💻 Author
Rajat (Rajat125tech)
srivastava.rajat2004@gmail.com

