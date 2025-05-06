
# Backend Project README

##  Project Overview
This backend provides API services for managing CRM functionalities, built using Django and Django REST Framework. It enables authentication, order processing, and admin operations.

## Getting Started

###  Installation
To set up the project locally, follow these steps:

```
git clone https://github.com/AlexHudkov/crm_backend.git
cd crm_backend
python -m venv venv              # Create a virtual environment
source venv/bin/activate         # On macOS/Linux
venv\Scripts\activate            # On Windows
pip install -r requirements.txt  # Install dependencies
```

###  Environment Variables (.env)
Create a `.env` file to store sensitive configurations:

```
DEBUG=
SECRET_KEY=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Ensure this file is included in `.gitignore` to prevent exposure of sensitive credentials.

###  Running the Project
Apply migrations and start the development server:

```
python manage.py migrate
python manage.py runserver
```

By default, the server runs at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

##  API Documentation

###  Postman Setup
To test API endpoints, import the Postman collection located in:

- `postman/collections/CRM_API.postman_collection.json`
- `postman/environments/CRM Environment.postman_environment.json`

Your Postman environment includes:

- `base_url`: localhost:8000 (update if running in production)
- `access_token`: Used for authentication
- `refresh_token`: Used for renewing sessions

##  Project Structure
```
crm_backend/
├── apps/
│   ├── auth/        # Authentication and user management
│   ├── orders/      # Order processing
│   ├── admin/       # Admin functionalities
│   ├── groups/      # Group management
├── core/
│   ├── dataclasses/ # Utility data classes
│   ├── middlewares/ # Custom middleware logic
│   ├── permissions/ # Permissions and access control
│   ├── services/    # Shared service logic
├── config/          # Django project settings
├── postman/         # Postman API collections
│   ├── collections/
│   ├── environments/
├── manage.py        # Django management script
├── requirements.txt # Dependencies
├── .env             # Environment variables (excluded via .gitignore)
├── .env.example     # Sample env configuration
├── README.md        # Project documentation
```

##  Developer Info
Author: Oleksii Hudkov  
Email: Alexnkest@gmail.com

