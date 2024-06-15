from flask import Flask, jsonify
from flask_cors import CORS
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

model_path = "../model/en_to_dz"  # Use raw string (r"") to avoid escape characters
tokenizer_path = "../model/tokenizer_en_to_dz"  # Use raw string (r"") to avoid escape characters

model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

with open('../../dict.json', 'r', encoding='utf-8') as f:
    translation_dict = json.load(f)

def translate(text):
    try:
        # Check if text is a single word and exists in the dictionary
        if text.lower() in translation_dict:
            return translation_dict[text.lower()]

        # If not in the dictionary, use the model
        encoded_inputs = tokenizer(text, return_tensors="pt")
        outputs = model.generate(**encoded_inputs)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        logging.error(f"Translation error: {str(e)}")
        return None

@app.route('/translate', methods=['GET'])
def translation():
    text = request.args.get('text')
    if text is None:
        # Return a 400 Bad Request response
        return jsonify({"error": "Missing 'text' query parameter"}), 400
    else:
        result = translate(text)
        if result is not None:
            return jsonify({"translation": result})
        else:
            return jsonify({"error": "Translation error"}), 500
        
@app.route("/health")
def health():
    return jsonify(
        status="UP"
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)