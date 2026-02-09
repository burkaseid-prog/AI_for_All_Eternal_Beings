# BACKEND API: FastAPI Implementation Guide

## 🚀 FastAPI Application Setup

### `/app/main.py` - Core Application

```python
"""
FastAPI application for Tree Wisdom system.
Serves both REST API and web UI via Jinja2 templates.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pathlib import Path

from app.config import Config
from app.database import engine, Base
from app.routers import trees, documents, observations, reflections, gallery

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app instance
app = FastAPI(
    title="Tree Wisdom API",
    description="Document tree observations with cultural and ideological significance",
    version="1.0.0",
    debug=Config.DEBUG
)

# CORS Middleware - allow same-origin requests only for local deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Trusted Host Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

# Include routers
app.include_router(trees.router, prefix="/api", tags=["Trees"])
app.include_router(documents.router, prefix="/api", tags=["Documents"])
app.include_router(observations.router, prefix="/api", tags=["Observations"])
app.include_router(reflections.router, prefix="/api", tags=["Reflections"])
app.include_router(gallery.router, prefix="/api", tags=["Gallery"])

# Mount static files (CSS, JS, images)
static_path = Path(__file__).parent / "templates" / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Tree Wisdom"}

# Root endpoint - serve home page
@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    html_path = Path(__file__).parent / "templates" / "index.html"
    return FileResponse(html_path, media_type="text/html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=Config.DEBUG)
```

---

## 🛣️ Router Modules

### 1. `/app/routers/trees.py` - Tree Database Endpoints

```python
"""
Trees endpoints: Browse cultural tree database.
GET /api/trees - List all trees
GET /api/trees/{tree_id} - Get specific tree with cultural data
GET /api/trees/search - Search by common name, scientific name, cultural principle
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TreeCultural
from app.schemas import TreeResponse
from app.services.tree_service import TreeService

router = APIRouter(prefix="/trees", tags=["Trees"])
tree_service = TreeService()

@router.get("", response_model=list[TreeResponse])
async def list_trees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all trees in database with pagination.
    """
    trees = db.query(TreeCultural).offset(skip).limit(limit).all()
    return trees

@router.get("/{tree_id}", response_model=TreeResponse)
async def get_tree(tree_id: int, db: Session = Depends(get_db)):
    """
    Get specific tree by ID with full cultural data.
    """
    tree = db.query(TreeCultural).filter(TreeCultural.id == tree_id).first()
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    return tree

@router.get("/search/cultural", response_model=list[TreeResponse])
async def search_cultural(
    principle: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    """
    Search trees by ideological principle (e.g., 'Enlightenment', 'Cosmic Axis').
    Searches through JSON ideological_principles field.
    """
    results = tree_service.search_by_principle(db, principle)
    return results

@router.get("/search/tribe", response_model=list[TreeResponse])
async def search_tribe(
    tribe_name: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    """
    Search trees associated with specific tribe/community.
    """
    results = tree_service.search_by_tribe(db, tribe_name)
    return results
```

---

### 2. `/app/routers/documents.py` - Document Creation & Retrieval

```python
"""
Documents endpoints: Image upload + reflection → documentation entry
POST /api/documents - Create new document (image + reflection)
GET /api/documents/{doc_id} - Get document with image and reflection
DELETE /api/documents/{doc_id} - Delete document
"""

from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Document, User
from app.schemas import DocumentCreateRequest, DocumentResponse
from app.services.image_service import ImageService
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])
image_service = ImageService()
document_service = DocumentService()

@router.post("", response_model=DocumentResponse, status_code=201)
async def create_document(
    image: UploadFile = File(..., description="Tree image (JPG/PNG, max 10MB)"),
    reflection: str = Form(..., description="User's reflection about the tree"),
    identified_species: str = Form(None, description="Tree species (optional)"),
    title: str = Form(None, description="Document title (optional)"),
    db: Session = Depends(get_db)
):
    """
    Upload tree image + write reflection to create documentation entry.
    
    Process:
    1. Validate image file (MIME type, size, dimensions)
    2. Save image to filesystem (original + thumbnail)
    3. Extract EXIF metadata (location, timestamp)
    4. Create Document record in database
    5. Trigger LLM reflection processing (async)
    6. Return created document
    """
    # Validate and save image
    image_data = await image_service.process_upload(image)
    
    # Create document
    doc = document_service.create_document(
        db=db,
        image_path=image_data['path'],
        thumbnail_path=image_data['thumbnail_path'],
        user_reflection=reflection,
        identified_species=identified_species,
        title=title or f"Tree Observation - {datetime.now().strftime('%Y-%m-%d')}",
        exif_data=image_data.get('exif')
    )
    
    return DocumentResponse.from_orm(doc)

@router.get("/{doc_id}", response_model=DocumentResponse)
async def get_document(doc_id: int, db: Session = Depends(get_db)):
    """
    Get document with image, reflection, and LLM-generated insights.
    """
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """
    Delete document and associated files.
    """
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete image files
    image_service.delete_files(doc.image_path, doc.thumbnail_path)
    
    # Delete from database
    db.delete(doc)
    db.commit()
    
    return {"message": "Document deleted"}
```

