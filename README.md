# 🎙️ Resonance: AI Audio Transcription & Translation

Resonance is a sophisticated, End-to-End Deep Learning application that performs highly accurate Speech-to-Text transcription and real-time Multi-lingual translation.

It is built with **FastAPI** for a robust, decoupled AI inference backend, and **Streamlit** for a modern, dashboard-style frontend.

## 🚀 Features
- **Speech Recognition**: Transcribes spoken audio (WAV, MP3, FLAC, OGG, AAC, M4A) to text using HuggingFace's `Speech2Text` model.
- **Microphone Support**: Record your voice directly in the browser to process it instantly.
- **Real-time Translation**: Instantly translates transcriptions into Hindi, Urdu, French, Spanish, German, or Chinese using Meta's `M2M100` machine translation model.

## 🛠️ Tech Stack
- **Frontend**: Streamlit
- **Backend**: FastAPI, Uvicorn
- **AI Models**: PyTorch, Transformers (HuggingFace)
- **Audio Processing**: Librosa, FFmpeg

## 📥 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/resonance.git
   cd resonance
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (Required for processing compressed formats like AAC and MP3):
   - Windows: `winget install Gyan.FFmpeg`
   - Linux: `sudo apt install ffmpeg`
   - Mac: `brew install ffmpeg`

## 🧠 Model Setup (Important)
Because AI models are extremely large, they are not included in this GitHub repository. You must download the models separately and place them in the following folders in the root directory:
- `model/` (Speech2Text Model files)
- `processor/` (Speech2Text Processor files)
- `pipe/` (M2M100 Translation Model files)

## 🎯 Running the Application

You can start both the backend and frontend simultaneously by double-clicking the provided batch script on Windows:
```cmd
run.bat
```

**Or start them manually in two separate terminal windows:**
1. Start the FastAPI Backend:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
2. Start the Streamlit Frontend:
   ```bash
   streamlit run app.py
   ```

## 👨‍💻 Developed By
**Syed Muhammad Zeeshan**
