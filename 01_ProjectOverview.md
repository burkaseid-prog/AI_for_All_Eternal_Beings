# PROJECT OVERVIEW: Tree Wisdom - A Geospatial & Cultural Documentation System

## 🌳 Core Vision

**Tree Wisdom** is an integrated system that enables users to:
- **Capture images** of trees and vegetation in their environment
- **Document reflections** on the cultural, ideological, and spiritual significance of tree species
- **Access a knowledge graph** of trees from diverse tribal and global communities
- **Understand connections** between human societies, trees, and environmental stewardship

The system bridges **geospatial data**, **cultural knowledge**, **LLM-powered insights**, and **agent-based documentation** to create a living archive of human-tree relationships across civilizations.

---

## 🎯 Core Features

### 1. **Image Capture & Processing**
- User uploads/captures tree images through responsive web interface
- Computer vision (via LLM) analyzes images to identify species, location, and characteristics
- Images stored locally with metadata (location, timestamp, user reflections)

### 2. **Cultural Knowledge Integration**
- Database of tree species linked to tribal/global communities
- Each tree record contains:
  - **Botanical Data**: Species, genus, characteristics
  - **Cultural Significance**: Associated communities, worship practices, ideological meaning
  - **Historical Context**: Role in societies, rituals, economic/medicinal importance
  - **Environmental Role**: Ecosystem services, conservation status

### 3. **LLM-Powered Insights**
- Ollama (local LLM) generates:
  - **Cultural interpretations** of user reflections within broader tribal/global context
  - **Educational narratives** connecting individual observations to universal patterns
  - **Cross-cultural comparisons** showing how different societies relate to same tree species
  - **Semantic enrichment** of user thoughts with relevant cultural knowledge

### 4. **User Documentation System**
- Users record thoughts/reflections upon viewing tree
- LLM contextualizes reflections with cultural data
- System creates shareable documentation entries combining:
  - Image
  - User reflection
  - Species data
  - Cultural significance
  - LLM-generated insights

### 5. **Graph-Based Navigation**
- Neo4j integration (optional future phase) for:
  - Species → Cultural Communities → Ideological Principles
  - User → Observations → Trees → Cultural Contexts
  - Cross-tree comparisons across geographies

---

## 🏗️ Technical Architecture

### Frontend
- **Single-Page Application** (vanilla JS + HTML5)
- **Camera/File Upload API** for image capture
- **Real-time image preview** and metadata entry
- **Responsive design** for desktop and mobile
- **Framework**: Jinja2 templates served by FastAPI

### Backend
- **FastAPI** (Python 3.11+): RESTful API for all operations
- **Image Processing**: Pillow for image storage and thumbnails
- **File Storage**: Local filesystem with organized directory structure
- **Database**: SQLite for relational data (trees, users, observations)

### AI/LLM
- **Ollama**: Local LLM server (no external API costs/latency)
- **Model**: Llama3.2 (3B or 7B, depending on hardware)
- **Integration**: FastAPI calls Ollama for text generation
- **Prompt Engineering**: System prompts designed for cultural contextualization

### Data Storage
- **SQLite Database**: Tree metadata, users, observations, reflections
- **File System**: Original images, thumbnails, processed media
- **JSON Exports**: Documentation entries as portable records

---

## 📊 Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│ USER CAPTURES TREE IMAGE & WRITES REFLECTION               │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND: Upload image + reflection text (HTTP POST)        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ BACKEND: FastAPI /document endpoint                         │
│  - Validate image (MIME type, size)                         │
│  - Extract EXIF metadata (location, timestamp)              │
│  - Save image to filesystem                                 │
│  - Store metadata in SQLite                                 │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ LLM PROCESSING: Ollama generates insights                   │
│  - Query LLM with: tree species + reflection + cultural DB  │
│  - Generate contextualized narrative                        │
│  - Extract cultural links and principles                    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ STORE COMPLETE DOCUMENTATION                                │
│  - Save LLM-generated insights to database                  │
│  - Create JSON export (portable format)                     │
│  - Return enriched entry to frontend                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ DISPLAY IN GALLERY                                          │
│  - Show image + reflection + cultural context + insights    │
│  - Enable filtering by tree species, culture, principles    │
│  - Allow sharing and export                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack (February 2026)

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Runtime** | Python | 3.11+ | Core runtime environment |
| **Web Framework** | FastAPI | 0.104+ | REST API, routing, validation |
| **Image Processing** | Pillow | 10.0+ | Image handling, resizing, thumbnails |
| **Database ORM** | SQLAlchemy | 2.0+ | Database abstraction, migrations |
| **Database** | SQLite | 3.40+ | Local relational database |
| **LLM Server** | Ollama | 0.2.0+ | Local LLM inference |
| **LLM Model** | Llama3.2 | 3B/7B | Text generation and understanding |
| **HTTP Client** | httpx | 0.25+ | Async HTTP calls to Ollama |
| **Async Runtime** | asyncio | Built-in | Concurrent request handling |
| **Server** | Uvicorn | 0.24+ | ASGI server for FastAPI |
| **Frontend** | Vanilla JS | HTML5 | No framework overhead |
| **Styling** | CSS3 | Custom | Responsive, semantic design |
| **File Upload** | Multipart Form Data | RFC 7578 | Image submission protocol |

