# Project Name

## Overview

This project consists of a FastAPI backend and a frontend application. This README provides detailed instructions for setting up and running both components.

## Requirements

- Python 3.10
- Node.js and npm

## Installation and Setup

### Clone the Repository

```bash
git clone https://github.com/username/nephro-scan.git
cd app
```

### Backend Setup

1. Create and activate a Python virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Start the FastAPI backend:

```bash
cd backend
uvicorn app:app --reload
```

The backend API will be available at http://127.0.0.1:8000. The interactive API documentation can be accessed at http://127.0.0.1:8000/docs.

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install npm packages:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The frontend application will be available at the URL shown in your terminal (typically http://localhost:3000 or http://localhost:5173).

## Project Structure

```
project-name/
├── backend/               # FastAPI backend
│   ├── app.py             # Main application file
│   ├── requirements.txt   # Python dependencies
│   └── ...
└── frontend/              # Frontend application
    ├── package.json
    └── ...
```
