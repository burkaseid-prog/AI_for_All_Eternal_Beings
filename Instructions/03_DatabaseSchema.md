# DATABASE SCHEMA: SQLite Design with Cultural Tree Data

## 🗄️ Overview

The Tree Wisdom system uses **SQLite** for relational data storage with a schema designed to capture:
- User observations and reflections about trees
- Comprehensive tree species database linked to cultural communities
- Cultural significance, ideological meanings, and tribal associations
- Generated LLM insights connecting individual observations to cultural contexts

---

## 📊 SQLAlchemy ORM Models

All models defined in `/app/models.py` using SQLAlchemy 2.0+ with async support.

### 1. **User Model**

```python
# users table
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    observations: Mapped[List["Observation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    documents: Mapped[List["Document"]] = relationship(back_populates="user", cascade="all, delete-orphan")
```

**Purpose**: Track users (for future multi-user support, currently single user per instance)
**Columns**:
- `id` (int, PK): Unique identifier
- `username` (str, unique): User login name
- `email` (str, unique): Contact email
- `created_at` (datetime): Account creation timestamp

---

### 2. **TreeCultural Model**

```python
# trees_cultural table - Comprehensive tree database with cultural context
class TreeCultural(Base):
    __tablename__ = "trees_cultural"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    common_name: Mapped[str] = mapped_column(String(150), index=True)
    scientific_name: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    genus: Mapped[str] = mapped_column(String(100))
    family: Mapped[str] = mapped_column(String(100))
    
    # Cultural Data (JSON for flexibility)
    cultural_significance: Mapped[str] = mapped_column(Text)  # JSON string of cultural info
    tribal_associations: Mapped[str] = mapped_column(Text)   # JSON: {tribe: [associations]}
    ideological_principles: Mapped[str] = mapped_column(Text) # JSON: [principles]
    historical_context: Mapped[str] = mapped_column(Text)    # Historical role in societies
    worship_practices: Mapped[str] = mapped_column(Text)     # JSON: [practices]
    medicinal_uses: Mapped[str] = mapped_column(Text)        # JSON: {use: description}
    ecological_role: Mapped[str] = mapped_column(Text)       # Ecosystem services
    
    # Botanical Data
    native_regions: Mapped[str] = mapped_column(Text)        # JSON: [regions]
    height_range: Mapped[str] = mapped_column(String(50))    # e.g., "20-30m"
    lifespan_years: Mapped[int] = mapped_column(nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents: Mapped[List["Document"]] = relationship(back_populates="tree", cascade="all, delete-orphan")
```

**Purpose**: Core tree species database with cultural and botanical data
**Key Columns**:
- `common_name`, `scientific_name`: Species identification
- `genus`, `family`: Botanical classification
- `cultural_significance`: JSON blob with detailed cultural meaning
- `tribal_associations`: JSON mapping tribes → cultural meanings
- `ideological_principles`: JSON list of philosophical/spiritual concepts
- `worship_practices`: JSON array of ritual uses
- `medicinal_uses`: JSON mapping use cases → descriptions
- `ecological_role`: Ecosystem services and importance

**Example JSON Structure**:
```json
{
  "tribal_associations": {
    "Aboriginal Australian": "Sacred tree of interconnection, songlines",
    "Hindu": "Bodhi tree - enlightenment symbol",
    "Norse": "Yggdrasil - world tree, cosmic center"
  },
  "ideological_principles": [
    "Divine Connection",
    "Cosmic Axis",
    "Interconnectedness",
    "Regeneration"
  ]
}
```

---

### 3. **Observation Model**

