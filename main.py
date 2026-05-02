import io
import os
import tempfile
os.environ["USE_TF"] = "0"
import torch
import librosa
from fastapi import FastAPI, UploadFile, File, Form
from transformers import Speech2TextProcessor, Speech2TextForConditionalGeneration
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

app = FastAPI(title="Speech Processing & Translation API")

# Resolve absolute paths based on backend directory location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASR_MODEL_PATH = os.path.join(BASE_DIR, "model")
ASR_PROCESSOR_PATH = os.path.join(BASE_DIR, "processor")
TRANSLATION_MODEL_PATH = os.path.join(BASE_DIR, "pipe")

# Load Models
print("Loading Speech2Text Processor...")
processor = Speech2TextProcessor.from_pretrained(ASR_PROCESSOR_PATH)
print("Loading Speech2Text Model...")
model_asr = Speech2TextForConditionalGeneration.from_pretrained(ASR_MODEL_PATH, low_cpu_mem_usage=True)

print("Loading M2M100 Tokenizer...")
tokenizer_mt = M2M100Tokenizer.from_pretrained(TRANSLATION_MODEL_PATH)
print("Loading M2M100 Model...")
model_mt = M2M100ForConditionalGeneration.from_pretrained(TRANSLATION_MODEL_PATH, low_cpu_mem_usage=True)

print("Models loaded successfully.")

@app.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        content = await audio_file.read()
        
        # Librosa's fallback decoder (audioread) cannot read MP3/AAC from memory (BytesIO).
        # We must write it to a temporary file first.
        ext = os.path.splitext(audio_file.filename)[1] if audio_file.filename else ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
            
        try:
            # Load audio using librosa from the temp file (automatically resamples to 16kHz)
            speech, rate = librosa.load(tmp_path, sr=16000)
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
        # Process input
        inputs = processor(speech, sampling_rate=16000, return_tensors="pt")
        
        # Generate transcription
        generated_ids = model_asr.generate(inputs["input_features"], attention_mask=inputs.get("attention_mask"))
        transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return {"transcription": transcription}
    except Exception as e:
        error_msg = str(e)
        if type(e).__name__ == "NoBackendError":
            error_msg = "Audio format not supported natively. Please install 'FFmpeg' on your Windows machine to process AAC/MP3/M4A files."
        elif not error_msg:
            error_msg = f"Unknown error: {type(e).__name__}"
        return {"error": error_msg}

@app.post("/translate")
async def translate_text(text: str = Form(...), target_lang: str = Form(...)):
    try:
        # Set source language to English
        tokenizer_mt.src_lang = "en"
        
        # Tokenize text
        encoded_text = tokenizer_mt(text, return_tensors="pt")
        
        # Generate translation
        generated_tokens = model_mt.generate(
            **encoded_text, 
            forced_bos_token_id=tokenizer_mt.get_lang_id(target_lang)
        )
        translation = tokenizer_mt.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        
        return {"translation": translation}
    except Exception as e:
        return {"error": str(e)}
