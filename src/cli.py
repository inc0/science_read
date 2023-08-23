import click
from templates.arxiv import ArxivTemplate
from transformers import AutoProcessor, BarkModel, AutoTokenizer
from transformers.utils import logging
import torch
from scipy.io.wavfile import write
import numpy as np
from tqdm import tqdm
from librosa.effects import trim, split


logging.set_verbosity_error()


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
    # TODO: add more than just english speaker. There are 9 speakers in total https://github.com/suno-ai/bark/tree/main/bark/assets/prompts/v2. Quality of results is different for each speaker though.
    voice_preset = "v2/en_speaker_6"
    result = []

    for section in tqdm(text):
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
            splitted = split(s, top_db=100)
            for ss in splitted:
                if ss[1] - ss[0] < 0.25 * sampling_rate:
                    continue
                result.append(s[ss[0]:ss[1]])
                result.append(np.zeros(int(0.15 * sampling_rate))) # 0.25 seconds of silence between sentences
        
        result.append(np.zeros(int(1.0 * sampling_rate))) # 1 second of silence between sections

    result = np.concatenate(result)
    if dest.endswith("wav"):
        write(dest, sampling_rate, result)


if __name__ == "__main__":
    read()