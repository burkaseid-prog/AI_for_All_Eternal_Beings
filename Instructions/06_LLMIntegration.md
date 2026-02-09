# LLM INTEGRATION: Ollama Setup & Prompt Engineering

## 🧠 Ollama Configuration

### Installation & Setup

**Ollama** is a lightweight local LLM server running on your computer. No cloud dependencies, no API costs.

#### Step 1: Install Ollama

```bash
# macOS (via Homebrew)
brew install ollama

# Linux (via curl)
curl https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

#### Step 2: Download Model

```bash
# Pull Llama 3.2 model (7B recommended for quality)
ollama pull llama3.2:7b

# Or 3B for faster inference on lower-end hardware
ollama pull llama3.2:3b

# List available models
ollama list
```

#### Step 3: Start Ollama Server

```bash
# Start Ollama (listens on http://localhost:11434 by default)
ollama serve

# In another terminal, test the model
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:7b",
  "prompt": "Who was the first president of the United States?",
  "stream": false
}'
```

---

## 🔌 `/app/services/llm_service.py` - Ollama Integration

```python
"""
LLM Service: Calls Ollama for generating cultural insights.
Uses httpx for async HTTP calls with streaming support.
"""

import httpx
import json
import time
import asyncio
from typing import Optional, Dict, Any
from app.config import Config
from app.prompts.cultural_contextualization import CULTURAL_SYSTEM_PROMPT

