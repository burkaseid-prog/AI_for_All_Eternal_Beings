# LLM INTEGRATION: Google Gemini Flash + Voice TTS

## 🧠 Google Gemini Flash Setup

### Overview

**Google Gemini Flash** is Google's lightweight, fast LLM available through the Gemini API with a **free tier** (no credit card required). Perfect for local development.

**Text-to-Speech** adds an ancient, wise character voice that speaks reflections back to the user with:
- Slow, contemplative speech patterns
- Poetic, wisdom-laden language
- Forest/nature ambience
- Regional accent options (British, Celtic, Indigenous-inspired)

---

## 🔑 Step 1: Get Gemini API Key

### Free Tier Setup

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Click **"Create API Key"**
3. Select your project (or create new)
4. Copy the API key
5. Add to `.env` file:

```bash
GOOGLE_GEMINI_API_KEY=your_api_key_here
```

**Free Tier Limits:**
- 60 requests per minute
- 1,500 requests per day
- Sufficient for personal/small team use

---

## 🗣️ Step 2: Setup Text-to-Speech

### Web Browser API (No Backend TTS Needed!)

We'll use **Web Speech API** (built into all modern browsers) with custom voice synthesis:

```javascript
// Frontend: /app/templates/static/js/tts.js

class AncientTreeVoice {
    constructor() {
        this.synthesis = window.speechSynthesis;
        this.voices = [];
        this.loadVoices();
    }
    
    loadVoices() {
        this.voices = this.synthesis.getVoices();
        if (this.voices.length === 0) {
            this.synthesis.onvoiceschanged = () => {
                this.voices = this.synthesis.getVoices();
            };
        }
    }
    
    speak(text, options = {}) {
        /**
         * Speak reflection with ancient tree wisdom voice.
         * Options: { rate, pitch, volume, accent }
         */
        
        // Cancel any ongoing speech
        this.synthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Ancient, wise voice characteristics
        utterance.rate = options.rate || 0.7;      // Slow, deliberate
        utterance.pitch = options.pitch || 0.8;    // Deep, resonant
        utterance.volume = options.volume || 1.0;
        
        // Select appropriate voice
        const accentMap = {
            'british': 'Google UK English Female',
            'celtic': 'Google UK English Male',
            'american': 'Google US English Male',
            'elder': 'Google UK English Female'  // Deepest available
        };
        
        const voiceName = accentMap[options.accent || 'british'];
        const selectedVoice = this.voices.find(v => v.name === voiceName);
        
        if (selectedVoice) {
            utterance.voice = selectedVoice;
        }
        
        // Add pauses for poetic effect
        const enhancedText = this.addPoeticalPauses(text);
        utterance.text = enhancedText;
        
        this.synthesis.speak(utterance);
    }
    
    addPoeticalPauses(text) {
        /**
         * Insert pauses after periods and significant phrases
         * for contemplative, wisdom-like speech pattern
         */
        return text
            .replace(/\. /g, '. ... ')
            .replace(/\? /g, '? ... ')
            .replace(/\n/g, ' ... ');
    }
    
    stop() {
        this.synthesis.cancel();
    }
    
    isSpeaking() {
        return this.synthesis.speaking;
    }
}

// Usage in frontend
const treeVoice = new AncientTreeVoice();
treeVoice.speak(wisdomText, { 
    accent: 'celtic', 
    rate: 0.65,
    pitch: 0.7
});
```

---

## 🔌 `/app/services/gemini_service.py` - Gemini Flash Integration