---

## 🔐 Security Considerations

1. **Image Validation**: MIME type checking, file size limits, extension verification
2. **File Storage**: Uploaded files stored outside web root, served through FastAPI endpoint
3. **EXIF Data**: Optional extraction (with user consent) for location/timestamp
4. **Input Sanitization**: SQL injection prevention via SQLAlchemy ORM
5. **Rate Limiting**: Optional API rate limiting per IP/user
6. **CORS**: Same-origin by default (no cross-origin requests)

---

## 📦 Deliverables

All documentation is provided as Markdown files designed for **Claude Code** consumption:

1. ✅ **00_PROJECT_OVERVIEW.md** (this file)
2. ✅ **01_PROJECT_STRUCTURE.md** - Directory layout
3. ✅ **02_DATABASE_SCHEMA.md** - SQLite schema definition
4. ✅ **03_BACKEND_API.md** - FastAPI implementation
5. ✅ **04_FRONTEND_INTERFACE.md** - HTML/CSS/JS interface
6. ✅ **05_LLM_INTEGRATION.md** - Ollama configuration
7. ✅ **06_INSTALLATION_SETUP.md** - Dependency installation
8. ✅ **07_DEPLOYMENT_LOCAL.md** - Launch and running instructions
9. ✅ **08_API_REFERENCE.md** - Endpoint documentation
10. ✅ **09_TREE_DATABASE.md** - Cultural tree data

---

## 🚀 Deployment Target

**Environment**: Local computer (single-machine)
**OS**: Linux, macOS, Windows (WSL2)
**Hardware Requirements**:
- CPU: Quad-core recommended (Ollama inference CPU-intensive)
- RAM: 16GB minimum (8GB for Llama3.2 3B model)
- Storage: 10GB minimum (model + database + images)

**Access**: `http://localhost:8000`

---

## 📈 Future Enhancements

1. **Neo4j Graph Integration**: Build knowledge graph of trees ↔ cultures ↔ principles
2. **Geospatial Mapping**: Show documented trees on interactive map (Folium/Mapbox)
3. **Agent-Based Modeling**: ABM simulations of human-tree relationships
4. **Community Sharing**: Multi-user support, cloud backend
5. **Advanced Vision**: Species classification via fine-tuned ML model
6. **Multilingual Support**: LLM-generated translations of cultural narratives
7. **API Exposure**: Public API for research/educational integration

---

## 📖 How to Use These Documents

This documentation is written for **Claude Code** to consume sequentially:

1. **Start** with this file (PROJECT_OVERVIEW) for context
2. **Read** PROJECT_STRUCTURE to understand directory layout
3. **Review** DATABASE_SCHEMA for data models
4. **Study** BACKEND_API for API endpoint implementations
5. **Check** FRONTEND_INTERFACE for UI requirements
6. **Understand** LLM_INTEGRATION for Ollama setup
7. **Follow** INSTALLATION_SETUP for environment preparation
8. **Execute** DEPLOYMENT_LOCAL to run the application
9. **Reference** API_REFERENCE for endpoint details
10. **Load** TREE_DATABASE with initial cultural data

**Result**: A fully functional, locally-deployed Tree Wisdom application requiring zero manual coding.

---

## 🤝 Integration Notes

- All files use **standard Python/FastAPI/SQLite** conventions
- No exotic dependencies (production-tested packages only)
- Cross-platform compatible (Windows/macOS/Linux via Python)
- Extensible architecture for Neo4j, advanced vision, cloud deployment
- Documentation includes package names, version numbers, and import statements

---

**Status**: Ready for Claude Code Generation
**Last Updated**: February 2026
**Compatibility**: FastAPI 0.104+, Python 3.11+, Ollama 0.2.0+