import sys
import os
import traceback
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

from audio_deconstructor.deconstruct import deconstruct_audio

GENERATED_TRACK = "music_generator/output/edm_track.wav"
DECONSTRUCTED_DIR = "output/deconstructed"
os.makedirs(DECONSTRUCTED_DIR, exist_ok=True)

st.title("AI EDM Music Generator & Audio Deconstructor")
st.header("Generate Music")
prompt_text = st.text_input("Music Prompt", value="Martin Garrix style EDM")
if st.button("Generate Track"):
    if os.path.exists(GENERATED_TRACK):
        st.audio(GENERATED_TRACK, format="audio/wav")
        st.success(f"Generated track: {GENERATED_TRACK}")
    else:
        st.warning("No track generated. Make sure your music generator outputs to 'music_generator/output/edm_track.wav'.")

st.header("Deconstruct Audio")
uploaded_file = st.file_uploader("Upload Audio (.wav or .mp3)", type=["wav", "mp3"])

def visualize_stems(stem_folder):
    """Generate waveform and spectrogram plots for each stem."""
    images = []
    for f in sorted(os.listdir(stem_folder)):
        if f.endswith(".wav"):
            path = os.path.join(stem_folder, f)
            y, sr = librosa.load(path, sr=None)
            plt.figure(figsize=(12, 3))
            librosa.display.waveshow(y, sr=sr)
            plt.title(f"Waveform: {f}")
            plt.tight_layout()
            wave_path = os.path.join(stem_folder, f"{Path(f).stem}_waveform.png")
            plt.savefig(wave_path)
            plt.close()
            images.append(wave_path)
            D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
            plt.figure(figsize=(12, 4))
            librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
            plt.colorbar(format='%+2.0f dB')
            plt.title(f"Spectrogram: {f}")
            plt.tight_layout()
            spec_path = os.path.join(stem_folder, f"{Path(f).stem}_spectrogram.png")
            plt.savefig(spec_path)
            plt.close()
            images.append(spec_path)
    return images

if uploaded_file is not None:
    file_path = os.path.join(DECONSTRUCTED_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        st.info(f"Deconstructing {uploaded_file.name}...")
        stem_folder = deconstruct_audio(file_path, DECONSTRUCTED_DIR)
        st.success(f"Deconstruction completed! Stems in {stem_folder}")
        stems = [os.path.join(stem_folder, f) for f in os.listdir(stem_folder) if f.endswith(".wav")]
        if stems:
            st.subheader("Deconstructed Stems")
            for stem in stems:
                st.audio(stem, format="audio/wav")
        else:
            st.warning("No stems found.")
        images = visualize_stems(stem_folder)
        if images:
            st.subheader("Waveforms & Spectrograms")
            for img_path in images:
                st.image(img_path)

    except Exception as e:
        st.error(f"Error during deconstruction: {e}")
        traceback.print_exc()
