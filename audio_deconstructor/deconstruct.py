import os
import subprocess
import librosa
import numpy as np
import json

try:
    from spleeter.separator import Separator
except TypeError:
    from spleeter.separator import Separator as LegacySeparator
    Separator = LegacySeparator
PRETRAINED_MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pretrained_models")
os.environ["SPLEETER_MODEL_DIR"] = PRETRAINED_MODELS_DIR
def ensure_wav_compatibility(file_path):
    """
    Converts audio to WAV PCM 16-bit 44.1kHz using FFmpeg.
    Returns the path to the converted file.
    """
    base, ext = os.path.splitext(file_path)
    fixed_path = f"{base}_fixed.wav"

    if os.path.exists(fixed_path) and os.path.getmtime(fixed_path) > os.path.getmtime(file_path):
        return fixed_path

    try:
        subprocess.run([
            'ffmpeg', '-y', '-i', file_path,
            '-acodec', 'pcm_s16le', '-ar', '44100', fixed_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return fixed_path
    except Exception as e:
        print(f"[WARN] FFmpeg conversion failed for {file_path}. Using original. Error: {e}")
        return file_path

def separate_stems(input_path, output_dir):
    """
    Separates audio into 5 stems using a locally downloaded Spleeter model.
    """
    os.makedirs(output_dir, exist_ok=True)

    try:
        separator = Separator('spleeter:5stems', multiprocess=False)
        separator.separate_to_file(input_path, output_dir)
        print(f"Stems separated successfully to: {output_dir}")
        return True
    except Exception as e:
        print(f"[ERROR] Spleeter separation failed: {e}")
        return False
    
def extract_audio_features(audio_path):
    y, sr = librosa.load(audio_path, sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
    rms = np.mean(librosa.feature.rms(y=y))
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    return {
        "tempo_bpm": float(tempo),
        "num_beats": int(len(beats)),
        "spectral_centroid_mean": float(spectral_centroid),
        "spectral_rolloff_mean": float(spectral_rolloff),
        "zero_crossing_rate_mean": float(zero_crossing_rate),
        "rms_energy_mean": float(rms),
        "onset_count": int(len(onset_frames))
    }

def analyze_stems(stem_dir, feature_output_path):
    all_features = {}
    if not os.path.exists(stem_dir):
        print(f"Stem directory {stem_dir} does not exist.")
        return

    for stem_file in os.listdir(stem_dir):
        if stem_file.endswith('.wav'):
            stem_path = os.path.join(stem_dir, stem_file)
            features = extract_audio_features(stem_path)
            all_features[stem_file] = features
            print(f"Extracted features for {stem_file}")

    os.makedirs(os.path.dirname(feature_output_path), exist_ok=True)
    with open(feature_output_path, 'w') as f:
        json.dump(all_features, f, indent=4)
    print(f"Features saved to {feature_output_path}")

def deconstruct_audio(input_file_path: str, output_root_dir: str) -> str:
    """
    Main function to deconstruct audio file into stems.
    Returns the path to the folder containing stems.
    """
    compatible_path = ensure_wav_compatibility(input_file_path)

    if not separate_stems(compatible_path, output_root_dir):
        raise RuntimeError(f"Audio separation failed for file: {input_file_path}")

    base_name = os.path.basename(compatible_path)
    track_name = os.path.splitext(base_name)[0]
    stems_folder = os.path.join(output_root_dir, track_name)

    if not os.path.exists(stems_folder):
        # fallback: maybe Spleeter added "_fixed" to folder
        stems_folder = os.path.join(output_root_dir, f"{track_name}_fixed")
        if not os.path.exists(stems_folder):
            print(f"Stem folder not found. Returning root output dir.")
            return output_root_dir

    return stems_folder

if __name__ == "__main__":
    input_track = "input/track.mp3"
    output_root = "output"

    if os.path.exists(input_track):
        print("--- Running standalone deconstruction test ---")
        stems_folder_path = deconstruct_audio(input_track, output_root)
        print(f"Deconstruction complete! Stems are in: {stems_folder_path}")
    else:
        print(f"Please place a test file at '{input_track}' to run this script.")
