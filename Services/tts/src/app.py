from flask import Flask, request, send_file, jsonify
# from TTS.api import TTS
from pathlib import Path
from flask_cors import CORS
import os  # Added for temporary file handling

# # Initialize the TTS model with the appropriate model and config paths
# tts = TTS(
#     model_path=Path("./best_model_8910_overflow.pth"),
#     config_path=Path("./config_overflow.json"),
#     progress_bar=True,
#     gpu=False  # Specify whether to use the GPU (if available)
# )

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# def synthesize_wylie_text(input_wylie_text, output_audio_file: Path):
#     # Synthesize speech from Wylie Transcript
#     tts.tts_to_file(text=input_wylie_text, file_path=output_audio_file)

# @app.route("/convert", methods=["POST"])
# def convert_wylie_to_audio():
#     # Get the Wylie text from the request body
#     wylie_text = request.json["wylie_text"]

#     # Generate the audio file
#     output_audio_file = Path("output.wav")
#     synthesize_wylie_text(wylie_text, output_audio_file)

#     # Send the audio file as the response
#     response = send_file(output_audio_file, mimetype="audio/wav")

#     # Delete the audio file
#     output_audio_file.unlink()

#     # Set CORS headers
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Headers"] = "*"
#     response.headers["Access-Control-Allow-Methods"] = "*"

#     return response


@app.route('/text_to_audio', methods=['POST'])
def text_to_audio():
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request body"}), 400
            
        text = data['text']
        print(f"Received text: {text}")  # For testing

        # Here, you would generate audio from text
        # For demonstration, I'll return a sample audio file
        sample_audio_path = os.path.join(os.path.dirname(__file__), "sample_audio.wav")
        if not os.path.exists(sample_audio_path):
            return jsonify({"error": "sample_audio.wav not found in the same directory."}), 500

        return send_file(
            sample_audio_path,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="sample_audio.wav"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return jsonify(
        status="UP"
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)