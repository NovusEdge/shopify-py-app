# Shopify App Template

## Setup
1. Clone this template
2. Set up frontend: `cd frontend && npm install`
3. Set up backend: `cd backend && pip install -r requirements.txt`
4. Copy `.env.example` to `.env` in both directories
5. Add your Shopify app credentials

## Development
- Frontend: `npm run dev` (port 3000)
- Backend: `uvicorn main:app --reload --port 8000`

## Architecture
- Frontend: Handles Shopify auth, UI (Polaris), App Bridge
- Backend: Handles business logic, external APIs, data processing