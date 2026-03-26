# Navjeevan AI

## Backend

1. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Run API:
   ```bash
   uvicorn backend.main:app --reload
   ```
3. Chat endpoint:
   - `POST /chat`
   - Body: `{"query": "your question"}`

## Frontend

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run React app:
   ```bash
   npm run dev
   ```

Optional: set `VITE_API_BASE` in frontend environment if backend URL differs.
