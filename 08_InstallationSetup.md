# INSTALLATION & SETUP: Complete Environment Configuration

## 🎯 System Requirements

### Minimum Hardware
- **CPU**: Dual-core processor (Intel i5/AMD Ryzen 5 or better)
- **RAM**: 8GB minimum (for smooth operation)
- **Storage**: 5GB free space (for Python, dependencies, database)
- **OS**: Windows 10/11, macOS 10.14+, Linux (any recent distribution)

### Software Requirements
- **Python**: 3.11 or newer (download from python.org)
- **pip**: Package manager (comes with Python)
- **Git**: Version control (optional, for cloning repositories)
- **Browser**: Any modern browser (Chrome, Firefox, Safari, Edge)

---

## 📋 Step 1: Prepare Your Computer

### macOS

```bash
# 1. Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python 3.11
brew install python@3.11

# 3. Verify installation
python3 --version
pip3 --version

# 4. Install Git (optional)
brew install git
```

### Windows (PowerShell as Administrator)

```powershell
# 1. Install Python 3.11 from https://www.python.org/downloads/
#    - Check "Add Python to PATH" during installation
#    - Choose "Install for all users"

# 2. Verify installation (open new PowerShell)
python --version
pip --version

# 3. Install Git (optional) from https://git-scm.com/download/win
```

### Linux (Ubuntu/Debian)

```bash
# 1. Update package manager
sudo apt update
sudo apt upgrade -y

# 2. Install Python 3.11 and dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip git

# 3. Verify installation
python3.11 --version
pip3 --version
```

---

## 🚀 Step 2: Create Project Directory

```bash
# Create and navigate to project
mkdir ~/tree-wisdom
cd ~/tree-wisdom

# Create subdirectories
mkdir -p app/{routers,services,templates/{static/{css,js}},prompts}
mkdir -p data/{uploads/{original,thumbnails},tree_data,exports}
mkdir -p scripts tests

# Verify structure
tree -L 3  # (if tree command available)
# or
ls -la
```

---

## 🐍 Step 3: Create Python Virtual Environment

### macOS/Linux

```bash
cd ~/tree-wisdom

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) prefix in terminal
```

### Windows (PowerShell)

```powershell
cd C:\Users\YourUsername\tree-wisdom

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then run activation command again
```

---

## 📦 Step 4: Install Python Dependencies

With virtual environment activated (you should see `(venv)` prefix):

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies from requirements.txt
pip install fastapi==0.104.1 \
            uvicorn[standard]==0.24.0 \
            sqlalchemy==2.0.23 \
            pillow==10.1.0 \
            httpx==0.25.2 \
            pydantic==2.5.0 \
            python-multipart==0.0.6 \
            python-dotenv==1.0.0 \
            google-generativeai==0.3.0

# Verify installation
pip list | grep -E "fastapi|sqlalchemy|pillow|google"
```

---

## 🔐 Step 5: Get Google Gemini API Key

### Free (No Credit Card Required)

1. **Open** [Google AI Studio](https://aistudio.google.com/apikey)
2. **Sign in** with your Google account
3. **Click** "Create API Key" button
4. **Select** your project (or create new)
5. **Copy** the generated API key
6. **Save** it securely (you'll need it soon)

**Note**: Free tier allows 60 requests/minute and 1,500 requests/day—plenty for local development.

---

## 🌍 Step 6: Create Environment Configuration

### Create `.env` file in project root

```bash
# Navigate to project root
cd ~/tree-wisdom

# Create .env file with your API key
cat > .env << 'EOF'
# Environment
DEBUG=True
ENV=development

# Database
DATABASE_URL=sqlite:///./data/database.db

# Uploads
UPLOAD_DIR=./data/uploads
MAX_FILE_SIZE=10485760

# Google Gemini API (Free tier)
# Get at: https://aistudio.google.com/apikey
GEMINI_API_KEY=your_api_key_here_paste_here

# Application
PORT=8000
WORKERS=1
EOF

