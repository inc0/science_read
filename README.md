## **Text-to-Speech for Scientific Papers**
---

### **Introduction**

In the fast-paced world of academia and research, keeping up with the latest scientific papers can be a daunting task. While reading remains the traditional method of consuming this knowledge, not everyone finds it the most effective or convenient. That's where our Text-to-Speech (TTS) for Scientific Papers comes into play.

#### **Why Use Text-to-Speech for Scientific Papers?**

- **Auditory Learning**: Some individuals are auditory learners, meaning they grasp and retain information better when they hear it. Converting scientific papers to audio can cater to this learning style, allowing them to understand and recall complex concepts more easily.

- **Multitasking**: In today's busy world, not everyone has the luxury of sitting down to read a paper. With TTS, users can now listen to the latest research while driving, cooking, working out, or performing chores. It not only makes use of time more efficiently but also integrates continuous learning into daily routines.

- **Accessibility**: For those with visual impairments or other conditions that make reading difficult, TTS offers an alternative way to access and consume the vast world of scientific knowledge.

By providing a platform that converts dense and intricate scientific texts into audible content, we hope to make research more accessible, digestible, and convenient for everyone, regardless of their preferred learning method or lifestyle.


## Installation

`pip install https://github.com/inc0/science_read.git`

## Usage

Simple usage example

```
scienceread https://www.biorxiv.org/content/10.1101/2023.08.05.552127v1.full paper.wav
```

Currently project only supports arxiv papers with full text available on web. Click on "full text" tab on arxiv and copy url. 

Magic is done by [Bark](https://huggingface.co/docs/transformers/main/model_doc/bark) model. It's state of the art TTS model available.

It may take a long time to process paper (it took about 30min on Nvidia 4090 to fully transcribe example paper). For that reason we also added `--small` flag that uses smaller version of model. It's quite a bit faster and doesn't require such heavy compute, but it also gets "confused" more often and produces more artifacts.

## Contribution

This is very early version of the tool. All contributions are welcome. There are number of `TODO` comments. Larger problems are described in the issue tracker.