```python
# observations table
class Observation(Base):
    __tablename__ = "observations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tree_id: Mapped[int] = mapped_column(ForeignKey("trees_cultural.id"), nullable=True)
    
    # Observation Data
    observation_text: Mapped[str] = mapped_column(Text)      # User's raw observation
    reflection: Mapped[str] = mapped_column(Text, nullable=True)  # User's thoughts/feelings
    
    # Metadata
    latitude: Mapped[float] = mapped_column(nullable=True)    # EXIF or manual location
    longitude: Mapped[float] = mapped_column(nullable=True)
    location_description: Mapped[str] = mapped_column(String(255), nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="observations")
    documents: Mapped[List["Document"]] = relationship(back_populates="observation")
    reflections: Mapped[List["Reflection"]] = relationship(back_populates="observation", cascade="all, delete-orphan")
```

**Purpose**: Track user observations about trees in their environment
**Columns**:
- `observation_text`: Detailed description of what user saw
- `reflection`: User's thoughts, feelings, cultural connections
- `latitude`, `longitude`: GPS coordinates (from EXIF or manual entry)
- `observed_at`: When the observation occurred

---

### 4. **Document Model**

```python
# documents table
class Document(Base):
    __tablename__ = "documents"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    observation_id: Mapped[int] = mapped_column(ForeignKey("observations.id"), nullable=True)
    tree_id: Mapped[int] = mapped_column(ForeignKey("trees_cultural.id"), nullable=True)
    
    # Image Data
    image_filename: Mapped[str] = mapped_column(String(255), unique=True)  # original.jpg
    thumbnail_filename: Mapped[str] = mapped_column(String(255), nullable=True)  # thumb.jpg
    image_path: Mapped[str] = mapped_column(String(500))      # Full path to original
    thumbnail_path: Mapped[str] = mapped_column(String(500))  # Full path to thumbnail
    image_size_bytes: Mapped[int] = mapped_column()
    image_mime_type: Mapped[str] = mapped_column(String(50))
    
    # Document Content
    title: Mapped[str] = mapped_column(String(200))
    user_reflection: Mapped[str] = mapped_column(Text)        # User's written reflection
    identified_species: Mapped[str] = mapped_column(String(150), nullable=True)
    
    # Metadata
    exif_data: Mapped[str] = mapped_column(Text, nullable=True)  # JSON: {key: value}
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="documents")
    observation: Mapped["Observation"] = relationship(back_populates="documents")
    tree: Mapped["TreeCultural"] = relationship(back_populates="documents")
    reflection: Mapped["Reflection"] = relationship(back_populates="document", uselist=False, cascade="all, delete-orphan")
```

**Purpose**: Complete documentation entry combining image + metadata + reflection
**Columns**:
- `image_filename`, `image_path`: Stored image file
- `user_reflection`: User's written thoughts about the tree
- `identified_species`: Tree species (auto-identified or user-provided)
- `exif_data`: JSON extraction from image metadata

---

### 5. **Reflection Model**

```python
# reflections table
class Reflection(Base):
    __tablename__ = "reflections"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    observation_id: Mapped[int] = mapped_column(ForeignKey("observations.id"), nullable=True)
    
    # LLM-Generated Content
    cultural_interpretation: Mapped[str] = mapped_column(Text)    # LLM output: cultural context
    ideological_connections: Mapped[str] = mapped_column(Text)   # JSON: linked principles
    cross_cultural_comparison: Mapped[str] = mapped_column(Text) # LLM: how other cultures view same tree
    educational_narrative: Mapped[str] = mapped_column(Text)     # LLM: educational summary
    
    # Linked Cultural Data
    linked_tribes: Mapped[str] = mapped_column(Text)             # JSON: [tribe names]
    linked_principles: Mapped[str] = mapped_column(Text)         # JSON: [ideological principles]
    
    # Processing Metadata
    llm_model_used: Mapped[str] = mapped_column(String(100))     # e.g., "llama3.2:7b"
    llm_prompt_version: Mapped[str] = mapped_column(String(50))  # Prompt template version
    processing_time_ms: Mapped[int] = mapped_column()            # LLM inference time
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    document: Mapped["Document"] = relationship(back_populates="reflection")
    observation: Mapped["Observation"] = relationship(back_populates="reflections")
```

