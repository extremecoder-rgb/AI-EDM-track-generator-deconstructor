import os
import json
import librosa
import numpy as np
import subprocess
from spleeter.separator import Separator

def ensure_wav_compatibility(file_path):
    """Re-encode WAV files to standard PCM 16-bit format (Windows-safe)."""
    fixed_path = file_path.replace('.wav', '_fixed.wav')
    if not os.path.exists(fixed_path):
        try:
            subprocess.run([
                'ffmpeg', '-y', '-i', file_path,
                '-acodec', 'pcm_s16le', '-ar', '44100', fixed_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"[⚠] FFmpeg conversion failed for {file_path}: {e}")
            return file_path
    return fixed_path

def separate_stems(input_path, output_dir):
    """Use Spleeter to separate audio into 5 stems."""
    os.makedirs(output_dir, exist_ok=True)
    separator = Separator('spleeter:5stems')
    separator.separate_to_file(input_path, output_dir)
    print(f"[✔] Stems saved to {output_dir}")

def extract_audio_features(audio_path):
    """Extract audio features using Librosa."""
    audio_path = ensure_wav_compatibility(audio_path)
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
    """Extract and save Librosa features for each stem."""
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

if __name__ == "__main__":
    input_track = "input/track.mp3"
    output_root = "output"
    separate_stems(input_track, output_root)
    stems_dir = os.path.join(output_root, os.path.splitext(os.path.basename(input_track))[0])
    features_path = os.path.join(output_root, "features", "features.json")
    analyze_stems(stems_dir, features_path)

    print("\nDeconstruction complete!")
