from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response
import httpx

app = FastAPI()

DZO_TO_ENG_URL = 'http://10.2.5.72:1213/translate'
ENG_TO_DZO_URL = 'http://10.2.5.72:1212/translate'
TTS_URL = 'http://10.2.5.72:1214/convert'
ASR_URL = 'http://10.2.5.72:1215/convert'

# Use an HTTPX client for connection pooling
http_client = httpx.AsyncClient()

@app.get("/nmt/dzo-to-eng")
async def service1(text: str):
    try:
        response = await http_client.get(DZO_TO_ENG_URL, params={"text": text})
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        logging.error(f"Error requesting {exc.request.url!r}: {exc}")
        raise HTTPException(status_code=500, detail="Service1 error")

@app.get("/nmt/eng-to-dzo")
async def service2(text: str):
    try:
        response = await http_client.get(ENG_TO_DZO_URL, params={"text": text})
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        logging.error(f"Error requesting {exc.request.url!r}: {exc}")
        raise HTTPException(status_code=500, detail="Service2 error")

@app.post("/tts")
async def service3(request: Request):
    try:
        json_body = await request.json()
        response = await http_client.post(TTS_URL, json=json_body)
        response.raise_for_status()
        return Response(content=response.content, media_type="audio/wav")
    except httpx.RequestError as exc:
        logging.error(f"Error requesting {exc.request.url!r}: {exc}")
        raise HTTPException(status_code=500, detail="Failed to get TTS response")

@app.post("/asr")
async def convert_audio(file: bytes):
    try:
        files = {"audio_file": ("audio.wav", file, "audio/wav")}
        response = await http_client.post(ASR_URL, files=files)
        response.raise_for_status()
        return response.json()
    except httpx.RequestError as exc:
        logging.error(f"Error requesting {exc.request.url!r}: {exc}")
        raise HTTPException(status_code=500, detail="Failed to get ASR response")

# Ensure the HTTPX client is closed properly
@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()