# On Windows, create manually:
# 1. Open Notepad
# 2. Paste the content above
# 3. Save as "C:\Users\YourUsername\tree-wisdom\.env"
```

Replace `your_api_key_here_paste_here` with your actual Gemini API key from Step 5.

---

## 📄 Step 7: Create Project Files

### Create `requirements.txt`

```bash
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pillow==10.1.0
httpx==0.25.2
pydantic==2.5.0
python-multipart==0.0.6
python-dotenv==1.0.0
google-generativeai==0.3.0
EOF
```

### Create `.gitignore`

```bash
cat > .gitignore << 'EOF'
# Virtual Environment
venv/
env/
__pycache__/
*.py[cod]

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database & Uploads
*.db
data/uploads/
data/exports/

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Project
*.log
.pytest_cache/
EOF
```

### Create `app/__init__.py` (Empty file)

```bash
touch app/__init__.py
touch app/routers/__init__.py
touch app/services/__init__.py
touch app/prompts/__init__.py
touch tests/__init__.py
```

---

## 🗄️ Step 8: Initialize Database

### Create `scripts/init_db.py`

```bash
cat > scripts/init_db.py << 'EOF'
"""
Initialize SQLite database schema.
Run once at startup.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import engine
from app.models import Base

if __name__ == "__main__":
    print("🌳 Initializing Tree Wisdom database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database initialized successfully!")
    print("📁 Location: ./data/database.db")
EOF

# Run initialization
python scripts/init_db.py
```

---

## 📊 Step 9: Load Initial Tree Data

### Create `scripts/load_trees.py`

```bash
cat > scripts/load_trees.py << 'EOF'
"""
Load cultural tree database from JSON.
Run after init_db.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models import TreeCultural

