from flask import Flask, jsonify
from flask_cors import CORS
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

model_path = r"D:\dzonlp-microservices\Services\nmt-dzo-to-eng\model\dz_to_en"  
tokenizer_path = r"D:\dzonlp-microservices\Services\nmt-dzo-to-eng\model\tokenizer_dz_to_en"  

model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

def translate(text):
    try:
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
        return jsonify({"error": "Missing 'text' query parameter"}), 400
    else:
        result = translate(text)
        if result is not None:
            return jsonify({"translation": result})
        else:
            return jsonify({"error": "Translation error"}), 500
        
@app.route("/health")
def health():
    return jsonify(status="UP")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