**Purpose**: Store LLM-generated insights connecting user observations to cultural knowledge
**Columns**:
- `cultural_interpretation`: LLM's contextualization of user's reflection within cultural frameworks
- `ideological_connections`: JSON list linking user's observation to cultural principles
- `cross_cultural_comparison`: LLM analysis of how different cultures relate to this tree species
- `linked_tribes`, `linked_principles`: References to cultural database

---

## 📈 Entity Relationship Diagram

```
┌──────────────┐
│    Users     │
│──────────────│
│ id (PK)      │
│ username     │
│ email        │
└──────┬───────┘
       │
       ├──1:N──────────────────┐
       │                        │
       │                   ┌────────────────────┐
       │                   │  Observations      │
       │                   │────────────────────│
       │                   │ id (PK)            │
       │                   │ user_id (FK)       │
       │                   │ tree_id (FK)   ────────┐
       │                   │ observation_text   │    │
       │                   │ reflection         │    │
       │                   │ latitude/longitude │    │
       │                   └────────────────────┘    │
       │                                             │
       │                   ┌────────────────────┐    │
       └──1:N─────────────→│  Documents         │    │
                           │────────────────────│    │
                           │ id (PK)            │    │
                           │ user_id (FK)       │    │
                           │ observation_id (FK)│    │
                           │ tree_id (FK)   ────────┘
                           │ image_filename     │
                           │ user_reflection    │
                           │ exif_data          │
                           └────────┬───────────┘
                                    │
                           1:1       │
                           ┌─────────▼──────────────┐
                           │  Reflections           │
                           │────────────────────────│
                           │ id (PK)                │
                           │ document_id (FK)       │
                           │ cultural_interpretation│
                           │ ideological_connections│
                           │ cross_cultural_compare │
                           │ linked_tribes (JSON)   │
                           │ linked_principles(JSON)│
                           └────────────────────────┘
                                    │
                                    │ references
                                    ↓
                           ┌────────────────────┐
                           │ TreesCultural      │
                           │────────────────────│
                           │ id (PK)            │
                           │ common_name        │
                           │ scientific_name    │
                           │ tribal_associations│ ← JSON
                           │ ideological_prin.  │ ← JSON
                           │ worship_practices  │ ← JSON
                           │ medicinal_uses     │ ← JSON
                           │ ecological_role    │
                           └────────────────────┘
```

---

## 🔧 SQL DDL (Generated from SQLAlchemy)

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ix_users_username ON users(username);
CREATE INDEX ix_users_email ON users(email);