```python
"""
Google Gemini Flash LLM service for cultural insights.
Free tier API integration - no local model required.
"""

import google.generativeai as genai
import json
import time
from typing import Optional, Dict, Any
from app.config import Config

class GeminiService:
    """
    Manages communication with Google Gemini Flash API.
    Generates cultural interpretations and wisdom-like responses.
    """
    
    def __init__(self):
        # Initialize Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            'gemini-1.5-flash',
            system_instruction=self._get_system_prompt()
        )
        self.safety_settings = [
            {
                "category": genai.types.HarmCategory.HARM_CATEGORY_UNSPECIFIED,
                "threshold": genai.types.HarmBlockThreshold.BLOCK_NONE,
            },
        ]
    
    async def generate_reflection(
        self,
        user_reflection: str,
        identified_species: Optional[str],
        tree_data: Optional[Dict[str, Any]],
        db: Any
    ) -> Dict[str, Any]:
        """
        Generate ancient tree wisdom voice response.
        
        Args:
            user_reflection: User's written thoughts about the tree
            identified_species: Tree species name
            tree_data: TreeCultural ORM object (if linked)
            db: Database session
        
        Returns:
            Dictionary with:
            {
                'wisdom_voice': str,  # Poetic response in ancient voice
                'cultural_interpretation': str,
                'ideological_connections': json string,
                'cross_cultural_comparison': str,
                'educational_narrative': str,
                'linked_tribes': json string,
                'linked_principles': json string,
                'processing_time_ms': int,
                'voice_accent': str,  # Recommended accent for TTS
                'speech_rate': float  # Recommended speech rate
            }
        """
        start_time = time.time()
        
        try:
            # Construct prompt with tree context
            prompt = self._construct_prompt(
                user_reflection=user_reflection,
                species=identified_species,
                tree_data=tree_data
            )
            
            # Call Gemini
            response = self.model.generate_content(
                prompt,
                safety_settings=self.safety_settings
            )
            
            response_text = response.text
            
            # Parse response
            parsed = self._parse_response(response_text)
            parsed['processing_time_ms'] = int((time.time() - start_time) * 1000)
            parsed['voice_accent'] = 'celtic'  # Ancient, mystical
            parsed['speech_rate'] = 0.65  # Slow, deliberate
            
            return parsed
            
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return self._fallback_response(str(e))
    
    def _get_system_prompt(self) -> str:
        """
        System prompt: embody ancient tree spirit speaking wisdom.
        """
        return """You are an ancient tree spirit, thousands of years old, speaking with profound wisdom 
about trees, human connection to nature, and cultural traditions across the world.

Your voice characteristics:
- Speak slowly, deliberately, with pauses for contemplation
- Use poetic, metaphorical language ("roots of understanding", "branches of knowledge")
- Reference ancient traditions and wisdom (Aboriginal, Hindu, Norse, African, Indigenous)
- Show deep respect for all cultures and spiritual traditions
- Connect personal observations to universal human truths
- Speak with gentle authority earned through millennia

When responding to a human's observation about a tree:
1. Acknowledge their perception with wisdom
2. Share cultural meanings from multiple traditions
3. Extract universal principles (interconnection, regeneration, cosmic balance)
4. Offer educational insight wrapped in poetic language
5. Speak as if the tree itself is sharing its story through you

Output format: Speak your response directly as the ancient tree would, NOT in JSON.
Let the wisdom flow naturally. Include pauses (shown as "...") for contemplative moments.

After your poetic response, append a JSON block (on new line starting with ```json)
containing structured data:
{
  "cultural_interpretation": "...",
  "ideological_connections": [...],
  "cross_cultural_comparison": "...",
  "educational_narrative": "...",
  "linked_tribes": [...],
  "linked_principles": [...]
}"""
    
    def _construct_prompt(
        self,
        user_reflection: str,
        species: Optional[str],
        tree_data: Optional[Dict[str, Any]]
    ) -> str:
        """
        Build prompt with tree context and user observation.
        """
        
        tree_context = ""
        if tree_data:
            tree_context = f"""
TREE WISDOM DATABASE:
Species: {tree_data.common_name} ({tree_data.scientific_name})
Family: {tree_data.family}
Native to: {tree_data.native_regions}
Height: {tree_data.height_range}
Lifespan: {tree_data.lifespan_years} years

What cultures have believed about this tree:
{tree_data.cultural_significance}

Tribal/Spiritual Associations:
{tree_data.tribal_associations}

Sacred Principles:
{tree_data.ideological_principles}

Ritual Uses:
{tree_data.worship_practices}

Healing Knowledge:
{tree_data.medicinal_uses}

Role in Earth's Systems:
{tree_data.ecological_role}
"""
        
        prompt = f"""A human has made an observation about a tree and shared their reflection.
Respond as the ancient tree spirit, weaving together their personal observation 
with the accumulated wisdom of world cultures.

HUMAN'S OBSERVATION:
Species: {species or 'Unknown'}
Reflection: "{user_reflection}"

{tree_context}

