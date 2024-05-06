# import sys
# import logging
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# model_path = "./model/en_to_dz"
# tokenizer_path = "./model/tokenizer_en_to_dz"

# model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
# tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

# def translate(text):
#     try:
#         # Translate the text.
#         encoded_inputs = tokenizer(text, return_tensors="pt")
#         outputs = model.generate(**encoded_inputs)
#         translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return translated_text
#     except Exception as e:
#         logging.error(f"Translation error: {str(e)}")
#         return None

# def main():
#     print("Model loaded successfully")
#     while True:
#         user_input = input().strip()
#         if user_input == "00":
#             print("Exiting...")
#             break
#         translation_result = translate(user_input)
#         if translation_result is not None:
#             print(translation_result)
#         else:
#             print("Translation error")

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     main()


import sys
import logging
import psutil
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_path = "./model/en_to_dz"
tokenizer_path = "./model/tokenizer_en_to_dz"

model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

def translate(text):
    try:
        # Translate the text.
        encoded_inputs = tokenizer(text, return_tensors="pt")
        outputs = model.generate(**encoded_inputs)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        logging.error(f"Translation error: {str(e)}")
        return None

def main():
    print("Model loaded successfully")
    while True:
        user_input = input().strip()
        if user_input == "00":
            print("Exiting...")
            break
        
        # Measure CPU usage before translation
        cpu_before = psutil.cpu_percent()
        
        translation_result = translate(user_input)
        
        # Measure CPU usage after translation
        cpu_after = psutil.cpu_percent()
        
        if translation_result is not None:
            print(translation_result)
        else:
            print("Translation error")
        
        # Print CPU usage
        print("CPU usage during translation:", cpu_after - cpu_before, "%")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
