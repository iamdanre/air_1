# Air Research Preview Program: Backend API

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at http://127.0.0.1:8000

3. **Run tests:**
   ```bash
   pytest
   ```

## Project Structure
- `main.py`: FastAPI app entrypoint
- `models.py`: SQLAlchemy models
- `schemas.py`: Pydantic schemas
- `database.py`: DB setup and test data
- `crud.py`: CRUD operations
- `tests/`: Endpoint autotests

## Notes
- Uses SQLite for file-based storage (no setup required)
- Initial test data is loaded on first run 