from audio_deconstructor.deconstruct import deconstruct_audio
import os

OUTPUT_DIR = "backend/media/deconstructed"

def run_deconstruction(file_path: str) -> dict:
    """
    Takes an input audio file path and returns the path of deconstructed stems.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    stems_path = deconstruct_audio(file_path, OUTPUT_DIR)
    
    return {
        "status": "success",
        "stems_path": stems_path
    }
