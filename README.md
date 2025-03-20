# Team Activities Web Application

A web application for managing team activities, leaderboards, and photo contests.

## Features

- Team registration and management (2-person teams)
- Activity scheduling and participation tracking
- Points system with leaderboard
- Photo uploads and weekly contests
- Mobile and desktop responsive design

## Setup and Installation

1. Clone the repository
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Set environment variables (create a .env file)
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=your-database-url
   S3_BUCKET=your-s3-bucket-name
   S3_KEY=your-s3-key
   S3_SECRET=your-s3-secret
   ```

5. Initialize the database
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application
   ```
   flask run
   ```

## Development

- Run tests: `pytest`
- Format code: `black .`
- Check code style: `flake8`

## Deployment

This application is configured for deployment on AWS.
