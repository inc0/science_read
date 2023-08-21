import click
from templates.arxiv import ArxivTemplate
from transformers import AutoProcessor, BarkModel, AutoTokenizer
import torch
from scipy.io.wavfile import write
import numpy as np
from tqdm import tqdm


@click.command()
@click.argument('src', nargs=1)
@click.argument('dest', nargs=1)
@click.option('--small', is_flag=True, default=False, help='Use small model for faster inference')
def read(src, dest, small):
    # TODO: add more than just arxiv web
    template = ArxivTemplate(src)
    title, text = template.parse()
    # TODO: there is also bark-small model for faster inference
    if small:
        processor = AutoProcessor.from_pretrained("suno/bark-small")
        model = BarkModel.from_pretrained("suno/bark-small")
    else:
        processor = AutoProcessor.from_pretrained("suno/bark")
        model = BarkModel.from_pretrained("suno/bark")
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    model.to(device)
    # TODO: add more than just english speaker. There are 9 speakers in total https://github.com/suno-ai/bark/tree/main/bark/assets/prompts/v2
    voice_preset = "v2/en_speaker_6"
    result = []

    for section in tqdm(text[:20]):
        inputs = processor(
            text=section,
            return_tensors="pt",
            voice_preset=voice_preset,
            max_length=512,  # TODO: this is hack to allow longer sentences in batch. We need to ensure that no batch has more than 512 tokens (words)
        )
        inputs.to(device)
        sampling_rate = 24_000
        # TODO: Bark procudes a lot of warnings about pad token. It doesn't affect the result but it's annoying and messes up tqdm progress bar
        speech_values = model.generate(**inputs)

        for s in speech_values.cpu().numpy():
            result.append(s)
            result.append(np.zeros(int(0.25 * sampling_rate))) # 0.25 seconds of silence between sentences
        
        result.append(np.zeros(int(0.5 * sampling_rate))) # 0.5 seconds of silence between sections

    result = np.concatenate(result)
    write(dest, sampling_rate, result)  # TODO: add option to save as mp3, wav are huge




if __name__ == "__main__":
    read()