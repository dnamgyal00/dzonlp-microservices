from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from pyctcdecode import build_ctcdecoder
import torch
import os
import librosa

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the ASR model and processor
model_path = "model/"
processor = Wav2Vec2Processor.from_pretrained(model_path)
model = Wav2Vec2ForCTC.from_pretrained(model_path)

@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file found'}), 400
    
    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected audio file'}), 400
    
    # Save the audio file temporarily
    audio_path = "temp_audio.wav"
    audio_file.save(audio_path)
    
    # Transcribe the audio
    transcription = process_audio(audio_path)
    
    # Delete the temporary audio file
    os.remove(audio_path)
    
    return jsonify({'transcription': transcription}), 200

def process_audio(audio_path):
    audio_input, sampling_rate = librosa.load(audio_path, sr=16000)
    input_values = processor(audio_input, sampling_rate=sampling_rate, return_tensors="pt").input_values
    logits = model(input_values).logits
    pred_ids = torch.argmax(logits, dim=-1)[0].cpu().numpy().tolist()
    transcription = processor.decode(pred_ids)
    return transcription

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1215)
