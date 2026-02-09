# PROJECT STRUCTURE: Directory Layout & File Organization

## 📁 Complete Project Directory Tree

```
tree-wisdom/
│
├── README.md                              # Project documentation for humans
├── requirements.txt                       # Python dependencies
├── .env                                   # Environment configuration (Ollama host, ports)
├── .gitignore                             # Git exclusions
│
├── app/                                   # Backend FastAPI application
│   ├── __init__.py                        # Package initialization
│   ├── main.py                            # Main FastAPI application instance
│   ├── config.py                          # Configuration settings (DB path, uploads dir)
│   ├── models.py                          # SQLAlchemy database models
│   ├── schemas.py                         # Pydantic validation schemas
│   ├── database.py                        # Database connection and session management
│   │
│   ├── routers/                           # API route handlers
│   │   ├── __init__.py
│   │   ├── trees.py                       # GET /api/trees, GET /api/trees/{id}
│   │   ├── documents.py                   # POST /api/documents (upload + create)
│   │   ├── observations.py                # GET /api/observations, POST /api/observations
│   │   ├── reflections.py                 # POST /api/reflections/analyze (LLM integration)
│   │   └── gallery.py                     # GET /api/gallery (all user docs)
│   │
│   ├── services/                          # Business logic and utilities
│   │   ├── __init__.py
│   │   ├── image_service.py               # Image upload, validation, storage
│   │   ├── llm_service.py                 # Ollama API calls and prompt management
│   │   ├── tree_service.py                # Tree database queries and caching
│   │   ├── document_service.py            # Document creation, retrieval, export
│   │   └── exif_service.py                # EXIF metadata extraction
│   │
│   ├── prompts/                           # LLM system prompts
│   │   ├── __init__.py
│   │   ├── cultural_contextualization.py  # Prompt for cultural interpretation
│   │   ├── species_identification.py      # Prompt for tree species analysis
│   │   └── cross_cultural_comparison.py   # Prompt for comparing cultural meanings
│   │
│   └── templates/                         # Jinja2 templates (served by FastAPI)
│       ├── base.html                      # Base template with header/footer
│       ├── index.html                     # Home page / gallery view
│       ├── upload.html                    # Image upload form
│       ├── document.html                  # Document detail view
│       └── static/                        # Static assets (served by FastAPI)
│           ├── css/
│           │   └── style.css              # Application styling
│           ├── js/
│           │   ├── camera.js              # Camera/file input handling
│           │   ├── upload.js              # Image upload logic
│           │   ├── gallery.js             # Gallery display and filtering
│           │   └── utils.js               # Utility functions
│           └── images/
│               └── icons/                 # UI icons (if needed)
│
├── data/                                  # Data directory
│   ├── database.db                        # SQLite database file (auto-created)
│   ├── uploads/                           # User-uploaded images
│   │   ├── original/                      # Full-resolution images
│   │   ├── thumbnails/                    # 200x200px previews
│   │   └── metadata.json                  # Image metadata index
│   │
│   ├── tree_data/                         # Tree cultural database (JSON/CSV)
│   │   ├── trees_cultural.json            # Comprehensive tree data with cultural context
│   │   ├── tribes_communities.json        # Tribal/cultural community database
│   │   └── ideological_principles.json    # Ideological concepts and meanings
│   │
│   └── exports/                           # User document exports
│       └── *.json                         # Exportable documentation entries
│
├── scripts/                               # Utility scripts
│   ├── init_db.py                         # Initialize SQLite schema
│   ├── load_trees.py                      # Load tree_cultural.json into database
│   ├── seed_data.py                       # Populate sample data for testing
│   └── reset_db.py                        # Reset database (development only)
│
├── tests/                                 # Unit and integration tests
│   ├── __init__.py
│   ├── test_api.py                        # API endpoint tests
│   ├── test_image_service.py              # Image processing tests
│   ├── test_llm_service.py                # LLM integration tests
│   └── conftest.py                        # Pytest fixtures
│
├── docs/                                  # Documentation (provided separately)
│   ├── 00_PROJECT_OVERVIEW.md
│   ├── 01_PROJECT_STRUCTURE.md            # This file
│   ├── 02_DATABASE_SCHEMA.md
│   ├── 03_BACKEND_API.md
│   ├── 04_FRONTEND_INTERFACE.md
│   ├── 05_LLM_INTEGRATION.md
│   ├── 06_INSTALLATION_SETUP.md
│   ├── 07_DEPLOYMENT_LOCAL.md
│   ├── 08_API_REFERENCE.md
│   └── 09_TREE_DATABASE.md
│
├── docker/                                # Docker configuration (optional future)
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
│
└── venv/                                  # Python virtual environment (auto-created)
    ├── bin/                               # Python executables
    ├── lib/                               # Installed packages
    └── pyvenv.cfg                         # Venv configuration
```

