import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load model and tokenizer once and share them
model_path = os.getenv('MODEL_DIR', '/app/models/dz_to_en')
tokenizer_path = os.getenv('TOKENIZER_DIR', '/app/models/tokenizer_dz_to_en')

model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

class TranslationRequest(BaseModel):
    text: str

@app.post("/translate")
async def translate(request: TranslationRequest):
    try:
        encoded_inputs = tokenizer(request.text, return_tensors="pt")
        outputs = model.generate(**encoded_inputs)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"translation": translated_text}
    except Exception as e:
        logging.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1213)
