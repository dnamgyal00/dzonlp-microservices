import sys
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, request, jsonify

app = Flask(__name__)

model_path = "./model/en_to_dz"
tokenizer_path = "./model/tokenizer_en_to_dz"

model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)


def translate(text):
    try:
        # Translate the text.
        encoded_inputs = tokenizer(text, return_tensors="pt")
        outputs = model.generate(**encoded_inputs)
        translated_text = tokenizer.decode(
            outputs[0], skip_special_tokens=True)
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
            return jsonify({"text": result})
        else:
            return jsonify({"error": "Translation error"}), 500


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=1212)