def load_trees():
    """Load tree_cultural.json into database."""
    
    # Sample tree data (replace with comprehensive data from document 09)
    sample_trees = [
        {
            "common_name": "Bodhi Tree",
            "scientific_name": "Ficus religiosa",
            "genus": "Ficus",
            "family": "Moraceae",
            "native_regions": ["India", "Southeast Asia", "Nepal"],
            "height_range": "15-25m",
            "lifespan_years": 2000,
            "cultural_significance": "Sacred in Buddhism. Tree under which Buddha achieved enlightenment. Symbol of awakening and spiritual growth.",
            "tribal_associations": '{"Hindu": "Connection to divine consciousness", "Buddhist": "Gateway to Nirvana", "Indian": "Guardian of wisdom"}',
            "ideological_principles": '["Enlightenment", "Transcendence", "Divine Connection", "Spiritual Awakening"]',
            "worship_practices": '["Meditation", "Pilgrimage", "Ritual circumambulation", "Offerings of flowers"]',
            "historical_context": "Ancient symbol spanning 2500+ years of human spiritual seeking across cultures.",
            "medicinal_uses": '{"Sanskrit": "Used in Ayurveda for balance", "Traditional": "Bark for digestive health", "Modern": "Research on anti-inflammatory properties"}',
            "ecological_role": "Shade provider in warm climates. Supports diverse bird and insect species. Contributes to air purification."
        },
        {
            "common_name": "Oak",
            "scientific_name": "Quercus robur",
            "genus": "Quercus",
            "family": "Fagaceae",
            "native_regions": ["Europe", "Western Asia", "North Africa"],
            "height_range": "20-40m",
            "lifespan_years": 1000,
            "cultural_significance": "Revered in Celtic, Germanic, and Norse traditions. Symbol of strength, endurance, and cosmic wisdom. Sacred to Druids.",
            "tribal_associations": '{"Celtic": "Druidic knowledge center", "Germanic": "Thor\'s sacred tree", "Norse": "Connected to Yggdrasil", "European": "Symbol of nationhood"}',
            "ideological_principles": '["Strength", "Endurance", "Cosmic Connection", "Ancient Wisdom", "Community Root"]',
            "worship_practices": '["Sacred groves", "Ceremonial gatherings", "Oath-taking rituals", "Solar celebrations"]',
            "historical_context": "Central to European paganism and later Christian symbolism. Hundreds of ancient oaks still alive today.",
            "medicinal_uses": '{"Traditional": "Bark for fever and wounds", "Herbalism": "Tannins for health", "Folk": "Acorns ground for sustenance"}',
            "ecological_role": "Keystone species. Supports 300+ insect species. Provides acorns for wildlife. Long-term carbon storage."
        },
        {
            "common_name": "Baobab",
            "scientific_name": "Adansonia digitata",
            "genus": "Adansonia",
            "family": "Bombacaceae",
            "native_regions": ["Africa", "Madagascar", "Australia"],
            "height_range": "18-25m",
            "lifespan_years": 6000,
            "cultural_significance": "Tree of Life in African mythology. Symbol of regeneration, resilience, and ancestral connection. Community gathering center.",
            "tribal_associations": '{"African": "Ancestral gathering place", "Aboriginal": "Songline marker", "Malagasy": "Symbol of life force"}',
            "ideological_principles": '["Regeneration", "Community", "Ancestral Connection", "Temporal Continuity", "Life Force"]',
            "worship_practices": '["Ancestor veneration", "Community gatherings", "Sacred ceremonies", "Healing rituals"]',
            "historical_context": "Some baobabs are thousands of years old. Documented in Egyptian hieroglyphics. Symbol of African identity.",
            "medicinal_uses": '{"African": "Fruit for nutrition and immune health", "Traditional": "Bark for fevers", "Modern": "Superfood marketed globally"}',
            "ecological_role": "Drought survivor. Provides water, food, and shelter in arid regions. Critical to savanna ecosystems."
        }
    ]
    
    db = SessionLocal()
    
    try:
        for tree_data in sample_trees:
            # Check if already exists
            existing = db.query(TreeCultural).filter_by(
                scientific_name=tree_data['scientific_name']
            ).first()
            
            if not existing:
                tree = TreeCultural(**tree_data)
                db.add(tree)
                print(f"✅ Added: {tree_data['common_name']}")
            else:
                print(f"⏭️  Skipped: {tree_data['common_name']} (already exists)")
        
        db.commit()
        print("\n🌳 Tree database loaded successfully!")
        
    except Exception as e:
        print(f"❌ Error loading trees: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_trees()
EOF

# Run tree loading
python scripts/load_trees.py
```

---

## ✅ Step 10: Verify Installation

```bash
# Make sure virtual environment is active
# (you should see (venv) prefix)

# Test imports
python -c "
import fastapi
import sqlalchemy
import PIL
import google.generativeai
print('✅ All dependencies installed successfully!')
"

# Test database
python -c "
from app.database import SessionLocal
from app.models import TreeCultural
db = SessionLocal()
trees = db.query(TreeCultural).count()
print(f'✅ Database initialized with {trees} trees')
db.close()
"

# Test Gemini API
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    print(f'✅ Gemini API key configured')
else:
    print('❌ Gemini API key not found in .env')
"
```

---

## 🎯 Quick Setup Summary (Copy & Paste)

For experienced developers:

```bash
# Clone/create project
mkdir ~/tree-wisdom && cd ~/tree-wisdom

# Setup Python
python3.11 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows

# Install dependencies
pip install fastapi uvicorn sqlalchemy pillow httpx pydantic python-multipart python-dotenv google-generativeai

# Create .env (REPLACE WITH YOUR GEMINI KEY)
echo "GEMINI_API_KEY=your_key_here" > .env
echo "DEBUG=True" >> .env
echo "DATABASE_URL=sqlite:///./data/database.db" >> .env

# Create directories
mkdir -p app/{routers,services,templates/{static/{css,js}},prompts} data/{uploads/{original,thumbnails},tree_data,exports} scripts tests

# Initialize database
python scripts/init_db.py

# Ready to launch! (see next document)
```

---

## 🆘 Troubleshooting

### "python not found"
```bash
# Use python3 instead
python3.11 -m venv venv
```

### "pip: command not found"
```bash
# Use pip3
pip3 install fastapi
```

### "Module not found" errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows

# Then install requirements
pip install -r requirements.txt
```

### ".env file not found"
```bash
# Ensure .env is in project root
ls -la .env  # Should exist in ~/tree-wisdom/

# If not, create it with your Gemini API key
```

### "GEMINI_API_KEY" errors
```bash
# Check .env file has correct key
cat .env | grep GEMINI_API_KEY

# Or verify in code
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY'))"
```

---

**Status**: Installation complete
**Next**: See DEPLOYMENT_LOCAL.md for running the application