# RAG App by [Rhys Josmin](https://rhysjosmin.vercel.app/)
## Overview
A project with:
- `/backend`: Built with Python and FastAPI.
- `/web`: A Next.js web application.

## Directories
- `/backend`: API server using FastAPI.
- `/web`: Frontend built with Next.js.

---

## Backend Setup

### Prerequisites
- Python 3.9+ installed.
- [Poetry](https://python-poetry.org/) installed.

### Installation
1. Navigate to `/backend`:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run the server:
   ```bash
   poetry run python main.py
   ```

---

## Web Setup

### Prerequisites
- Node.js 18+ installed.
- npm or yarn installed.

### Installation
1. Navigate to `/web`:
   ```bash
   cd web
   ```
2. Install dependencies:
   ```bash
   npm install
   # or
   yarn
   ```
3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

---

## Notes
- Ensure the backend is running before accessing the web app.
- Update `.env` file in `/backend` 


```env
CLAYSIS_API_KEY=YOUR API KEY
CLAYSIS_URL= YOUR URL
GROQ_API_KEY=YOUR API KEY
```
```