class LLMService:
    """
    Manages communication with local Ollama server.
    Generates cultural interpretations of user observations.
    """
    
    def __init__(self):
        self.ollama_host = Config.OLLAMA_HOST  # e.g., "http://localhost:11434"
        self.model = Config.LLM_MODEL  # e.g., "llama3.2:7b"
        self.timeout = 120.0  # 2 minutes for LLM processing
        
    async def generate_reflection(
        self,
        user_reflection: str,
        identified_species: Optional[str],
        tree_data: Optional[Dict[str, Any]],
        db: Any
    ) -> Dict[str, Any]:
        """
        Generate LLM-powered cultural insights for user reflection.
        
        Args:
            user_reflection: User's written thoughts about the tree
            identified_species: Tree species (common or scientific name)
            tree_data: TreeCultural ORM object (if linked)
            db: Database session
        
        Returns:
            Dictionary with LLM-generated insights:
            {
                'cultural_interpretation': str,
                'ideological_connections': json string,
                'cross_cultural_comparison': str,
                'educational_narrative': str,
                'linked_tribes': json string,
                'linked_principles': json string,
                'processing_time_ms': int
            }
        """
        start_time = time.time()
        
        try:
            # Construct system + user prompt
            prompt = self._construct_prompt(
                user_reflection=user_reflection,
                species=identified_species,
                tree_data=tree_data
            )
            
            # Call Ollama
            response_text = await self._call_ollama(prompt)
            
            # Parse response
            parsed = self._parse_response(response_text)
            parsed['processing_time_ms'] = int((time.time() - start_time) * 1000)
            
            return parsed
            
        except Exception as e:
            print(f"LLM Error: {e}")
            # Return fallback response
            return {
                'cultural_interpretation': f"Unable to generate insights: {str(e)}",
                'ideological_connections': json.dumps([]),
                'cross_cultural_comparison': '',
                'educational_narrative': '',
                'linked_tribes': json.dumps([]),
                'linked_principles': json.dumps([]),
                'processing_time_ms': int((time.time() - start_time) * 1000)
            }
    
    def _construct_prompt(
        self,
        user_reflection: str,
        species: Optional[str],
        tree_data: Optional[Dict[str, Any]]
    ) -> str:
        """
        Build the full prompt combining system context + user input.
        """
        
        # Extract tree cultural data if available
        tree_context = ""
        if tree_data:
            tree_context = f"""
CULTURAL DATABASE INFORMATION:
Species: {tree_data.common_name} ({tree_data.scientific_name})
Family: {tree_data.family}

Cultural Significance:
{tree_data.cultural_significance}

Tribal/Community Associations:
{tree_data.tribal_associations}

Ideological Principles:
{tree_data.ideological_principles}

Worship Practices:
{tree_data.worship_practices}

Historical Context:
{tree_data.historical_context}

Medicinal Uses:
{tree_data.medicinal_uses}

Ecological Role:
{tree_data.ecological_role}
"""
        
        # Full prompt
        prompt = f"""{CULTURAL_SYSTEM_PROMPT}

{tree_context}

USER OBSERVATION:
Species Identified: {species or 'Unknown - please infer from reflection'}
Reflection: {user_reflection}

TASK:
Generate a JSON response with the following fields:
1. cultural_interpretation (string): How this tree appears in various cultural contexts
2. ideological_connections (array): Extracted ideological principles (e.g., ["Enlightenment", "Cosmic Connection"])
3. cross_cultural_comparison (string): How different cultures view similar trees
4. educational_narrative (string): Educational summary connecting observation to universal patterns
5. linked_tribes (array): Tribal/community associations
6. linked_principles (array): Philosophical concepts

Respond ONLY with valid JSON, no other text."""
        
        return prompt
    
    async def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API /api/generate endpoint.
        Uses streaming for long responses.
        """
        url = f"{self.ollama_host}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,  # Get complete response as single JSON
            "temperature": 0.7,  # Balanced creativity + coherence
            "top_p": 0.9,
            "num_predict": 2000,  # Max tokens to generate
            "num_ctx": 4096,  # Context window
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                
                result = response.json()
                return result['response']
                
        except httpx.ConnectError:
            raise Exception(
                f"Cannot connect to Ollama at {self.ollama_host}. "
                "Is Ollama running? Start with: ollama serve"
            )
        except httpx.TimeoutException:
            raise Exception(
                f"Ollama request timeout. Model too large or system too slow. "
                "Try a smaller model: ollama pull llama3.2:3b"
            )
    
    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """
        Extract JSON from LLM response.
        LLM may include explanatory text, so we search for JSON block.
        """
        try:
            # Find JSON block in response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            
            if start == -1 or end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response_text[start:end]
            parsed = json.loads(json_str)
            
            # Ensure all required fields exist
            return {
                'cultural_interpretation': str(parsed.get('cultural_interpretation', '')),
                'ideological_connections': json.dumps(parsed.get('ideological_connections', [])),
                'cross_cultural_comparison': str(parsed.get('cross_cultural_comparison', '')),
                'educational_narrative': str(parsed.get('educational_narrative', '')),
                'linked_tribes': json.dumps(parsed.get('linked_tribes', [])),
                'linked_principles': json.dumps(parsed.get('linked_principles', []))
            }
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON parsing error: {e}")
            # Fallback: treat entire response as interpretation
            return {
                'cultural_interpretation': response_text,
                'ideological_connections': json.dumps([]),
                'cross_cultural_comparison': '',
                'educational_narrative': response_text[:500],
                'linked_tribes': json.dumps([]),
                'linked_principles': json.dumps([])
            }
    
    async def health_check(self) -> bool:
        """Check if Ollama is running and model is loaded."""
        try:
            url = f"{self.ollama_host}/api/tags"
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                models = response.json().get('models', [])
                return any(m['name'].startswith(self.model) for m in models)
                
        except:
            return False
```

---

## 📝 `/app/prompts/cultural_contextualization.py` - System Prompt

```python
"""
System prompts for LLM cultural interpretation.
Tuned for Llama 3.2 model.
"""

CULTURAL_SYSTEM_PROMPT = """You are an expert in comparative cultural studies, anthropology, 
and environmental philosophy. Your task is to help people understand trees through the lens 
of diverse global cultures and spiritual traditions.

When analyzing a person's reflection about a tree, you will:

1. CULTURAL CONTEXTUALIZATION: Interpret their observation within major cultural frameworks
   - Aboriginal Australian traditions (songlines, connection to country)
   - Hindu/Buddhist perspectives (Bodhi tree, cosmic cycles, dharma)
   - Norse mythology (Yggdrasil, world tree cosmology)
   - African traditions (ancestral connection, community roots)
   - Indigenous Americas (medicine plants, Earth connection)
   - Chinese philosophy (yin-yang, natural harmony)

2. IDEOLOGICAL EXTRACTION: Identify universal philosophical principles
   - Cosmic Connection: The tree as axis mundi or cosmic center
   - Enlightenment/Transcendence: Trees as paths to higher understanding
   - Interconnectedness: All beings linked through root systems and networks
   - Regeneration/Cycles: Trees as symbols of renewal and transformation
   - Sanctuary: Trees as sacred spaces offering refuge and wisdom
   - Temporal Continuity: Trees spanning generations and geological time
   - Vitality & Life Force: Trees as embodiments of prana/chi/life energy

