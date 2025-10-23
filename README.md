# EDM Studio AI

**Tagline:**
*Instantly play AI-generated EDM tracks and explore your own music by deconstructing audio into stems — all in one intuitive Streamlit interface.*

---

## Table of Contents

* [Inspiration](#inspiration)
* [What it does](#what-it-does)
* [How we built it](#how-we-built-it)
* [Challenges we ran into](#challenges-we-ran-into)
* [Accomplishments that we're proud of](#accomplishments-that-were-proud-of)
* [What we learned](#what-we-learned)
* [What's next for EDM Studio AI](#whats-next-for-edm-studio-ai)
* [Project Structure](#project-structure)
* [Getting Started](#getting-started)
* [Dependencies](#dependencies)
* [Usage](#usage)

---

## Inspiration

We wanted to create a fun, interactive tool for EDM enthusiasts and aspiring music producers to **experience AI-generated EDM tracks** while also exploring the inner structure of music. Many existing AI music demos either generate audio without giving insight into the composition or require expensive GPU setups. Our goal was to make a **hackathon-ready, accessible platform** that demonstrates both generation and audio deconstruction in a simple interface using Streamlit.

---

## What it does

**EDM Studio AI** lets users:

1. **Play a pre-generated EDM track** in the style of Martin Garrix.
2. **Upload their own audio files** (wav/mp3) and automatically deconstruct them into stems such as vocals and accompaniment.
3. **Listen to and explore** both generated and deconstructed audio directly in a user-friendly web interface.

---

## How we built it

* **Music Generation:** Pre-generated EDM track stored in the project to avoid GPU constraints.
* **Audio Deconstruction:** Implemented using **Spleeter** and **Librosa** for separating stems.
* **Frontend:** Built with **Streamlit**, providing an intuitive layout with tabs for music generation and audio deconstruction.
* **Backend (optional):** Python scripts manage file handling and processing.

---

## Challenges we ran into

* **GPU dependency:** MusicGen originally required a GPU; hosting on a CPU-based server like Render was infeasible.
* **User-friendly UI:** Ensuring both generation and deconstruction could coexist in a simple interface.
* **File management:** Handling multiple uploads and keeping generated/deconstructed files organized.

---

## Accomplishments that we're proud of

* Created a **fully functional, interactive demo** that works without live GPU generation.
* Successfully integrated **audio playback and file deconstruction** into one platform.
* Designed a **clean, hackathon-ready UI** using Streamlit.

---

## What we learned

* Learned how to **integrate AI audio models and audio processing tools** into a web interface.
* Gained experience with **Streamlit for building hackathon-ready demos**.
* Realized the importance of **pre-generated outputs** for rapid prototyping when GPU resources are limited.

---

## What's next for EDM Studio AI

* Add **live MusicGen generation** with GPU support for dynamic prompts.
* Expand audio deconstruction to **multi-stem separation** (e.g., drums, bass, synths).
* Improve UI with **audio galleries and progress indicators**.
* Deploy on a **cloud GPU environment** for real-time, interactive music generation.

---

## Project Structure

```
AI-EDM-track-generator-deconstructor/
│
├── audio_deconstructor/
│   ├── input/
│   ├── output/
│   └── deconstruct.py           # Spleeter + Librosa logic
│
├── music_generator/
│   ├── output/
│   │   └── edm_track.wav        # Pre-generated EDM track
│   └── music_generator.ipynb    # Optional notebook code
│
├── frontend/
│   └── app.py                   # Streamlit interface
│
├── output/
│   ├── generated/
│   └── deconstructed/
│
├── requirements.txt
└── README.md
```

---

## Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/extremecoder-rgb/AI-EDM-track-generator-deconstructor
cd AI-EDM-track-generator-deconstructor
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Dependencies

* streamlit==1.25.0
* numpy==1.26.4
* soundfile==0.12.1
* librosa==0.10.3.post2
* spleeter==2.5.2

> GPU packages like torch or Audiocraft are **not required** for this static demo.

---

## Usage

Run the Streamlit app:

```bash
streamlit run frontend/app.py
```

* **Generate Music Tab:** Click “Play Track” to listen to the pre-generated EDM track (`edm_track.wav`).
* **Deconstruct Audio Tab:** Upload `.wav` or `.mp3` files to deconstruct into stems.

All outputs are stored in:

* `output/generated/`
* `output/deconstructed/`

---