---

## 📋 File Descriptions

### Root Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview for humans (installation, usage, architecture) |
| `requirements.txt` | Python package dependencies (FastAPI, Pillow, SQLAlchemy, httpx, python-multipart, ollama) |
| `.env` | Environment variables (OLLAMA_HOST, DATABASE_URL, UPLOAD_DIR, DEBUG) |
| `.gitignore` | Git exclusions (venv/, data/uploads/, *.db, .env) |

### `/app` - FastAPI Application

#### Core Files
- **`main.py`**: FastAPI application initialization, CORS setup, static/template routing, mounted routers
- **`config.py`**: Configuration class with paths, database URL, upload limits, LLM parameters
- **`models.py`**: SQLAlchemy ORM models (User, Tree, TreeCultural, Observation, Document, Reflection)
- **`schemas.py`**: Pydantic request/response models for validation
- **`database.py`**: SQLAlchemy engine, session factory, Base class

#### `/app/routers` - API Endpoints
- **`trees.py`**: Tree catalog endpoints (GET all trees, GET by ID/species, search)
- **`documents.py`**: Document creation (POST image + reflection), retrieval (GET by ID)
- **`observations.py`**: User observation CRUD
- **`reflections.py`**: LLM analysis endpoint (POST reflection → LLM → enriched response)
- **`gallery.py`**: Gallery view (GET all user documents with filtering/sorting)

#### `/app/services` - Business Logic
- **`image_service.py`**: Handles file upload validation, storage, thumbnail generation, EXIF extraction
- **`llm_service.py`**: Ollama HTTP client, prompt construction, response parsing, streaming support
- **`tree_service.py`**: Tree data queries, caching, cultural context retrieval
- **`document_service.py`**: Document CRUD, export to JSON, metadata management
- **`exif_service.py`**: EXIF metadata parsing (optional geolocation, timestamp)

#### `/app/prompts` - LLM Prompt Management
- **`cultural_contextualization.py`**: System prompt for interpreting reflections within cultural context
- **`species_identification.py`**: System prompt for identifying tree species and characteristics
- **`cross_cultural_comparison.py`**: System prompt for comparing how different cultures view same species

#### `/app/templates` - Frontend
- **`base.html`**: Base template with navigation, header, footer
- **`index.html`**: Home/gallery page (display all documents, filter/search)
- **`upload.html`**: Upload form with camera/file input
- **`document.html`**: Individual document view with image, reflection, cultural context, LLM insights

#### `/app/templates/static` - Static Assets
- **`css/style.css`**: Responsive CSS (mobile-first, semantic HTML)
- **`js/camera.js`**: Camera input handling (getUserMedia API)
- **`js/upload.js`**: File upload via FormData API, progress indication
- **`js/gallery.js`**: Gallery filtering, sorting, dynamic rendering
- **`js/utils.js`**: Shared utilities (date formatting, API calls, error handling)

### `/data` - User Data

- **`database.db`**: SQLite database (auto-created by init_db.py)
- **`uploads/original/`**: Full-resolution user images (organized by date: YYYY/MM/DD/)
- **`uploads/thumbnails/`**: 200x200px preview images
- **`tree_data/trees_cultural.json`**: Comprehensive tree database with cultural significance
- **`exports/`**: JSON exports of completed documents (user-shareable format)

### `/scripts` - Utilities

| Script | Purpose |
|--------|---------|
| `init_db.py` | Create SQLite schema from SQLAlchemy models |
| `load_trees.py` | Populate tree_cultural.json into database |
| `seed_data.py` | Load sample data for development/testing |
| `reset_db.py` | Drop and recreate database (dev only) |