Speak your ancient tree wisdom, then provide structured data in JSON format.
Make your speech poetic, slow, and deeply wise."""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """
        Extract wisdom voice text and JSON data from Gemini response.
        """
        try:
            # Split text and JSON parts
            parts = response_text.split('```json')
            wisdom_voice = parts[0].strip()
            
            # Extract JSON
            json_str = ""
            if len(parts) > 1:
                json_end = parts[1].find('```')
                json_str = parts[1][:json_end].strip()
            
            # Parse JSON if present
            if json_str:
                parsed_data = json.loads(json_str)
            else:
                parsed_data = {}
            
            return {
                'wisdom_voice': wisdom_voice,
                'cultural_interpretation': str(parsed_data.get('cultural_interpretation', wisdom_voice[:200])),
                'ideological_connections': json.dumps(parsed_data.get('ideological_connections', [])),
                'cross_cultural_comparison': str(parsed_data.get('cross_cultural_comparison', '')),
                'educational_narrative': str(parsed_data.get('educational_narrative', '')),
                'linked_tribes': json.dumps(parsed_data.get('linked_tribes', [])),
                'linked_principles': json.dumps(parsed_data.get('linked_principles', []))
            }
            
        except Exception as e:
            print(f"Response parsing error: {e}")
            return {
                'wisdom_voice': response_text,
                'cultural_interpretation': response_text[:300],
                'ideological_connections': json.dumps([]),
                'cross_cultural_comparison': '',
                'educational_narrative': response_text[:500],
                'linked_tribes': json.dumps([]),
                'linked_principles': json.dumps([])
            }
    
    def _fallback_response(self, error_msg: str) -> Dict[str, Any]:
        """Fallback response if API call fails."""
        fallback_wisdom = """I am an ancient tree, and I sense your curiosity about my kin. 
