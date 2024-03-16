import re
import inflect
import os
from openai import OpenAI
from googletrans import Translator
import numpy as np

translator = Translator()


# Set an environment variable for the key
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", None)
client_op = OpenAI()  # add api_key


def convert_number_to_words(number: float) -> str:
    p = inflect.engine()
    words = p.number_to_words(number)
    words = translator.translate(words, dest="hy").text
    return words


def process_text(text: str) -> str:
    # Convert numbers to words
    words = []
    for word in text.split():
        # Check if the word is a number
        if re.search(r"\d", word):
            words.append(
                convert_number_to_words(int("".join(filter(str.isdigit, word))))
            )
        else:
            words.append(word)

    # Join the words back into a sentence
    processed_text = " ".join(words)

    # Remove URLs
    processed_text = re.sub(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        "",
        processed_text,
    )

    return processed_text


def tts(text, model, voice):
    text = process_text(text)
    response = client_op.audio.speech.create(
        model=model,  # "tts-1","tts-1-hd"
        voice=voice,  # 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'
        input=text,
    )

    # Get the audio data as a NumPy array
    audio_data = np.frombuffer(response.content, dtype=np.int16)

    # Convert the audio data to bytes for storage in the database
    audio_data_bytes = audio_data.tobytes()

    return audio_data_bytes
