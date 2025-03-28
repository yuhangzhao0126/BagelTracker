# BagelTracker

A web application for tracking tennis matches and "bagels" (6-0 sets).

## Features

- User registration and authentication
- Record tennis match results
- Track bagels matches
- View match history and statistics

## Tech Stack

### Frontend
- React
- Bootstrap
- Formik for form handling

### Backend
- Flask (Python)
- SQL Server database
- JWT for authentication

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory: `cd bagel-tracker-backend`
2. Create a virtual environment: `python -m venv bagel-env`
3. Activate the virtual environment:
   - Windows: `bagel-env\Scripts\activate`
   - macOS/Linux: `source bagel-env/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in `.env` file
6. Initialize the database: `python -m app.utils.init_db`
7. Start the server: `python run.py`

### Frontend Setup
1. Navigate to the frontend directory: `cd bagel-tracker-frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

## API Documentation

### Authentication Endpoints
- POST /api/auth/register - Register a new user
- POST /api/auth/login - Login a user

## Contributors
- [Yuhang Zhao](https://github.com/yuhangzhao0126)