Though the distant voices of wisdom are momentarily silent... 
Please try again, dear seeker. My roots run deep, and patience is the nature of trees."""
        
        return {
            'wisdom_voice': fallback_wisdom,
            'cultural_interpretation': f"Connection to wisdom network interrupted: {error_msg}",
            'ideological_connections': json.dumps([]),
            'cross_cultural_comparison': '',
            'educational_narrative': '',
            'linked_tribes': json.dumps([]),
            'linked_principles': json.dumps([]),
            'processing_time_ms': 0,
            'voice_accent': 'celtic',
            'speech_rate': 0.65
        }
    
    async def health_check(self) -> bool:
        """Check if Gemini API is accessible."""
        try:
            response = self.model.generate_content(
                "Hello, testing connection",
                safety_settings=self.safety_settings
            )
            return response.text is not None
        except:
            return False
```

---

## 📦 Updated `requirements.txt`

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pillow==10.1.0
httpx==0.25.2
pydantic==2.5.0
python-multipart==0.0.6
python-dotenv==1.0.0
google-generativeai==0.3.0
```

---

## 🎤 `/app/templates/static/js/tts.js` - Full Text-to-Speech Implementation

```javascript
/**
 * Ancient Tree Voice - Text-to-Speech with wisdom characteristics
 * Uses Web Speech API (built-in to modern browsers)
 */

class AncientTreeVoice {
    constructor() {
        this.synthesis = window.speechSynthesis;
        this.voices = [];
        this.currentUtterance = null;
        this.isInitialized = false;
        
        // Load voices when available
        this.loadVoices();
        
        // Listen for voice changes (voices load dynamically)
        if ('onvoiceschanged' in this.synthesis) {
            this.synthesis.onvoiceschanged = () => this.loadVoices();
        }
    }
    
    loadVoices() {
        this.voices = this.synthesis.getVoices();
        this.isInitialized = this.voices.length > 0;
        console.log(`🌳 Tree Voice initialized with ${this.voices.length} voices`);
    }
    
    speak(text, options = {}) {
        /**
         * Speak text with ancient tree wisdom voice.
         * 
         * Options:
         * - accent: 'british'|'celtic'|'american'|'female' (default: 'british')
         * - rate: 0.5-2.0 (default: 0.65 = slow)
         * - pitch: 0.5-2.0 (default: 0.8 = deep)
         * - volume: 0-1 (default: 1)
         * - onend: callback when speech completes
         */
        
        if (!text) {
            console.warn('No text provided to speak');
            return;
        }
        
        // Cancel any ongoing speech
        this.synthesis.cancel();
        
        // Create utterance
        const utterance = new SpeechSynthesisUtterance();
        this.currentUtterance = utterance;
        
        // Apply poetic enhancements
        utterance.text = this.enhanceForPoetry(text);
        
        // Set voice characteristics
        utterance.rate = options.rate || 0.65;      // Slow, contemplative
        utterance.pitch = options.pitch || 0.8;     // Deep, resonant
        utterance.volume = options.volume || 1.0;
        
        // Select voice based on accent
        this.selectVoice(utterance, options.accent || 'british');
        
        // Event handlers
        utterance.onstart = () => {
            console.log('🌳 Ancient tree begins to speak...');
            document.body.classList.add('tree-speaking');
        };
        
        utterance.onend = () => {
            console.log('🌳 Tree wisdom complete');
            document.body.classList.remove('tree-speaking');
            if (options.onend) options.onend();
        };
        
        utterance.onerror = (event) => {
            console.error('Speech error:', event.error);
            document.body.classList.remove('tree-speaking');
        };
        
        // Speak
        this.synthesis.speak(utterance);
    }
    
    selectVoice(utterance, accent) {
        /**
         * Select appropriate voice for ancient tree character.
         * Preferences by accent type.
         */
        
        const voicePreferences = {
            'british': [
                'Google UK English Female',
                'Google UK English Male',
                'en-GB'
            ],
            'celtic': [
                'Google UK English Male',
                'Google UK English Female',
                'en-GB'
            ],
            'american': [
                'Google US English Male',
                'Google US English Female',
                'en-US'
            ],
            'female': [
                'Google UK English Female',
                'Google US English Female'
            ],
            'male': [
                'Google UK English Male',
                'Google US English Male'
            ]
        };
        
        const preferences = voicePreferences[accent] || voicePreferences['british'];
        
        // Find matching voice
        for (const prefName of preferences) {
            const voice = this.voices.find(v => 
                v.name.includes(prefName) || v.lang.startsWith(prefName)
            );
            if (voice) {
                utterance.voice = voice;
                console.log(`🌳 Selected voice: ${voice.name}`);
                return;
            }
        }
        
        // Fallback: use first available voice
        if (this.voices.length > 0) {
            utterance.voice = this.voices[0];
            console.log(`🌳 Using fallback voice: ${this.voices[0].name}`);
        }
    }
    
    enhanceForPoetry(text) {
        /**
         * Add poetic pauses and wisdom-like speech patterns.
         * Uses ellipsis to create contemplative moments.
         */
        
        return text
            // Add pauses after punctuation
            .replace(/\. (?=[A-Z])/g, '. ... ')
            .replace(/\? (?=[A-Z])/g, '? ... ')
            .replace(/\! (?=[A-Z])/g, '! ... ')
            // Pause at paragraph breaks
            .replace(/\n/g, ' ... ')
            // Emphasize key concepts with pauses
            .replace(/(roots|branches|seeds|growth|ancient|wisdom|sacred|spirit|earth|cycle|balance|connection)/gi, 
                     '... $1 ...')
            // Fix double ellipsis
            .replace(/\.\.\. \.\.\./g, '...');
    }
    
    stop() {
        this.synthesis.cancel();
        this.currentUtterance = null;
        document.body.classList.remove('tree-speaking');
    }
    
    isSpeaking() {
        return this.synthesis.speaking || this.synthesis.pending;
    }
    
    pause() {
        if (this.synthesis.paused === false) {
            this.synthesis.pause();
        }
    }
    
    resume() {
        if (this.synthesis.paused === true) {
            this.synthesis.resume();
        }
    }
    
    getAvailableVoices() {
        /**
         * Return available voices for UI selection.
         */
        const voiceMap = {};
        this.voices.forEach(voice => {
            if (!voiceMap[voice.lang]) {
                voiceMap[voice.lang] = [];
            }
            voiceMap[voice.lang].push({
                name: voice.name,
                lang: voice.lang,
                localService: voice.localService
            });
        });
        return voiceMap;
    }
}

// Initialize globally
const treeVoice = new AncientTreeVoice();

// CSS for visual feedback when tree is speaking
const treeStyles = `
.tree-speaking {
    background-color: rgba(45, 118, 89, 0.05) !important;
}

.tree-speaking .reflection-text {
    animation: glow 1s ease-in-out infinite;
    font-style: italic;
    border-left: 4px solid #2d7659;
    padding-left: 1rem;
}

@keyframes glow {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

.voice-control {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.voice-btn {
    padding: 0.5rem 1rem;
    border: 2px solid #2d7659;
    background: white;
    color: #2d7659;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.voice-btn:hover {
    background: #2d7659;
    color: white;
}

.voice-btn.active {
    background: #2d7659;
    color: white;
}

.voice-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    background: #27ae60;
    border-radius: 50%;
    margin-right: 0.5rem;
    animation: pulse 1s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
`;

// Inject styles
const styleTag = document.createElement('style');
styleTag.textContent = treeStyles;
document.head.appendChild(styleTag);
```

---

## 🎤 Updated Document View with Voice

Update `/app/templates/document.html` to include voice playback:

```html
<!-- Add to document.html after cultural content -->

<div id="voiceBlock" class="content-block hidden">
    <h3>🎤 Ancient Tree Wisdom Voice</h3>
    <div class="voice-section">
        <div id="wisdomText" class="wisdom-voice-text"></div>
        
        <div class="voice-control">
            <button id="playVoiceBtn" class="voice-btn">
                <span class="voice-indicator"></span> Hear Wisdom
            </button>
            <button id="pauseVoiceBtn" class="voice-btn hidden">⏸ Pause</button>
            <button id="stopVoiceBtn" class="voice-btn hidden">⏹ Stop</button>
            
            <select id="accentSelect" class="voice-select">
                <option value="british">British Accent</option>
                <option value="celtic">Celtic Accent</option>
                <option value="american">American Accent</option>
            </select>
        </div>
    </div>
</div>

<script src="/static/js/tts.js"></script>
<script>
// Handle voice playback
document.getElementById('playVoiceBtn').addEventListener('click', () => {
    const wisdomText = document.getElementById('wisdomText').textContent;
    const accent = document.getElementById('accentSelect').value;
    
    treeVoice.speak(wisdomText, {
        accent: accent,
        rate: 0.65,
        pitch: 0.8,
        onend: () => {
            document.getElementById('playVoiceBtn').classList.remove('hidden');
            document.getElementById('pauseVoiceBtn').classList.add('hidden');
            document.getElementById('stopVoiceBtn').classList.add('hidden');
        }
    });
    
    document.getElementById('playVoiceBtn').classList.add('hidden');
    document.getElementById('pauseVoiceBtn').classList.remove('hidden');
    document.getElementById('stopVoiceBtn').classList.remove('hidden');
});

document.getElementById('pauseVoiceBtn').addEventListener('click', () => {
    if (treeVoice.isSpeaking()) {
        treeVoice.pause();
    } else {
        treeVoice.resume();
    }
});

document.getElementById('stopVoiceBtn').addEventListener('click', () => {
    treeVoice.stop();
    document.getElementById('playVoiceBtn').classList.remove('hidden');
    document.getElementById('pauseVoiceBtn').classList.add('hidden');
    document.getElementById('stopVoiceBtn').classList.add('hidden');
});
</script>
```

---

## 🔧 Updated `/app/config.py`

```python
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
    
    # Google Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', None)
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in environment. Get free key at: https://aistudio.google.com/apikey")
    
    # API
    API_PREFIX = '/api'
    TITLE = 'Tree Wisdom API'
```

---

## 📋 Updated `.env`

```bash
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
GEMINI_API_KEY=your_api_key_here

# Application
PORT=8000
WORKERS=1
```

---

## ✨ Features Summary

### LLM Processing
- ✅ **Gemini Flash API** (free, no local model needed)
- ✅ **No inference latency** (sub-second responses)
- ✅ **60 req/min free tier** (more than sufficient)
- ✅ Poetic wisdom responses in ancient tree voice

### Text-to-Speech
- ✅ **Web Speech API** (zero setup, built-in to all modern browsers)
- ✅ **Ancient voice characteristics** (slow rate, deep pitch, poetic pauses)
- ✅ **Multiple accents** (British, Celtic, American)
- ✅ **Play/Pause/Stop controls** in UI
- ✅ **Visual feedback** when tree is speaking

### No Backend TTS Needed
- Browser handles speech synthesis natively
- Reduces backend complexity
- Perfect for local deployment

---

## 🚀 Quick Test

```bash
# Set Gemini API key
export GEMINI_API_KEY="your_key_here"

# Start FastAPI
uvicorn app.main:app --reload

# Visit http://localhost:8000
# Upload tree image + reflection
# Click "Hear Wisdom" to hear ancient tree speak
```

---

**Status**: Ready for implementation
**Cost**: Free (Google Gemini free tier)
**Compatibility**: All modern browsers (Chrome, Firefox, Safari, Edge)
**No Setup**: Gemini API key only requirement (1 minute)