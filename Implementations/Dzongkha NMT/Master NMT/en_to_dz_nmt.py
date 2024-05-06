import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, request, jsonify

app = Flask(__name__)

model = AutoModelForSeq2SeqLM.from_pretrained("./model/en_to_dz")
tokenizer = AutoTokenizer.from_pretrained("./model/tokenizer_en_to_dz")


def translate(text):
    # Translate the text.
    encoded_inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**encoded_inputs)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text


@app.route('/translate', methods=['POST'])
def translation():
    content = request.get_json()
    text = content.get('text')
    result = translate(text)
    return jsonify({"translation": result})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)  # Run the API
