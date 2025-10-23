import import_ipynb
import sys
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).parent.parent / "music_generator"))

import music_generator  

import torch
from audiocraft.utils.notebook import display_audio


def generate_music_pipeline(prompts: List[str], duration: int = 8, device: str = "cuda"):
    """
    Wrapper to generate music using the notebook's generate_music function.
    
    Args:
        prompts (List[str]): List of prompt strings for music generation.
        duration (int): Duration in seconds for each generated track.
        device (str): 'cuda' or 'cpu' for device placement.
    
    Returns:
        List of audio tensors
    """
    results = []
    for prompt in prompts:
        print(f"Generating music for prompt: {prompt}")
        audio = music_generator.generate_music(prompt=prompt, duration=duration, device=device)
        results.append(audio)
    return results


if __name__ == "__main__":
    test_prompts = ["Generate an Indian-style EDM like Martin Garrix."]
    generated_audio = generate_music_pipeline(test_prompts, duration=8)
    display_audio(generated_audio[0], 32000)
