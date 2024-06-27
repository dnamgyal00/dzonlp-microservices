import os
import logging
from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define URLs for microservices
DZO_TO_ENG_URL = 'http://localhost:1213/translate'
ENG_TO_DZO_URL = 'http://localhost:1212/translate'
TTS_URL = 'http://localhost:1214/convert'
ASR_URL = 'http://localhost:1215/convert'

# CORS (Cross-Origin Resource Sharing) settings
origins = [
    "*",  # Allow all origins (not recommended for production)
    # Add more origins as needed
]

# Add CORS middleware to allow specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class TranslationRequest(BaseModel):
    text: str

class Settings(BaseModel):
    authjwt_secret_key: str = "123456"  # Replace with your actual secret key

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

@app.post("/nmt/dzo-to-eng")
async def translate_dzo_to_eng(request: TranslationRequest, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(DZO_TO_ENG_URL, json={"text": request.text})

        # Check response status code
        if response.status_code == 200:
            return response.json()
        else:
            error_message = f"Error from DZO_TO_ENG_URL: {response.status_code} - {response.content}"
            raise HTTPException(status_code=response.status_code, detail=error_message)

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/nmt/eng-to-dzo")
async def translate_eng_to_dzo(request: TranslationRequest, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(ENG_TO_DZO_URL, json={"text": request.text})

        # Check response status code
        if response.status_code == 200:
            return response.json()
        else:
            error_message = f"Error from ENG_TO_DZO_URL: {response.status_code} - {response.content}"
            raise HTTPException(status_code=response.status_code, detail=error_message)

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {e}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/tts")
async def service3(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    try:
        json_body = await request.json()
        wylie_text = json_body.get('wylie_text')
        if not wylie_text:
            raise HTTPException(status_code=400, detail="Missing 'wylie_text' field in request body")

        async with httpx.AsyncClient() as client:
            response = await client.post(TTS_URL, json={"wylie_text": wylie_text})

        if response.status_code == 200:
            return Response(content=response.content, media_type="audio/wav")

        raise HTTPException(status_code=response.status_code, detail="Failed to get TTS response")
    except httpx.RequestError as e:
        logging.error(f"Error forwarding request to {TTS_URL}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/asr")
async def convert_audio(request: Request, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    try:
        audio_file = await request.body()
        files = {"audio_file": ("audio.wav", audio_file, "audio/wav")}

        async with httpx.AsyncClient() as client:
            response = await client.post(ASR_URL, files=files)

        if response.status_code == 200:
            return response.json()

        raise HTTPException(status_code=response.status_code, detail="Failed to get ASR response")
    except httpx.RequestError as e:
        logging.error(f"Error forwarding request to {ASR_URL}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=1216)
