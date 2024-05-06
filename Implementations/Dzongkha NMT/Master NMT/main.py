import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import json


class TrieNode:
    def __init__(self):
        self.children = {}
        self.translation = None


class EnglishToDzongkhaDictionary:
    def __init__(self):
        self.root = TrieNode()
        self.reverse_root = TrieNode()

    def insert(self, word, translation):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.translation = translation

    def insert_reverse(self, word, translation):
        node = self.reverse_root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.translation = translation

    def load_from_json(self, json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            for word, translation in data.items():
                self.insert(word.lower(), translation)
                self.insert_reverse(translation.lower(), word)

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.translation

    def reverse_search(self, word):
        node = self.reverse_root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.translation


# Define the paths to the model and tokenizer
model_en_to_dz = './model/en_to_dz'
tokenizer_en_to_dz = './model/tokenizer_en_to_dz'
model_dz_to_en = './model/dz_to_en'
tokenizer_dz_to_en = './model/tokenizer_dz_to_en'

# Load the tokenizer and model for English to Dzongkha translation
print("Loading English to Dzongkha model and tokenizer...")
tokenizer_en_to_dz = AutoTokenizer.from_pretrained(tokenizer_en_to_dz)
model_en_to_dz = AutoModelForSeq2SeqLM.from_pretrained(model_en_to_dz)

# Load the tokenizer and model for Dzongkha to English translation
print("Loading Dzongkha to English model and tokenizer...")
tokenizer_dz_to_en = AutoTokenizer.from_pretrained(tokenizer_dz_to_en)
model_dz_to_en = AutoModelForSeq2SeqLM.from_pretrained(model_dz_to_en)


# Create an instance of the Trie-based dictionary
dictionary = EnglishToDzongkhaDictionary()
dictionary.load_from_json('./model/dictionary.json')


def translate_english_to_dzongkha_model(text):
    translation_pipeline = pipeline(
        "translation", model=model_en_to_dz, tokenizer=tokenizer_en_to_dz, src_lang="eng_Latn", tgt_lang="dzo_Tibt")
    output = translation_pipeline(text)
    return output[0]['translation_text']


def translate_dzongkha_to_english_model(text):
    translation_pipeline = pipeline(
        "translation", model=model_dz_to_en, tokenizer=tokenizer_dz_to_en, src_lang="dzo_Tibt", tgt_lang="eng_Latn")
    output = translation_pipeline(text)
    return output[0]['translation_text']


def translateToDzo(word_to_translate):
    # Use the Trie dictionary to translate from English to Dzongkha
    translation_to_dzongkha = dictionary.search(word_to_translate.lower())
    return translation_to_dzongkha


def translateToEng(word_to_translate):
    # Use the Trie dictionary to translate from Dzongkha to English
    translation_to_english = dictionary.reverse_search(word_to_translate)
    return translation_to_english


# english_text = "Hello how are you?"
# dzongkha_translation = translate_english_to_dzongkha_model(english_text)
# print(f"English to Dzongkha: {english_text} -> {dzongkha_translation}")

# # Dzongkha to English translation
# dzongkha_text = "སྐུ་གཟུགས་བཟང་ ཁྱོད་ག་དེ་སྦེ་ཡོད?"
# english_translation = translate_dzongkha_to_english_model(dzongkha_text)
# print(f"Dzongkha to English: {dzongkha_text} -> {english_translation}")

# # Translate individual words
# word_to_translate_dzo = "གཅིག།"
# word_to_translate_eng = "Apple"
# dzo_translation = translateToEng(word_to_translate_dzo)
# eng_translation = translateToDzo(word_to_translate_eng)
# print(f"Dzongkha to English: {word_to_translate_dzo} -> {dzo_translation}")
# print(f"English to Dzongkha: {word_to_translate_eng} -> {eng_translation}")

text = [
    {
        "text": "Hello how are you?",
        "langSrc": "eng_Latn",
        "langTgt": "dzo_Tibt"
    },
    {
        "text": "སྐུ་གཟུགས་བཟང་ ཁྱོད་ག་དེ་སྦེ་ཡོད?",
        "langSrc": "dzo_Tibt",
        "langTgt": "eng_Latn"
    },
    {
        "text": "གསུམ།",
        "langSrc": "dzo_Tibt",
        "langTgt": "eng_Latn"
    },
    {
        "text": "apple",
        "langSrc": "eng_Latn",
        "langTgt": "dzo_Tibt"
    },
]

# Loop through each text
for text in text:

    if text["langSrc"] == "dzo_Tbt" and not text["text"].endswith("།"):
        input_text = text["text"] + "།"
    else:
        input_text = text["text"]

    if text["langSrc"] == "dzo_Tibt" and text["langTgt"] == "eng_Latn":
        if translateToEng(input_text):
            print(
                f"Dzongkha to English (Dictionary): {input_text} -> {translateToEng(input_text)}")
        else:
            translation = translate_dzongkha_to_english_model(input_text)
            print(
                f"Dzongkha to English (Model): {input_text} -> {translation}")

    elif text["langSrc"] == "eng_Latn" and text["langTgt"] == "dzo_Tibt":
        if translateToDzo(input_text):
            print(
                f"English to Dzongkha (Dictionary): {input_text} -> {translateToDzo(input_text)}")
        else:
            translation = translate_english_to_dzongkha_model(input_text)
            print(
                f"English to Dzongkha (Model): {input_text} -> {translation}")