---

### 3. `/app/routers/reflections.py` - LLM-Powered Analysis

```python
"""
Reflections endpoints: LLM processing of observations + cultural contextualization
POST /api/reflections/analyze - Generate insights for a document
GET /api/reflections/{reflection_id} - Get reflection details
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Document, Reflection
from app.schemas import ReflectionAnalysisRequest, ReflectionResponse
from app.services.llm_service import LLMService
from app.services.document_service import DocumentService

router = APIRouter(prefix="/reflections", tags=["Reflections"])
llm_service = LLMService()
doc_service = DocumentService()

@router.post("/analyze", response_model=ReflectionResponse, status_code=201)
async def analyze_reflection(
    request: ReflectionAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Analyze user reflection against cultural tree database.
    
    LLM Processing:
    1. Query document with image path and user reflection
    2. Identify tree species from image + user text
    3. Retrieve cultural data for identified species
    4. Generate cultural interpretation (how different cultures view this tree)
    5. Extract ideological principles and tribal associations
    6. Generate cross-cultural comparison narrative
    7. Store all insights in Reflection table
    
    Returns enriched document with LLM-generated cultural context.
    """
    # Fetch document
    doc = db.query(Document).filter(Document.id == request.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check if reflection already exists
    existing = db.query(Reflection).filter(Reflection.document_id == doc.id).first()
    if existing:
        return existing
    
    # Process with LLM
    reflection_data = await llm_service.generate_reflection(
        user_reflection=doc.user_reflection,
        identified_species=doc.identified_species,
        tree_data=doc.tree,  # TreeCultural object if linked
        db=db
    )
    
    # Create Reflection record
    reflection = Reflection(
        document_id=doc.id,
        cultural_interpretation=reflection_data['cultural_interpretation'],
        ideological_connections=reflection_data['ideological_connections'],
        cross_cultural_comparison=reflection_data['cross_cultural_comparison'],
        educational_narrative=reflection_data['educational_narrative'],
        linked_tribes=reflection_data['linked_tribes'],
        linked_principles=reflection_data['linked_principles'],
        llm_model_used="llama3.2:7b",
        llm_prompt_version="v1.0",
        processing_time_ms=reflection_data['processing_time_ms']
    )
    
    db.add(reflection)
    db.commit()
    
    return reflection

@router.get("/{reflection_id}", response_model=ReflectionResponse)
async def get_reflection(reflection_id: int, db: Session = Depends(get_db)):
    """
    Get reflection with LLM-generated insights.
    """
    reflection = db.query(Reflection).filter(Reflection.id == reflection_id).first()
    if not reflection:
        raise HTTPException(status_code=404, detail="Reflection not found")
    return reflection
```

---

### 4. `/app/routers/gallery.py` - User Document Gallery

```python
"""
Gallery endpoints: View all user's documented trees
GET /api/gallery - List all documents (with pagination, filtering, sorting)
GET /api/gallery/export - Export all documents as JSON
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Document
from app.schemas import DocumentResponse

router = APIRouter(prefix="/gallery", tags=["Gallery"])

@router.get("", response_model=list[DocumentResponse])
async def list_gallery(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    species: str = Query(None, description="Filter by tree species"),
    sort_by: str = Query("created_at", enum=["created_at", "updated_at", "title"]),
    order: str = Query("desc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    """
    Get all documents with optional filtering and sorting.
    """
    query = db.query(Document)
    
    if species:
        query = query.filter(Document.identified_species.ilike(f"%{species}%"))
    
    # Sort
    order_col = getattr(Document, sort_by)
    if order == "asc":
        query = query.order_by(order_col.asc())
    else:
        query = query.order_by(order_col.desc())
    
    documents = query.offset(skip).limit(limit).all()
    return documents

@router.get("/export/json")
async def export_gallery(db: Session = Depends(get_db)):
    """
    Export all documents as JSON (including reflections and cultural data).
    """
    from app.services.document_service import DocumentService
    export_data = DocumentService().export_all_json(db)
    
    from fastapi.responses import FileResponse
    from datetime import datetime
    
    filename = f"tree_wisdom_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Save and return file
    return FileResponse(
        path=f"data/exports/{filename}",
        filename=filename,
        media_type="application/json"
    )
```

---

## 🔐 Services Layer

### `/app/services/image_service.py`

