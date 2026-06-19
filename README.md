# RAG-Based AI Teaching Assistant

A retrieval-augmented generation (RAG) system that converts video lectures into an intelligent Q&A assistant using embeddings, semantic search, and local LLM inference.

## 📋 Overview

This project enables you to build a custom AI teaching assistant from your own video content. It transcribes videos, creates semantic embeddings, and uses similarity search to retrieve relevant content chunks before feeding them to an LLM for context-aware answers.

## ✨ Features

- **Video Processing**: Automatic conversion of video files to MP3 format using FFmpeg
- **Speech-to-Text**: Transcription and optional translation using OpenAI Whisper
- **Semantic Search**: Embedding-based retrieval using BGE-M3 embeddings via Ollama
- **Local LLM**: Query answering with Llama 3.2 through Ollama API
- **Persistent Storage**: Embeddings cached using joblib for fast reuse
- **Context Injection**: Retrieved video chunks automatically formatted into prompts

## 🛠️ Prerequisites

- **Python**: 3.8 or higher
- **FFmpeg**: For audio conversion (download: https://ffmpeg.org/download.html)
- **Ollama**: For local embedding and LLM models (download: https://ollama.ai)
- **Ollama Models**: 
  - `bge-m3` (for embeddings)
  - `llama3.2` (for text generation)

## 📦 Installation

1. **Clone or download the project**
   ```bash
   cd RAG_Based_AI
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install pandas scikit-learn numpy joblib requests openai-whisper
   ```

4. **Ensure Ollama is running**
   ```bash
   ollama serve
   ```

5. **Pull required models (in a new terminal)**
   ```bash
   ollama pull bge-m3
   ollama pull llama3.2
   ```

## 🚀 Quick Start

### Step 1: Prepare Videos
Place your video files in the `Videos/` folder. Video filenames should follow the format:
```
#<number> <title> [optional].mp4
```

### Step 2: Convert Videos to MP3
```bash
python video_to_mp3.py
```
Outputs MP3 files to `audios/` folder.

### Step 3: Transcribe MP3 to JSON
```bash
python mp3_to_json.py
```
Creates timestamped transcription chunks in `jsons/` folder with format:
```json
{
  "title": "Video Title",
  "number": "01",
  "chunks": [
    {"text": "...", "start": 0.0, "end": 5.5},
    ...
  ]
}
```

### Step 4: Create Embeddings
```bash
python preprocess_json.py
```
Generates `embeddings.joblib` file containing embeddings for all text chunks.

### Step 5: Query the Assistant
```bash
python process_incoming.py
```
Interactive prompt:
```
Ask a Question: What is HTML?
```
Returns relevant video sections with timestamps and LLM-generated answers.

## 📁 Project Structure

```
RAG_Based_AI/
├── Videos/              # Input video files (place your videos here)
├── audios/              # Converted MP3 files
├── jsons/               # Transcribed JSON with timestamps
├── video_to_mp3.py      # Video → MP3 converter
├── mp3_to_json.py       # MP3 → JSON transcriber (Whisper)
├── preprocess_json.py   # JSON → Embeddings generator
├── process_incoming.py  # Query interface & LLM inference
├── embeddings.joblib    # Cached embeddings (auto-generated)
├── prompt.txt           # Last generated prompt
├── response.txt         # Last LLM response
└── Readme.md           # This file
```

## 🔧 Configuration

### Environment Variables
The system uses default local API endpoints:
- **Ollama Embed API**: `http://localhost:11434/api/embed`
- **Ollama Generate API**: `http://localhost:11434/api/generate`

### Model Parameters (in source files)
- **BGE-M3 Model**: Used for embeddings (`create_embedding()` in `preprocess_json.py`)
- **Llama 3.2 Model**: Used for text generation (`inference()` in `process_incoming.py`)
- **Top Results**: 5 similar chunks retrieved per query

## 📝 Dependencies

| Package | Purpose |
|---------|---------|
| `pandas` | Data frame operations |
| `scikit-learn` | Cosine similarity calculations |
| `numpy` | Numerical computations |
| `joblib` | Embedding serialization |
| `requests` | Ollama API calls |
| `openai-whisper` | Speech-to-text transcription |

## 🎯 Usage Example

```python
# Direct Python usage
import joblib
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load embeddings
df = joblib.load('embeddings.joblib')

# Create embedding for query
query_embedding = create_embedding(["your question"])[0]

# Find similar chunks
similarities = cosine_similarity(np.vstack(df['embedding']), [query_embedding]).flatten()
top_indices = similarities.argsort()[::-1][:5]

# Display results
for idx in top_indices:
    print(f"Video: {df.loc[idx, 'title']} at {df.loc[idx, 'start']}s")
    print(f"Content: {df.loc[idx, 'text']}")
```

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| FFmpeg not found | Ensure FFmpeg is in PATH or specify full path in `video_to_mp3.py` |
| Ollama connection error | Verify Ollama is running: `ollama serve` |
| Missing models | Pull models: `ollama pull bge-m3 && ollama pull llama3.2` |
| Memory issues | Process videos in smaller batches or use smaller Whisper model |
| Slow embeddings | Ensure sufficient RAM; consider using `bge-small-en-v1.5` instead of `bge-m3` |

## 📄 Output Files

- **`embeddings.joblib`**: Serialized DataFrame with embeddings (auto-generated)
- **`prompt.txt`**: Last formatted prompt sent to LLM
- **`response.txt`**: Last response from LLM
- **`jsons/*.json`**: Transcribed chunks with metadata

## 🔐 Notes

- All processing is local; no external API calls except Ollama
- Embeddings are cached; delete `embeddings.joblib` to regenerate
- Whisper uses GPU if available; falls back to CPU automatically
- LLM responses depend on model quality and context relevance

## 📌 Requirements Summary

- Python 3.8+
- FFmpeg
- Ollama with bge-m3 and llama3.2 models
- ~4GB RAM minimum (depends on video length and model size)
