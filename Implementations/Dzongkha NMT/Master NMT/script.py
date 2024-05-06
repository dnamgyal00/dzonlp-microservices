from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


def translate(text):
    # Load the model and tokenizer.
    print("Loading model....")
    model = AutoModelForSeq2SeqLM.from_pretrained("./model/en_to_dz")
    print("Loading tokenizer....")
    tokenizer = AutoTokenizer.from_pretrained("./model/tokenizer_en_to_dz")

    # Translate the text.
    print("Translating....")
    encoded_inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**encoded_inputs)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Translated....")

    return translated_text
