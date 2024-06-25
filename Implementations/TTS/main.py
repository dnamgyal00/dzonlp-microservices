import os
import io
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from TTS.api import TTS
from pydub import AudioSegment

app = FastAPI()

# Enable CORS for all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print('========== LOADING TTS MODEL ==========')
tts = TTS(
    model_path="./best_model_26040.pth", 
    config_path="./config_26040.json", 
    progress_bar=True, gpu=False
)
print('========== LOADED TTS MODEL ==========')

class WylieRequest(BaseModel):
    wylie_text: str

def split_input_into_sentence(input_sen: str, limit=30):
    input_sen = input_sen.replace('/', '/ ')
    words = input_sen.split()
    return [' '.join(words[i:i+limit]) for i in range(0, len(words), limit)]

def concatenate_audio_files(input_files):
    final_audio = AudioSegment.empty()
    for file in input_files:
        final_audio += AudioSegment.from_file(file)
    with io.BytesIO() as audio_buffer:
        final_audio.export(audio_buffer, format="wav")
        audio_data = audio_buffer.getvalue()
    # Clean up the temporary audio files
    for file in input_files:
        os.remove(file)
    return audio_data

def predict_using_tts_api(wylie_transcript, fileName):
    try:
        print('======= Predicting ========')

        # Ensure the directory for output exists
        output_dir = Path("media/tts_output_wavs")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Clear old files if necessary
        for old_file in output_dir.glob("*"):
            old_file.unlink()

        splitted_sentences = split_input_into_sentence(wylie_transcript)

        counter_file_name = 0
        output_wavs = []
        for sentence in splitted_sentences:
            print('Sentence: ', sentence)
            path_to_save = output_dir / f"{fileName}_{counter_file_name}.wav"
            output_wavs.append(path_to_save)
            transcript = f"{sentence}"
            tts.tts_to_file(text=transcript, file_path=str(path_to_save))
            counter_file_name += 1

        # Concatenate the audio files and get the byte data
        audio_data = concatenate_audio_files(output_wavs)

        return audio_data
    except Exception as e:
        print(f"Error during TTS prediction: {e}")
        raise

def normalize_number(input_text):
    number_map = {'༠': 'ཀླད་ཀོར', '༡': 'གཅིག་', '༢': 'གཉིས་', '༣': 'གསུམ་',
                  '༤': 'བཞི་', '༥': 'ལྔ་', '༦': 'དྲུག་', '༧': 'བདུན་', '༨': 'བརྒྱད་', '༩': 'དགུ་'}
    for dz, en in number_map.items():
        input_text = input_text.replace(dz, en)
    return input_text

@app.post("/convert")
async def convert_wylie_to_audio(request: WylieRequest):
    try:
        dzo = request.wylie_text
        if not dzo:
            raise HTTPException(status_code=400, detail="Missing 'wylie_text' in request body")

        lines = dzo.split('\n')
        wylie_transcriptions = []

        for line in lines:
            text = normalize_number(line.strip())
            wylie_transcriptions.append(convert_dzongkha_text_to_wylie(text))

        # Join all transcriptions into a single string
        full_wylie_text = ' '.join(wylie_transcriptions)
        print(f"Full Wylie Transcription: {full_wylie_text}")

        # Define output directory and ensure it exists
        output_dir = Path("media/tts_output_wavs")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define path for the output audio file
        output_audio_file = output_dir / "output.wav"

        # Generate audio data using the TTS synthesizer
        audio_data = predict_using_tts_api(full_wylie_text, 'output_audio_file')

        return StreamingResponse(io.BytesIO(audio_data), media_type="audio/wav")

    except Exception as e:
        print(f"Error during conversion: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def convert_dzongkha_text_to_wylie(dzo_text):
    java_command = f'java CustomToWylie "{dzo_text}"'
    wyile_output = os.popen(java_command).read()
    print(wyile_output)
    return wyile_output

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1214)
