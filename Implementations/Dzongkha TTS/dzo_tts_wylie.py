from flask import Flask, request, send_file
from TTS.api import TTS
from pathlib import Path
from flask_cors import CORS
import os

# Initialize the TTS model with the appropriate model and config paths
tts = TTS(
    model_path=Path("./best_model_8910_overflow.pth"),
    config_path=Path("./config_overflow.json"),
    progress_bar=True,
    gpu=False  # Specify whether to use the GPU (if available)
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def synthesize_wylie_text(input_wylie_text, output_audio_file: Path):
    # Synthesize speech from Wylie Transcript
    tts.tts_to_file(text=input_wylie_text, file_path=output_audio_file)

@app.route("/convert", methods=["POST"])
def convert_wylie_to_audio():
    # Get the Wylie text from the request body
    dzo = request.json["wylie_text"]
    print(dzo)
    wylie_text = convert_dzongkha_text_to_wylie(dzo)

    # Generate the audio file
    output_audio_file = Path("output.wav")
    synthesize_wylie_text(wylie_text, output_audio_file)

    # Send the audio file as the response
    response = send_file(output_audio_file, mimetype="audio/wav")

    # Delete the audio file
    output_audio_file.unlink()

    # Set CORS headers
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"

    return response

def convert_dzongkha_text_to_wylie(dzo_text):
    java_command = f'java CustomToWylie "{dzo_text}"'
    wyile_output = os.popen(java_command).read()
    print(wyile_output)
    return wyile_output
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1214)
