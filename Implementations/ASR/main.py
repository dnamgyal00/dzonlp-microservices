import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import librosa

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the ASR model and processor
model_path = os.getenv('MODEL_DIR', '/app/models/')
processor = Wav2Vec2Processor.from_pretrained(model_path)
model = Wav2Vec2ForCTC.from_pretrained(model_path)

@app.post("/convert")
async def convert_audio(audio_file: UploadFile = File(...)):
    try:
        if not audio_file.filename:
            raise HTTPException(status_code=400, detail="No audio file provided")

        # Save the audio file temporarily
        audio_path = "/app/temp_audio.wav"
        with open(audio_path, "wb") as f:
            f.write(await audio_file.read())

        # Transcribe the audio
        transcription = process_audio(audio_path)
        
        # Delete the temporary audio file
        os.remove(audio_path)

        return {"transcription": transcription}
    except Exception as e:
        logging.error(f"Audio conversion error: {str(e)}")
        raise HTTPException(status_code=500, detail="Audio conversion error")

def process_audio(audio_path):
    audio_input, sampling_rate = librosa.load(audio_path, sr=16000)
    input_values = processor(audio_input, sampling_rate=sampling_rate, return_tensors="pt").input_values
    logits = model(input_values).logits
    pred_ids = torch.argmax(logits, dim=-1)[0].cpu().numpy().tolist()
    transcription = processor.decode(pred_ids)
    return transcription

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1215)
