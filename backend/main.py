from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from generate_pipeline import generate_music_pipeline
from deconstruct_pipeline import run_deconstruction
import soundfile as sf
import uuid
import os

app = FastAPI()

GENERATED_DIR = "backend/media/generated"
DECONSTRUCTED_DIR = "backend/media/deconstructed"

os.makedirs(GENERATED_DIR, exist_ok=True)
os.makedirs(DECONSTRUCTED_DIR, exist_ok=True)


@app.post("/generate")
async def generate(prompt: str = Form(...), duration: int = Form(8)):
    """
    Generate music from a text prompt.
    Returns the path of the generated WAV file.
    """
    try:
        audio_list = generate_music_pipeline([prompt], duration=duration)
        file_name = f"{GENERATED_DIR}/{uuid.uuid4()}.wav"
        sf.write(file_name, audio_list[0].cpu().numpy(), 32000)
        return {"status": "success", "file": file_name}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.post("/deconstruct")
async def deconstruct(file: UploadFile = File(...)):
    """
    Deconstruct an uploaded audio file into stems.
    Returns paths of the deconstructed stems.
    """
    try:
        temp_file = f"{DECONSTRUCTED_DIR}/{uuid.uuid4()}_{file.filename}"
        with open(temp_file, "wb") as f:
            f.write(await file.read())
        
        result = run_deconstruction(temp_file)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.get("/")
def root():
    return {"status": "running", "endpoints": ["/generate", "/deconstruct"]}
