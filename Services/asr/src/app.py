# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
# from pyctcdecode import build_ctcdecoder
# import torch
# import os
# import librosa

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Load the ASR model and processor
# model_path = r"D:\dzonlp-microservices\Services\asr\model"
# processor = Wav2Vec2Processor.from_pretrained(model_path)
# model = Wav2Vec2ForCTC.from_pretrained(model_path)

# # Load the CTC decoder
# decoder = build_ctcdecoder(
#     model.config.vocab_size,
#     model.config.pad_token_id,
#     model.config.ctc_loss_reduction,
#     model.config.bos_token_id,  # Fix here
# )

# @app.route('/convert', methods=['POST'])
# def convert_audio():
#     if 'audio_file' not in request.files:
#         return jsonify({'error': 'No audio file found'}), 400
    
#     audio_file = request.files['audio_file']
#     if audio_file.filename == '':
#         return jsonify({'error': 'No selected audio file'}), 400
    
#     # Save the audio file temporarily
#     audio_path = "temp_audio.wav"
#     audio_file.save(audio_path)
    
#     # Transcribe the audio
#     try:
#         transcription = process_audio(audio_path)
#         os.remove(audio_path)  # Delete the temporary audio file
#         return jsonify({'transcription': transcription}), 200
#     except Exception as e:
#         os.remove(audio_path)  # Delete the temporary audio file in case of error
#         return jsonify({'error': str(e)}), 500

# def process_audio(audio_path):
#     try:
#         audio_input, sampling_rate = librosa.load(audio_path, sr=16000)
#         input_values = processor(audio_input, sampling_rate=sampling_rate, return_tensors="pt").input_values
#         logits = model(input_values).logits
#         pred_ids = torch.argmax(logits, dim=-1)[0].cpu().numpy().tolist()
#         transcription = processor.decode(pred_ids)
#         return transcription
#     except Exception as e:
#         raise RuntimeError(f"Error processing audio: {str(e)}")


from flask import Flask, request, send_file, jsonify
from pathlib import Path
from flask_cors import CORS
import os  # Added for temporary file handling

# # Initialize the TTS model with 
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/audio-to-text', methods=['POST'])
def audio_to_text():
    try:
        # Check if the request contains audio data
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        
        # Ensure the file has a supported format (e.g., WAV)
        if audio_file.filename == '' or not audio_file.filename.endswith('.wav'):
            return jsonify({"error": "Unsupported audio format, only WAV files are supported"}), 400

        # Save the audio file temporarily
        audio_path = os.path.join(os.path.dirname(__file__), "temp_audio.wav")
        audio_file.save(audio_path)

        # Here, you would perform audio-to-text processing
        # For demonstration, I'll return a sample text
        recognized_text = "This is a sample recognized text."

        # Remove the temporary audio file
        os.remove(audio_path)

        return jsonify({"text": recognized_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify(
        status="UP"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