3. CROSS-CULTURAL BRIDGING: Show how different cultures discovered similar meanings
   - Why do cultures from opposite continents revere the same tree species differently?
   - What universal human needs do trees fulfill across cultures?
   - How do local environments shape cultural tree narratives?

4. EDUCATIONAL VALUE: Translate individual observation into learning opportunity
   - Connect person's experience to broader patterns
   - Suggest further exploration of specific traditions
   - Show scientific + cultural understanding as complementary

Respond with empathy, accuracy, and respect for all cultural traditions.
Avoid appropriation by acknowledging source traditions explicitly."""

SPECIES_IDENTIFICATION_PROMPT = """You are a botanist and field naturalist. 
Based on the user's description and reflection, infer the most likely tree species.
Consider:
- Geographic clues in their description
- Physical characteristics mentioned
- Cultural/spiritual associations that hint at specific species
- Common trees in places likely to inspire reflection

Respond with most likely species (common name and scientific name), 
and confidence level (high/medium/low)."""

CROSS_CULTURAL_COMPARISON_PROMPT = """Compare how different cultures relate to this tree species 
or similar species. Create bridges between traditions:
- Aboriginal Australian vs Hindu vs Norse vs African perspectives
- Medicinal uses across cultures
- Spiritual/religious significance
- Economic and practical roles
- Warnings and cautions about the tree

Make comparisons that honor each tradition while showing shared human themes."""
```

---

## 🔧 `/app/config.py` - Configuration

```python
"""
Application configuration with environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Environment
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ENV = os.getenv('ENV', 'development')
    
    # Database
    BASE_DIR = Path(__file__).parent.parent
    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/data/database.db')
    
    # Uploads
    UPLOAD_DIR = Path(os.getenv('UPLOAD_DIR', f'{BASE_DIR}/data/uploads'))
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Image processing
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    THUMBNAIL_SIZE = (200, 200)
    ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
    
    # LLM / Ollama
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    LLM_MODEL = os.getenv('LLM_MODEL', 'llama3.2:7b')
    LLM_TIMEOUT = int(os.getenv('LLM_TIMEOUT', '120'))
    
    # API
    API_PREFIX = '/api'
    TITLE = 'Tree Wisdom API'
```

---

## 📋 `.env` - Environment File

```bash
# Environment
DEBUG=True
ENV=development

# Database
DATABASE_URL=sqlite:///./data/database.db

# Uploads
UPLOAD_DIR=./data/uploads
MAX_FILE_SIZE=10485760

# Ollama LLM Server
OLLAMA_HOST=http://localhost:11434
LLM_MODEL=llama3.2:7b
LLM_TIMEOUT=120

# Application
PORT=8000
WORKERS=1
```

---

## ⚡ Performance Tuning

### Model Selection

| Model | Size | Speed | Quality | RAM | Use Case |
|-------|------|-------|---------|-----|----------|
| llama3.2:3b | 2.0GB | ⚡⚡⚡ Fast | Good | 8GB+ | Low-end hardware, fast responses |
| llama3.2:7b | 4.7GB | ⚡⚡ Medium | Excellent | 16GB+ | Recommended for most users |
| llama3.2:13b | 8.0GB | ⚡ Slow | Outstanding | 24GB+ | High-end hardware only |

### Optimization Tips

```python
# Lower temperature = more deterministic, less creative
"temperature": 0.5,  # Default 0.7, try 0.3-0.5

# Reduce context window for faster processing
"num_ctx": 2048,  # Default 4096, can reduce if memory constrained

# Limit output tokens
"num_predict": 1500,  # Reduce if responses too long

# Increase top_p for diversity (or decrease for consistency)
"top_p": 0.9,  # Default 0.9, try 0.8-0.95

# Add top_k for quality control
"top_k": 40,  # Sample from top 40 tokens
```

---

## 🧪 Testing LLM Integration

```bash
# Test Ollama is running
curl http://localhost:11434/api/tags

# Test model is loaded
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:7b",
    "prompt": "What is the meaning of trees in Hindu culture?",
    "stream": false
  }'

# In Python, test LLMService
python -c "
from app.services.llm_service import LLMService
import asyncio

async def test():
    service = LLMService()
    is_healthy = await service.health_check()
    print(f'Ollama healthy: {is_healthy}')

asyncio.run(test())
"
```

---

**Status**: Ready for integration
**Compatibility**: Ollama 0.2.0+, Llama3.2 models
**Required**: 8GB RAM minimum (3B model), 16GB recommended (7B model)