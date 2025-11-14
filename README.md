# BlackLists API

A Flask REST API for managing blocked email addresses with JWT authentication.

## Recommended Versions

- Python 3.13.0

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables on .env file** (optional)
   ```bash
   JWT_SECRET_KEY=your-secret-key
   SQLALCHEMY_DATABASE_URI=sqlite:///app.db
   ```

## Run

```bash
export PYTHONPATH=.
python src/app.py
```

Or alternatively:

```bash
python -m src.app
```

API will be available at `http://localhost:5000`

## Test

```bash
pytest tests/ -v
```