```python
"""
Image upload, validation, storage, and EXIF extraction.
"""

from fastapi import UploadFile, HTTPException
from PIL import Image
from pathlib import Path
import hashlib
from datetime import datetime

class ImageService:
    UPLOAD_DIR = Path("data/uploads/original")
    THUMB_DIR = Path("data/uploads/thumbnails")
    ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}
    MAX_SIZE = 10 * 1024 * 1024  # 10MB
    THUMB_SIZE = (200, 200)
    
    async def process_upload(self, file: UploadFile):
        """
        1. Validate MIME type
        2. Validate file size
        3. Generate unique filename
        4. Save original image
        5. Generate thumbnail
        6. Extract EXIF metadata
        7. Return file paths and metadata
        """
        # Validate MIME type
        if file.content_type not in self.ALLOWED_MIME:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {self.ALLOWED_MIME}"
            )
        
        # Read file content
        content = await file.read()
        
        # Validate size
        if len(content) > self.MAX_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum: {self.MAX_SIZE / 1024 / 1024}MB"
            )
        
        # Generate filename (hash + timestamp)
        file_hash = hashlib.md5(content).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{file_hash}_{timestamp}.jpg"
        
        # Save original
        file_path = self.UPLOAD_DIR / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)
        
        # Generate thumbnail
        img = Image.open(file_path)
        img.thumbnail(self.THUMB_SIZE, Image.Resampling.LANCZOS)
        thumb_path = self.THUMB_DIR / f"thumb_{filename}"
        thumb_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(thumb_path, quality=85)
        
        # Extract EXIF (optional geolocation + timestamp)
        exif_data = self._extract_exif(file_path)
        
        return {
            "path": str(file_path),
            "thumbnail_path": str(thumb_path),
            "filename": filename,
            "size": len(content),
            "mime_type": file.content_type,
            "exif": exif_data
        }
    
    def _extract_exif(self, image_path):
        """Extract EXIF data including GPS coordinates."""
        try:
            from PIL.Image import Exif
            img = Image.open(image_path)
            exif = img.getexif()
            
            exif_dict = {}
            # Parse EXIF data (convert to JSON-serializable format)
            for key, value in exif.items():
                try:
                    exif_dict[str(key)] = str(value)
                except:
                    pass
            
            return exif_dict
        except:
            return None
    
    def delete_files(self, original_path, thumbnail_path):
        """Delete image files."""
        Path(original_path).unlink(missing_ok=True)
        Path(thumbnail_path).unlink(missing_ok=True)
```

---

### `/app/services/llm_service.py`

```python
"""
Ollama LLM integration for cultural insight generation.
"""

import httpx
import json
import time
from app.config import Config
from app.prompts import cultural_contextualization

class LLMService:
    def __init__(self):
        self.ollama_host = Config.OLLAMA_HOST
        self.model = Config.LLM_MODEL
        self.client = httpx.Client(timeout=120.0)
    
    async def generate_reflection(self, user_reflection, identified_species, tree_data, db):
        """
        Generate LLM-powered cultural insights for user reflection.
        """
        start_time = time.time()
        
        # Construct prompt
        prompt = self._construct_prompt(
            user_reflection=user_reflection,
            species=identified_species,
            tree_data=tree_data
        )
        
        # Call Ollama
        response = await self._call_ollama(prompt)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Parse response
        parsed = self._parse_response(response)
        parsed['processing_time_ms'] = processing_time
        
        return parsed
    
    def _construct_prompt(self, user_reflection, species, tree_data):
        """
        Build system prompt with cultural context and user input.
        """
        tree_context = ""
        if tree_data:
            tree_context = f"""
Tree Species: {tree_data.common_name} ({tree_data.scientific_name})
Cultural Significance: {tree_data.cultural_significance}
Tribal Associations: {tree_data.tribal_associations}
Ideological Principles: {tree_data.ideological_principles}
"""
        
        prompt = f"""{cultural_contextualization.SYSTEM_PROMPT}

User Reflection: {user_reflection}

Identified Species: {species or 'Unknown'}

{tree_context}

Generate:
1. Cultural interpretation of user's observation within global context
2. Connections to ideological principles (extract as JSON array)
3. Cross-cultural comparison (how other cultures view this tree)
4. Educational narrative connecting personal observation to universal patterns

Format response as JSON with keys: cultural_interpretation, ideological_connections, cross_cultural_comparison, educational_narrative, linked_tribes, linked_principles"""
        
        return prompt
    
    async def _call_ollama(self, prompt):
        """Call Ollama API endpoint."""
        url = f"{self.ollama_host}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7,
            "num_predict": 1500
        }
        
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()['response']
    
    def _parse_response(self, response_text):
        """Extract JSON from LLM response."""
        try:
            # LLM response should contain JSON block
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_str = response_text[start:end]
            return json.loads(json_str)
        except:
            # Fallback if JSON parsing fails
            return {
                "cultural_interpretation": response_text,
                "ideological_connections": json.dumps([]),
                "cross_cultural_comparison": "",
                "educational_narrative": "",
                "linked_tribes": json.dumps([]),
                "linked_principles": json.dumps([])
            }
```

---

## 📦 Requirements.txt

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pillow==10.1.0
httpx==0.25.2
pydantic==2.5.0
python-multipart==0.0.6
python-dotenv==1.0.0
ollama==0.1.33
