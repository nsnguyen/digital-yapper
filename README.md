# yapyap

chatbot

## Structure

- `backend/`: Python FastAPI application with Poetry
- `frontend/`: React application with TailwindCSS

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.12+ (for local backend development)
- Poetry (for Python dependency management)

### Running with Docker

Start the entire application:

```bash
docker compose --profile dev up
```

Backend will be available at http://localhost:8000
Frontend will be available at http://localhost:3000

### Development

#### Backend

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Run the backend:
   ```bash
   poetry run uvicorn app.main:app --reload --port 8000
   ```

#### Frontend

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run the frontend:
   ```bash
   npm start
   ```

### API Documentation

FastAPI automatically generates OpenAPI documentation for your API.
When the backend is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Pages

- Home: http://localhost:3000/
- Test Data Form: http://localhost:3000/test_endpoint

## Author

Nguyen <your.email@example.com>