-- Trees with cultural data
CREATE TABLE trees_cultural (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    common_name VARCHAR(150) NOT NULL,
    scientific_name VARCHAR(150) UNIQUE NOT NULL,
    genus VARCHAR(100) NOT NULL,
    family VARCHAR(100) NOT NULL,
    cultural_significance TEXT NOT NULL,
    tribal_associations TEXT NOT NULL,
    ideological_principles TEXT NOT NULL,
    historical_context TEXT NOT NULL,
    worship_practices TEXT NOT NULL,
    medicinal_uses TEXT NOT NULL,
    ecological_role TEXT NOT NULL,
    native_regions TEXT NOT NULL,
    height_range VARCHAR(50),
    lifespan_years INTEGER,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ix_trees_cultural_common_name ON trees_cultural(common_name);
CREATE INDEX ix_trees_cultural_scientific_name ON trees_cultural(scientific_name);

-- User observations
CREATE TABLE observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    tree_id INTEGER REFERENCES trees_cultural(id),
    observation_text TEXT NOT NULL,
    reflection TEXT,
    latitude FLOAT,
    longitude FLOAT,
    location_description VARCHAR(255),
    observed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Documents (image + metadata + reflection)
CREATE TABLE documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    observation_id INTEGER REFERENCES observations(id),
    tree_id INTEGER REFERENCES trees_cultural(id),
    image_filename VARCHAR(255) UNIQUE NOT NULL,
    thumbnail_filename VARCHAR(255),
    image_path VARCHAR(500) NOT NULL,
    thumbnail_path VARCHAR(500),
    image_size_bytes INTEGER NOT NULL,
    image_mime_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    user_reflection TEXT NOT NULL,
    identified_species VARCHAR(150),
    exif_data TEXT,
    latitude FLOAT,
    longitude FLOAT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- LLM-generated reflections and insights
CREATE TABLE reflections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL UNIQUE REFERENCES documents(id),
    observation_id INTEGER REFERENCES observations(id),
    cultural_interpretation TEXT NOT NULL,
    ideological_connections TEXT NOT NULL,
    cross_cultural_comparison TEXT NOT NULL,
    educational_narrative TEXT NOT NULL,
    linked_tribes TEXT NOT NULL,
    linked_principles TEXT NOT NULL,
    llm_model_used VARCHAR(100) NOT NULL,
    llm_prompt_version VARCHAR(50) NOT NULL,
    processing_time_ms INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## 💾 Data Loading Strategy

### Phase 1: Initialize Schema
```python
# scripts/init_db.py
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)
print("✅ Database schema initialized")
```

### Phase 2: Load Tree Data
```python
# scripts/load_trees.py
import json
from app.models import TreeCultural
from app.database import get_db

with open('data/tree_data/trees_cultural.json') as f:
    trees = json.load(f)
    
for tree_data in trees:
    tree = TreeCultural(
        common_name=tree_data['common_name'],
        scientific_name=tree_data['scientific_name'],
        tribal_associations=json.dumps(tree_data['tribal_associations']),
        ideological_principles=json.dumps(tree_data['ideological_principles']),
        # ... other fields
    )
    db.add(tree)
db.commit()
```

### Phase 3: Seed Sample Data (Development)
```python
# scripts/seed_data.py
# Creates sample users, observations, documents for testing
```

---

## 🔑 Key Design Decisions

1. **JSON for Complex Cultural Data**: Cultural meanings, tribal associations, principles stored as JSON strings in TEXT columns for flexibility and searchability

2. **Separate TreesCultural Table**: Maintains authoritative tree database independent of user observations (read-mostly)

3. **Reflection as Separate Table**: Allows LLM processing to be asynchronous and optional; document exists independently

4. **EXIF Extraction**: Geolocation and timestamps optionally extracted from images and stored in database

5. **Cascade Deletes**: Deleting a user cascades to observations, documents, reflections (GDPR compliance)

6. **Indexes on Common Queries**: `common_name`, `scientific_name`, `user_id` indexed for fast lookups

7. **Timestamps**: `created_at`, `updated_at` on all tables for audit trail

8. **UTF-8 Support**: SQLite with default UTF-8 encoding for multilingual cultural data

---

## 📋 Typical Query Patterns

```python
# Get all documents for a user
documents = db.query(Document).filter(Document.user_id == user_id).all()

# Get tree with cultural data
tree = db.query(TreeCultural).filter_by(scientific_name="Ficus religiosa").first()

# Get reflection insights for a document
reflection = db.query(Reflection).filter_by(document_id=doc_id).first()

# Search trees by cultural principle
# (requires parsing JSON - using raw SQL or ORM with JSON functions)
trees_enlightenment = db.query(TreeCultural).filter(
    TreeCultural.ideological_principles.contains('Enlightenment')
).all()

# Get recent observations with geographic location
recent = db.query(Observation).filter(
    Observation.latitude.isnot(None),
    Observation.created_at > datetime.utcnow() - timedelta(days=7)
).all()
```

---

**Status**: Ready for SQLAlchemy model generation by Claude Code
**Compatibility**: SQLAlchemy 2.0+, SQLite 3.40+, Python 3.11+
**JSON Fields**: All JSON data stored as TEXT, parsed/serialized in Python layer