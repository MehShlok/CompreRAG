# Ollama Setup Guide

Ollama allows you to run LLMs (like Llama 3, Mistral) **locally on your machine** for **FREE**. No API keys, no rate limits, no internet required after download!

## Installation Steps

### Step 1: Install Ollama

**On Windows (WSL):**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**On Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**On macOS:**
```bash
brew install ollama
```

**Or download installer from:** https://ollama.com/download

### Step 2: Start Ollama Service

After installation, start the Ollama service:
```bash
ollama serve
```

Leave this running in the background. You can also just run `ollama` which will auto-start the service.

### Step 3: Pull a Model

Download a model (I recommend **llama3.2** - 2GB, fast and good quality):

```bash
ollama pull llama3.2
```

**Other recommended models:**
- `llama3.2:1b` (1.3GB) - Smaller, faster, less accurate
- `mistral` (4.1GB) - Larger, more accurate
- `phi3` (2.3GB) - Good for educational tasks

To see all available models: https://ollama.com/library

### Step 4: Verify Installation

Test that Ollama is working:
```bash
ollama list
```

You should see your downloaded model listed.

### Step 5: Install Python Package

In your project directory:
```bash
pip install ollama
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## Running the Kanchan Agent

Once Ollama is set up, just run:
```bash
python main.py
```

The agent will automatically use Ollama (default model: `llama3.2`).

## Changing the Model

To use a different model, edit `main.py`:
```python
agent = AgentOrchestrator(vector_store, model_name="mistral")  
```

Or update the `.env` file:
```
OLLAMA_MODEL=mistral
```

## Troubleshooting

**Error: "Ollama not available"**
- Make sure Ollama service is running: `ollama serve`
- Verify model is pulled: `ollama list`

**Error: "model 'llama3.2' not found"**
- Pull the model first: `ollama pull llama3.2`

**Slow generation?**
- Try a smaller model like `llama3.2:1b`
- GPU acceleration is automatic if you have CUDA/ROCm