### `/tests` - Test Suite

- **`test_api.py`**: Test API endpoints (upload, retrieve, list)
- **`test_image_service.py`**: Test image validation, storage, thumbnail generation
- **`test_llm_service.py`**: Test Ollama integration (mock calls)
- **`conftest.py`**: Pytest fixtures (temporary uploads dir, test database, test client)

### `/docs` - Documentation

All documentation files provided for Claude Code processing (numbered 00-09).

---

## 🎯 Key Conventions

### File Naming
- **Python**: Snake_case (e.g., `image_service.py`)
- **Directories**: Lowercase plural (e.g., `/routers`, `/services`)
- **Templates**: HTML files in `/templates`, CSS in `/templates/static/css`
- **Data**: JSON for structured data, SQLite for relational

### Import Structure
```python
# Within app/routers/trees.py
from fastapi import APIRouter
from app.services.tree_service import get_all_trees
from app.schemas import TreeResponse

# Within app/services/image_service.py
from pathlib import Path
from PIL import Image
from app.config import Config
```

### URL Routes
- **API endpoints**: `/api/...` prefix (REST)
- **Templates**: `/` prefix (web UI)
- **Static files**: `/static/...` prefix (CSS, JS, images)

### Database Tables (SQLite)
```sql
users → observations (1:N)
users → documents (1:N)
trees_cultural → documents (1:N)
documents → reflections (1:1)
observations → reflections (1:N)
```

---

## 📦 Virtual Environment Setup

After cloning/creating the project:

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create data directory structure
mkdir -p data/uploads/original data/uploads/thumbnails
mkdir -p data/tree_data data/exports

# Initialize database
python scripts/init_db.py

# Load tree data
python scripts/load_trees.py
```

---

## 🔄 Data Flow in Directory Structure

```
User uploads image (browser)
    ↓
/app/routers/documents.py → /app/services/image_service.py
    ↓
Save to data/uploads/original/ + create thumbnail in data/uploads/thumbnails/
    ↓
Store metadata in database.db (SQLite)
    ↓
/app/services/llm_service.py → calls Ollama (local server)
    ↓
Save LLM response to database
    ↓
/app/routers/gallery.py retrieves from database
    ↓
Render in /app/templates/document.html + /app/templates/static/js/gallery.js
    ↓
User sees enriched document with image, reflection, cultural context, LLM insights
```

---

## 🚀 Deployment Note

For **local deployment** on single machine:
- All files stay in project directory
- SQLite database persists in `data/database.db`
- Images stored locally in `data/uploads/`
- Ollama runs as separate process (started before FastAPI app)
- FastAPI app serves web UI at `http://localhost:8000`
- Optional: Use nginx for static file serving (production optimization)

---

## 📝 File Creation Order for Claude Code

1. Create all directories: `/app`, `/app/routers`, `/app/services`, `/app/templates`, `/app/templates/static/css`, `/app/templates/static/js`, `/data`, `/data/uploads`, `/data/tree_data`, `/scripts`, `/tests`
2. Create `/app/__init__.py`, `/app/routers/__init__.py`, etc. (empty init files)
3. Create core files: `main.py`, `config.py`, `models.py`, `schemas.py`, `database.py`
4. Create routers: `trees.py`, `documents.py`, `observations.py`, `reflections.py`, `gallery.py`
5. Create services: `image_service.py`, `llm_service.py`, `tree_service.py`, `document_service.py`, `exif_service.py`
6. Create prompts: `cultural_contextualization.py`, etc.
7. Create templates: `base.html`, `index.html`, `upload.html`, `document.html`
8. Create static files: `style.css`, `camera.js`, `upload.js`, `gallery.js`, `utils.js`
9. Create scripts: `init_db.py`, `load_trees.py`, `seed_data.py`, `reset_db.py`
10. Create `requirements.txt`, `.env`, `.gitignore`, `README.md`

---

**Status**: Ready for generation by Claude Code
**Total Files**: ~35 Python files + HTML templates + CSS/JS + JSON data files
**Total LOC Expected**: ~2,500 lines (backend) + ~1,500 lines (frontend) = 4,000 LOC production code