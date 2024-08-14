# Journal App API

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Stack](#stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Journal Entries](#journal-entries)
  - [Search](#search)
- [Security](#security)
- [Error Handling](#error-handling)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Overview

The Journal App API is a FastAPI-based backend service that provides a robust platform for users to create, manage, and search personal journal entries. This API supports user authentication, CRUD operations for journal entries, and includes features like audio transcription and full-text search capabilities.

## Features

- User registration and authentication
- Create, read, update, and delete journal entries
- Audio transcription for voice journal entries
- Full-text search across journal entries
- Secure password hashing and JWT-based authentication
- CORS support for cross-origin requests
- Health check endpoint for monitoring

## Stack

- **FastAPI**: High-performance web framework for building APIs
- **Pydantic**: Data validation and settings management using Python type annotations
- **SQLAlchemy** (assumed): ORM for database interactions
- **JWT**: JSON Web Tokens for secure authentication
- **CORS**: Cross-Origin Resource Sharing middleware
- **Uvicorn**: ASGI server for running the application

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Balogunolalere/journal-app-api.git
   cd journal-app-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Configuration

1. Create a `.env` file in the root directory and add the following variables:
   ```
   PROJECT_NAME=Journal App
   PROJECT_VERSION=1.0.0
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DATABASE_URL=your_database_url_here
   ```

2. Replace `your_secret_key_here` with a secure random string.

## API Documentation

The API documentation is available at `/api/docs` (Swagger UI) and `/api/redoc` (ReDoc) when the server is running.

### Authentication

- `POST /token`: Obtain a JWT token
- `POST /register`: Register a new user
- `GET /users/me`: Get current user information
- `PUT /users/me/password`: Update user password
- `DELETE /users/me`: Delete user account
- `POST /logout`: Logout (client-side token removal)
- `POST /refresh-token`: Refresh access token

### Journal Entries

- `POST /journal/entries`: Create a new journal entry
- `GET /journal/entries/{entry_id}`: Retrieve a specific journal entry
- `PUT /journal/entries/{entry_id}`: Update a journal entry
- `DELETE /journal/entries/{entry_id}`: Delete a journal entry
- `GET /journal/entries`: List all journal entries (paginated)
- `POST /journal/entries/transcribe`: Create a journal entry from audio file

### Search

- `GET /journal/search`: Search journal entries

## Security

- Passwords are securely hashed before storage
- JWT tokens are used for authentication
- CORS middleware is configured to control access from different origins
- Dependency injection is used to ensure only authenticated users can access protected routes

## Error Handling

The API uses FastAPI's built-in exception handling and HTTP status codes to provide clear error messages. Custom exceptions are raised and caught to handle specific error cases.

## Deployment

1. Ensure all environment variables are properly set
2. Run the application using Uvicorn:
   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
3. For production, consider using a process manager like Gunicorn or deploying with Docker

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
