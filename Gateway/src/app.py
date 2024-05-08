from flask import Flask, request, jsonify,Response
from flask_cors import CORS
import requests
import logging
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Define the URLs for your microservices
DZO_TO_ENG_URL = 'http://10.2.4.11:1213/translate'
ENG_TO_DZO_URL = 'http://10.2.4.11:1212/translate'
TTS_URL = 'http://10.2.4.11:1214/convert'
ASR_URL = 'http://10.2.4.11:1215/convert'
# DZO_TO_ENG_URL = 'http://127.0.0.1:5000/translate'
# ENG_TO_DZO_URL = 'http://127.0.0.1:5001/translate'
# TTS_URL = 'http://127.0.0.1:5003/text_to_audio'
# ASR_URL = 'http://127.0.0.1:5004/audio-to-text'

def forward_request_to_microservice(url, data):
    try:
        response = requests.get(url, params=data)
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error forwarding request to {url}: {str(e)}")
        return None

@app.route('/nmt/dzo-to-eng')
def service1():
    data = request.args.to_dict()
    if not data:
        return jsonify({"error": "Missing data in request"}), 400
    result = forward_request_to_microservice(DZO_TO_ENG_URL, data)
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({"error": "Service1 error"}), 500

@app.route('/nmt/eng-to-dzo')
def service2():
    data = request.args.to_dict()
    if not data:
        return jsonify({"error": "Missing data in request"}), 400
    result = forward_request_to_microservice(ENG_TO_DZO_URL, data)
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({"error": "Service2 error"}), 500


@app.route('/tts', methods=['POST'])
def service3():
    try:
        data = request.json
        if not data or 'wylie_text' not in data:
            return jsonify({"error": "Missing 'wylie_text' field in request body"}), 400
            
        wylie_text = data['wylie_text']

        tts_response = requests.post(TTS_URL, json={"wylie_text": wylie_text})
        tts_response.raise_for_status()  # Raise an exception for HTTP errors
        audio_data = tts_response.content
        return Response(audio_data, mimetype='audio/wav', content_type='audio/wav')
    except requests.RequestException as e:
        # Log the error and return an error response
        logging.error(f"Error forwarding request to {TTS_URL}: {str(e)}")
        return jsonify({"error": "Failed to get TTS response"}), 500
    


@app.route('/asr', methods=['POST'])
def convert_audio():
    try:
        # Check if the request contains audio data
        if 'audio_file' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio_file = request.files['audio_file']
        
        # Ensure the file has a supported format (e.g., WAV)
        if audio_file.filename == '' or not audio_file.filename.endswith('.wav'):
            return jsonify({"error": "Unsupported audio format, only WAV files are supported"}), 400
        
        # Forward the audio to ASR service
        asr_response = requests.post(ASR_URL, files={'audio_file': audio_file})
        asr_response.raise_for_status()  # Raise an exception for HTTP errors
        
        transcription = asr_response.json().get('transcription')

        return jsonify({"transcription": transcription}), 200

    except requests.exceptions.HTTPError as err:
        return jsonify({"error": f"{err.response.status_code} Client Error: {err.response.text}"}), err.response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111)